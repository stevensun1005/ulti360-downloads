"""SPDX-License-Identifier: GPL-2.0-or-later. Install replaceable LGPL Mac FFmpeg."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
import zipfile

def sha(path):
    with path.open('rb') as file:return hashlib.file_digest(file,'sha256').hexdigest()

def dependencies(path):
    result=subprocess.run(['otool','-L',str(path)],capture_output=True,text=True,check=True)
    # Exclude the LC_ID_DYLIB entry, which is not an imported dependency.
    return re.findall(r'^\s+(\S+)\s+\(',result.stdout,re.M)

def install_shared(engine,archive,manifest):
    internal=engine/'_internal'
    def imports(path):
        return {Path(d).name for d in dependencies(path) if not d.startswith(('/usr/lib/','/System/Library/'))}
    old_dylibs={p.name:p for p in internal.rglob('*.dylib') if not p.is_symlink()}
    old_graph={name:imports(path) for name,path in old_dylibs.items()}
    with zipfile.ZipFile(archive) as bundle:
        for name,expected in manifest['libraries'].items():
            value=bundle.read(name)
            if hashlib.sha256(value).hexdigest()!=expected:raise RuntimeError('LGPL library checksum mismatch')
            target=internal/name
            target.write_bytes(value)
            target.chmod(0o755)
        (internal/'FFmpeg-LGPLv2.1.txt').write_bytes(bundle.read('COPYING.LGPLv2.1'))
    # Remove the old GPL FFmpeg and only its now-unreferenced library dependencies.
    dylibs={p.name:p for p in internal.rglob('*.dylib') if not p.is_symlink()}
    graph={name:imports(path) for name,path in dylibs.items()}
    old_ffmpeg={name for name in old_dylibs if name.startswith(('libavcodec.','libavformat.','libavutil.',
        'libavdevice.','libavfilter.','libswscale.','libswresample.','libpostproc.'))}
    old_closure=set(old_ffmpeg)
    pending=list(old_ffmpeg)
    # Also identify previous Homebrew optional codecs that can remain from PyInstaller's dependency closure.
    # They are candidates only; a surviving OpenCV/NumPy/ONNX import always retains its dependency.
    while pending:
        for name in old_graph.get(pending.pop(),set()):
            if name in dylibs and name not in old_closure:old_closure.add(name);pending.append(name)
    roots=set(manifest['libraries'])
    for path in internal.rglob('*.so'):roots.update(imports(path))
    roots.update(n for n,p in dylibs.items() if n.startswith(('libpython','libonnxruntime','libomp','libiomp')) or 'onnxruntime' in p.parts)
    # Preserve dependency closures of all unrelated dylibs as well.
    roots.update(set(dylibs)-old_closure)
    keep=set(roots);pending=list(roots)
    while pending:
        for name in graph.get(pending.pop(),set()):
            if name not in keep:keep.add(name);pending.append(name)
    removed=[]
    for name in sorted(old_closure-keep):
        if name in dylibs:dylibs[name].unlink();removed.append(name)
    for name in old_ffmpeg:
        if name not in manifest['libraries'] and name in dylibs and dylibs[name].exists():
            raise RuntimeError('An old FFmpeg library is still required: '+name)
    return {'removed_unused_libraries':removed,'libraries':{n:sha(internal/n) for n in manifest['libraries']}}
