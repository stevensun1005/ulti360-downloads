"""SPDX-License-Identifier: GPL-2.0-or-later. Repair the public 0.12.0 packages."""
from pathlib import Path
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile

REPO = 'stevensun1005/ulti360-downloads'
REV = '7.1-ulti360.1'
PLATFORM = sys.argv[1]
OUT = Path('repacked').resolve()
OUT.mkdir(exist_ok=True)

def sha(path):
    with path.open('rb') as source:
        return hashlib.file_digest(source, 'sha256').hexdigest()

def run(*args, **kwargs):
    return subprocess.run([str(x) for x in args], check=True, **kwargs)

def release(tag):
    request = urllib.request.Request(f'https://api.github.com/repos/{REPO}/releases/tags/{tag}',
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'User-Agent': 'ulti360-source-repack'})
    with urllib.request.urlopen(request) as response:
        return json.load(response)

def download(asset, folder):
    target = folder / asset['name']
    with urllib.request.urlopen(asset['browser_download_url'], timeout=120) as source, target.open('wb') as dest:
        shutil.copyfileobj(source, dest)
    if 'sha256:' + sha(target) != asset['digest']:
        raise RuntimeError('GitHub asset digest mismatch: ' + target.name)
    return target

def safe_extract(archive, target):
    with zipfile.ZipFile(archive) as bundle:
        for item in bundle.infolist():
            if not (target / item.filename).resolve().is_relative_to(target.resolve()):
                raise RuntimeError('Unsafe ZIP member')
        bundle.extractall(target)

native = release('ffmpeg-' + REV)
items = {x['name']: x for x in native['assets']}
manifest = download(items[f'ffmpeg-{PLATFORM}-{REV}.json'], OUT)
record = json.loads(manifest.read_text())
binary_zip = download(items[f'ffmpeg-{PLATFORM}-{REV}.zip'], OUT)
source_zip = download(items[record['source_archive']], OUT)
if sha(source_zip) != record['source_archive_sha256']:
    raise RuntimeError('Corresponding source mismatch')
binary_folder = OUT / 'ffmpeg'
safe_extract(binary_zip, binary_folder)
replacement = binary_folder / ('ffmpeg.exe' if PLATFORM == 'windows' else 'ffmpeg')
if sha(replacement) != record['ffmpeg_sha256']:
    raise RuntimeError('FFmpeg binary mismatch')
runtime_release = release('runtime-ffmpeg-1')
runtime_items = {x['name']:x for x in runtime_release['assets']}
runtime_path = download(runtime_items['runtime-ffmpeg-source.json'], OUT)
runtime = json.loads(runtime_path.read_text())
runtime_source = download(runtime_items[runtime['source_archive']], OUT)
if sha(runtime_source) != runtime['source_archive_sha256']:
    raise RuntimeError('Runtime corresponding source mismatch')
old = release('v0.12.0-beta.1')
app_name = 'ulti360-Windows.zip' if PLATFORM == 'windows' else 'ulti360-macOS-arm64.zip'
app_zip = download(next(x for x in old['assets'] if x['name'] == app_name), OUT)
stage = OUT / 'stage'
stage.mkdir()
if PLATFORM == 'macos':
    run('ditto', '-x', '-k', app_zip, stage)
    app = stage / 'ulti360.app'
    resources = app / 'Contents/Resources'
    root = resources
    engine = resources / 'runtime/macos/UltimateReframeEngine/UltimateReframeEngine'
else:
    safe_extract(app_zip, stage)
    app = stage / 'ulti360-Windows'
    root = app
    resources = app / 'resources'
    engine = resources / 'runtime/windows/UltimateReframeEngine/UltimateReframeEngine.exe'
bins = list((engine.parent / '_internal/imageio_ffmpeg/binaries').glob('ffmpeg-*'))
if len(bins) != 1:
    raise RuntimeError('Expected exactly one FFmpeg executable')
previous = sha(bins[0])
shutil.copy2(replacement, bins[0])
bins[0].chmod(0o755)
license_dir = resources / 'licenses/ffmpeg-ulti360'
license_dir.mkdir(parents=True, exist_ok=True)
runtime_notice = resources / 'licenses/runtime-ffmpeg'
runtime_notice.mkdir(parents=True,exist_ok=True)
shutil.copy2(runtime_path,runtime_notice/'source-manifest.json')
with zipfile.ZipFile(runtime_source) as source:
    (runtime_notice/'COPYING.LGPLv2.1').write_bytes(source.read('licenses/ffmpeg/COPYING.LGPLv2.1'))
if PLATFORM == 'macos':
    shared = download(runtime_items['ffmpeg-lgpl-macos-arm64.zip'], OUT)
    spec=importlib.util.spec_from_file_location('shared_install',Path('runtime-sources/install.py'))
    installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)
    runtime['installed']=installer.install_shared(engine.parent,shared,runtime)
else:
    plugin=engine.parent/'_internal/cv2/opencv_videoio_ffmpeg500_64.dll'
    if sha(plugin)!=runtime['source_inputs']['opencv_windows_ffmpeg_dll_sha256']:
        raise RuntimeError('Untracked OpenCV Windows FFmpeg plugin')
(runtime_notice/'source-manifest.json').write_text(json.dumps(runtime,indent=2)+'\n')
(runtime_notice/'SOURCES.txt').write_text(
    'Electron FFmpeg and OpenCV videoio FFmpeg: replaceable shared libraries.\n'
    'Exact source, patches, upstream configuration and scripts are supplied alongside the app.\n'
    f'https://github.com/{REPO}/releases/tag/runtime-ffmpeg-1\n'
    f'{runtime["source_archive"]}\nSHA256: {runtime["source_archive_sha256"]}\n'
    'You may reverse engineer this application as necessary to debug modifications to LGPL libraries.\n'
    'Replace the shared libraries at their original paths; on Mac re-sign your modified app locally with codesign --force --deep --sign -.\n'
    'Electron 与 OpenCV 的 FFmpeg 动态库附对应源码、补丁及构建脚本。\n'
    '允许为调试修改后的 LGPL 库而进行必要的应用逆向工程；可原位替换库，Mac 修改副本需重新本机签名。\n',encoding='utf8')
for name in ('COPYING.GPLv2', 'x264-COPYING'):
    shutil.copy2(binary_folder / name, license_dir / name)
shutil.copy2(manifest, license_dir / 'source-manifest.json')
(license_dir / 'SOURCES.txt').write_text(
    'FFmpeg 7.1-ulti360.1: GPL-2.0-or-later; external x264: GPL-2.0-or-later.\n'
    'Invoked as a separate executable. No restriction from the app license applies to these components.\n'
    'Exact source tarballs, build scripts, licenses, configuration and compiler records:\n'
    f'https://github.com/{REPO}/releases/tag/ffmpeg-{REV}\n'
    f'Archive: {record["source_archive"]}\nSHA256: {record["source_archive_sha256"]}\n'
    'FFmpeg 与 x264 以 GPL-2.0-or-later 发布，作为独立进程运行；应用许可不限制这些组件的授权。\n'
    '上方链接与同一应用 Release 提供对应源码、构建命令、许可与校验值。\n', encoding='utf8')
shutil.copy2(Path('THIRD-PARTY.md'), root / 'THIRD-PARTY.md')
if PLATFORM == 'macos':
    run('codesign', '--force', '--sign', '-', bins[0])
    run('codesign', '--force', '--sign', '-', engine)
record.update(packaged_ffmpeg_sha256=sha(bins[0]), replaced_ffmpeg_sha256=previous,
              distribution_revision=2, application_version='0.12.0',
              signing='codesign --force --sign -; outer app codesign --force --deep --sign -'
              if PLATFORM == 'macos' else 'unsigned Windows portable')
(license_dir / 'source-manifest.json').write_text(json.dumps(record, indent=2) + '\n')
build_path = root / 'BUILD-INFO.json'
build = json.loads(build_path.read_text())
build.update(distribution_revision=2, ffmpeg=record)
build['runtime_ffmpeg_source']=runtime
build_path.write_text(json.dumps(build, indent=2) + '\n')
ffmpeg = bins[0]
run(ffmpeg, '-version')
# Exercise the actual packaged worker, rather than just an unrelated FFmpeg executable.
sample = OUT / 'fixture.OSV'
run(ffmpeg, '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=size=1920x1920:rate=25',
    '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000', '-t', '1', '-map', '0:v',
    '-map', '0:v', '-map', '1:a', '-c:v', 'mpeg4', '-q:v', '12', '-c:a', 'aac', '-f', 'mp4', sample)
output = OUT / 'export'
output.mkdir()
work = output / 'work'
work.mkdir()
request = dict(mode='render', sources=[str(sample)], start=0, duration=1, stream=0,
    height=720, fov=100, quality='fast', acceleration='cpu', encoding='compact',
    roi=[[.15,.15],[.85,.15],[.85,.85],[.15,.85]], output_dir=str(output), work_dir=str(work))
result = run(engine, input=json.dumps(request) + '\n', text=True, capture_output=True, timeout=240)
events = [json.loads(line) for line in result.stdout.splitlines() if line.startswith('{')]
final = next((x for x in events if x.get('type') == 'result'), None)
if final is None or final.get('frames') != 25:
    raise RuntimeError('Packaged export failed: ' + result.stdout[-6000:] + result.stderr[-2000:])
run(ffmpeg, '-v', 'error', '-i', final['output'], '-f', 'null', '-')
record['packaged_engine_smoke'] = '1 second dual-lens OSV -> 25-frame 720p H264/AAC MP4; full decode passed'
record['smoke_result'] = {k: v for k, v in final.items() if k not in ('output', 'type')}
(OUT / f'distribution-{PLATFORM}.json').write_text(json.dumps(record, indent=2) + '\n')
if PLATFORM == 'macos':
    run('xattr', '-cr', app)
    run('codesign', '--force', '--deep', '--sign', '-', app)
    run('codesign', '--verify', '--deep', '--strict', app)
    app_zip.unlink()
    run('ditto', '-c', '-k', '--sequesterRsrc', '--keepParent', app, app_zip)
else:
    app_zip.unlink()
    with zipfile.ZipFile(app_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(app.rglob('*')):
            if file.is_file(): archive.write(file, file.relative_to(stage).as_posix())
app_zip.with_name(app_zip.name + '.sha256').write_text(sha(app_zip) + '  ' + app_zip.name + '\n')
source_zip.with_name(source_zip.name + '.sha256').write_text(sha(source_zip) + '  ' + source_zip.name + '\n')
runtime_source.with_name(runtime_source.name+'.sha256').write_text(sha(runtime_source)+'  '+runtime_source.name+'\n')
print(json.dumps({'app': app_zip.name, 'sha256': sha(app_zip), 'export_smoke': record['packaged_engine_smoke']}))
