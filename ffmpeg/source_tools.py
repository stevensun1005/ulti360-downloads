"""SPDX-License-Identifier: GPL-2.0-or-later. Pinned inputs and source delivery."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile

RECIPE = Path(__file__).resolve().parent
LOCK = json.loads((RECIPE / 'sources.json').read_text())
WORK = Path.cwd() / 'ffmpeg-build'
OUT = Path.cwd() / 'ffmpeg-dist'

def sha(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()

def fetch():
    archives = WORK / 'archives'
    archives.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(LOCK['sources']):
        target = archives / item['name']
        if not target.exists():
            supplied = Path.cwd() / 'archives' / item['name']
            if supplied.is_file():
                shutil.copy2(supplied, target)
            else:
                with urllib.request.urlopen(item['url'], timeout=120) as response, target.open('wb') as dest:
                    shutil.copyfileobj(response, dest)
        if sha(target) != item['sha256']:
            raise RuntimeError('Source checksum mismatch: ' + item['name'])
        folder = WORK / ('ffmpeg' if index == 0 else 'x264')
        if not folder.exists():
            unpack = WORK / ('unpack-' + str(index))
            unpack.mkdir(exist_ok=True)
            with tarfile.open(target) as archive:
                archive.extractall(unpack, filter='data')
            roots = list(unpack.iterdir())
            if len(roots) != 1 or not roots[0].is_dir():
                raise RuntimeError('Unexpected source archive layout')
            roots[0].rename(folder)

def run(*args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError('Command failed: ' + ' '.join(args) + '\n' + result.stderr[-4000:])
    return result.stdout + result.stderr

def finalize(platform):
    OUT.mkdir(exist_ok=True)
    binary = WORK / 'ffmpeg' / ('ffmpeg.exe' if platform == 'windows' else 'ffmpeg')
    records = WORK / 'records'
    records.mkdir(exist_ok=True)
    for option in ('version', 'buildconf', 'L', 'encoders', 'decoders', 'hwaccels'):
        (records / (option + '.txt')).write_text(run(str(binary), '-' + option), encoding='utf8')
    version = (records / 'version.txt').read_text()
    if '--enable-libx264' not in version or '--enable-nonfree' in version:
        raise RuntimeError('Unexpected FFmpeg configuration')
    externals = set(re.findall(r'--enable-lib[\w-]+', version))
    if externals != {'--enable-libx264'}:
        raise RuntimeError('Untracked external libraries: ' + str(externals))
    (records / 'compiler.txt').write_text(run('gcc' if platform == 'windows' else 'clang', '-v'), encoding='utf8')
    if platform == 'windows':
        dependencies = run('objdump', '-p', str(binary))
        dlls = re.findall(r'DLL Name:\s*(\S+)', dependencies, re.I)
        allowed = {'kernel32.dll','msvcrt.dll','ucrtbase.dll','user32.dll','advapi32.dll',
                   'bcrypt.dll','ole32.dll','oleaut32.dll','shell32.dll','shlwapi.dll',
                   'ws2_32.dll','secur32.dll','avrt.dll','winmm.dll','gdi32.dll',
                   'd3d11.dll','dxgi.dll','dxva2.dll','mfplat.dll','mfuuid.dll',
                   'strmiids.dll','psapi.dll','imm32.dll','version.dll','ntdll.dll',
                   'comdlg32.dll','comctl32.dll','vfw32.dll','opengl32.dll','dwmapi.dll',
                   'crypt32.dll','cryptbase.dll','dbghelp.dll','setupapi.dll','ksuser.dll',
                   'iphlpapi.dll','rpcrt4.dll','normaliz.dll','mfreadwrite.dll','mf.dll',
                   'propsys.dll','uuid.dll','winspool.drv'}
        unknown = [name for name in dlls if name.lower() not in allowed and not name.lower().startswith(('api-ms-', 'ext-ms-'))]
        if unknown:
            raise RuntimeError('Non-system DLL imports: ' + str(unknown))
    else:
        dependencies = run('otool', '-L', str(binary))
        paths = re.findall(r'^\s+(\S+)\s+\(', dependencies, re.M)
        if any(not path.startswith(('/usr/lib/', '/System/Library/')) for path in paths):
            raise RuntimeError('Non-system macOS library: ' + dependencies)
        if 'arm64' not in run('lipo', '-archs', str(binary)):
            raise RuntimeError('Not an Apple Silicon build')
    (records / 'system-dependencies.txt').write_text(dependencies, encoding='utf8')
    shutil.copy2(WORK / 'configure-command.txt', records)
    # Exercise the app's codecs, both lens streams, still preview, raw decoding and audio.
    sample = WORK / 'two-lens.OSV'
    run(str(binary), '-hide_banner', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i',
        'testsrc2=size=1920x1920:rate=25', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000',
        '-t', '0.12', '-map', '0:v', '-map', '0:v', '-map', '1:a', '-c:v', 'mpeg4', '-q:v', '10',
        '-c:a', 'aac', '-f', 'mp4', str(sample))
    run(str(binary), '-hide_banner', '-loglevel', 'error', '-i', str(sample), '-map', '0:v:1',
        '-frames:v', '1', '-vf', 'scale=320:320', '-f', 'image2pipe', '-vcodec', 'mjpeg', str(WORK / 'preview.jpg'))
    render = WORK / 'render.mp4'
    run(str(binary), '-hide_banner', '-loglevel', 'error', '-y', '-i', str(sample), '-t', '0.12',
        '-map', '0:v:1', '-map', '0:a:0', '-vf', 'scale=1280:720', '-c:v', 'libx264',
        '-preset', 'ultrafast', '-c:a', 'aac', str(render))
    run(str(binary), '-v', 'error', '-i', str(render), '-f', 'null', '-')
    manifest = {'schema': 1, 'revision': LOCK['revision'], 'platform': platform,
        'ffmpeg_sha256': sha(binary), 'source_inputs': LOCK,
        'external_libraries': ['x264'], 'system_dependencies': dependencies,
        'media_smoke': 'dual-square probe, MJPEG preview, H.264/AAC encode and full decode passed'}
    source_name = f'ffmpeg-corresponding-source-{platform}-{LOCK["revision"]}.zip'
    with zipfile.ZipFile(OUT / source_name, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in sorted((WORK / 'archives').iterdir()):
            archive.write(file, 'archives/' + file.name)
        for file in sorted(RECIPE.iterdir()):
            if file.is_file(): archive.write(file, 'build/' + file.name)
        for file in sorted(records.iterdir()): archive.write(file, 'build-record/' + file.name)
        for name in ('COPYING.GPLv2','COPYING.GPLv3','COPYING.LGPLv2.1','COPYING.LGPLv3','LICENSE.md'):
            archive.write(WORK / 'ffmpeg' / name, 'licenses/ffmpeg/' + name)
        archive.write(WORK / 'x264/COPYING', 'licenses/x264-COPYING')
        archive.writestr('source-manifest.json', json.dumps(manifest, indent=2) + '\n')
        if platform == 'windows':
            license_root = Path('/ucrt64/share/licenses')
            if license_root.is_dir():
                for file in sorted(license_root.rglob('*')):
                    if file.is_file(): archive.write(file, 'licenses/toolchain/' + file.relative_to(license_root).as_posix())
    manifest['source_archive'] = source_name
    manifest['source_archive_sha256'] = sha(OUT / source_name)
    manifest_name = f'ffmpeg-{platform}-{LOCK["revision"]}.json'
    (OUT / manifest_name).write_text(json.dumps(manifest, indent=2) + '\n')
    binary_name = f'ffmpeg-{platform}-{LOCK["revision"]}.zip'
    with zipfile.ZipFile(OUT / binary_name, 'w', zipfile.ZIP_DEFLATED) as archive:
        archive.write(binary, 'ffmpeg.exe' if platform == 'windows' else 'ffmpeg')
        archive.write(OUT / manifest_name, manifest_name)
        archive.write(WORK / 'ffmpeg/COPYING.GPLv2', 'COPYING.GPLv2')
        archive.write(WORK / 'x264/COPYING', 'x264-COPYING')
    for file in list(OUT.iterdir()):
        if file.suffix in ('.zip','.json'):
            file.with_name(file.name + '.sha256').write_text(sha(file) + '  ' + file.name + '\n')
    print(json.dumps(manifest, indent=2))

if __name__ == '__main__':
    if sys.argv[1] == 'fetch': fetch()
    else: finalize(sys.argv[2])
