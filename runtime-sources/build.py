"""SPDX-License-Identifier: GPL-2.0-or-later. Runtime FFmpeg source delivery."""
from pathlib import Path
import ctypes
import hashlib
import json
import re
import shutil
import subprocess
import tarfile
import urllib.request
import zipfile

HERE = Path(__file__).resolve().parent
LOCK = json.loads((HERE / 'sources.json').read_text())
WORK = Path('runtime-build').resolve()
OUT = Path('runtime-dist').resolve()
WORK.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

def sha(path):
    with path.open('rb') as source: return hashlib.file_digest(source,'sha256').hexdigest()

def run(*args, **kwargs):
    result = subprocess.run([str(x) for x in args], text=True, capture_output=True, **kwargs)
    if result.returncode:
        raise RuntimeError('Command failed: ' + ' '.join(map(str,args)) + '\n' + result.stdout[-2000:] + result.stderr[-4000:])
    return result.stdout + result.stderr

archives = WORK / 'archives'
archives.mkdir(exist_ok=True)
for item in LOCK['sources']:
    target = archives / item['name']
    if not target.exists():
        with urllib.request.urlopen(item['url'],timeout=180) as response,target.open('wb') as out:
            shutil.copyfileobj(response,out)
    if sha(target) != item['sha256']: raise RuntimeError('Source hash mismatch: ' + target.name)

with tarfile.open(archives / 'ffmpeg-7.1.1.tar.xz') as archive:
    archive.extractall(WORK,filter='data')
source = WORK / 'ffmpeg-7.1.1'
prefix = WORK / 'prefix'
flags = ['--prefix='+str(prefix),'--disable-autodetect','--disable-gpl','--disable-version3',
    '--disable-nonfree','--enable-shared','--disable-static','--disable-programs','--disable-doc',
    '--disable-debug','--disable-network','--arch=arm64','--cc=clang','--install-name-dir=@rpath',
    '--enable-videotoolbox','--enable-audiotoolbox','--extra-cflags=-mmacosx-version-min=13.0',
    '--extra-ldflags=-mmacosx-version-min=13.0']
records = WORK / 'records';records.mkdir(exist_ok=True)
(records/'configure-command.json').write_text(json.dumps(['./configure',*flags],indent=2)+'\n')
(records/'configure-output.txt').write_text(run('./configure',*flags,cwd=source))
print('Compiling LGPL shared libraries',flush=True)
(records/'make-output.txt').write_text(run('make','-j3',cwd=source))
run('make','install',cwd=source)
libraries = {p.name:p for p in (prefix/'lib').glob('*.dylib') if not p.is_symlink()}
# Use loader-relative dependencies so the distributed library remains replaceable.
for name,file in libraries.items():
    for dependency in re.findall(r'^\s+(\S+)\s+\(',run('otool','-L',file),re.M):
        base = Path(dependency).name
        if dependency.startswith(('/usr/lib/','/System/Library/')):continue
        if dependency.startswith('@rpath/') or str(prefix) in dependency:
            canonical = (prefix/'lib'/base).resolve().name
            if canonical not in libraries: raise RuntimeError('Unknown shared dependency: '+dependency)
            if base != name:run('install_name_tool','-change',dependency,'@loader_path/'+canonical,file)
    run('codesign','--force','--sign','-',file)
dependencies = '\n'.join(run('otool','-L',p) for p in libraries.values())
(records/'dependencies.txt').write_text(dependencies)
(records/'compiler.txt').write_text(run('clang','-v'))
codec = ctypes.CDLL(str(next(p for n,p in libraries.items() if n.startswith('libavcodec.'))))
codec.avcodec_configuration.restype=ctypes.c_char_p
configuration = codec.avcodec_configuration().decode()
if '--enable-gpl' in configuration or '--enable-version3' in configuration or '--enable-lib' in configuration:
    raise RuntimeError('Unexpected restricted codec library configuration')
(records/'runtime-configuration.txt').write_text(configuration)
manifest = dict(schema=1,revision=LOCK['revision'],ffmpeg_version='7.1.1',license='LGPL-2.1-or-later',
    libraries={n:sha(p) for n,p in libraries.items()},source_inputs=LOCK)
source_name='runtime-ffmpeg-corresponding-source-'+LOCK['revision']+'.zip'
with zipfile.ZipFile(OUT/source_name,'w',zipfile.ZIP_DEFLATED) as bundle:
    for file in archives.iterdir():bundle.write(file,'archives/'+file.name)
    for file in HERE.iterdir():
        if file.is_file():bundle.write(file,'build/'+file.name)
    for file in records.iterdir():bundle.write(file,'build-record/'+file.name)
    for name in ('COPYING.LGPLv2.1','COPYING.LGPLv3','LICENSE.md'):
        bundle.write(source/name,'licenses/ffmpeg/'+name)
    bundle.writestr('source-manifest.json',json.dumps(manifest,indent=2)+'\n')
manifest.update(source_archive=source_name,source_archive_sha256=sha(OUT/source_name))
(OUT/'runtime-ffmpeg-source.json').write_text(json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT/'ffmpeg-lgpl-macos-arm64.zip','w',zipfile.ZIP_DEFLATED) as bundle:
    for name,file in libraries.items():bundle.write(file,name)
    bundle.write(source/'COPYING.LGPLv2.1','COPYING.LGPLv2.1')
    bundle.write(OUT/'runtime-ffmpeg-source.json','runtime-ffmpeg-source.json')
for file in list(OUT.iterdir()):
    file.with_name(file.name+'.sha256').write_text(sha(file)+'  '+file.name+'\n')
print(json.dumps(manifest,indent=2))
