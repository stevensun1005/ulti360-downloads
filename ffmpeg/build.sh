#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-2.0-or-later
set -euo pipefail
platform="$1"
recipe="$(cd "$(dirname "$0")" && pwd)"
python "$recipe/source_tools.py" fetch
work="$PWD/ffmpeg-build"
prefix="$work/prefix"
export PKG_CONFIG_PATH="$prefix/lib/pkgconfig"
export MACOSX_DEPLOYMENT_TARGET=13.0
mkdir -p "$prefix" "$PWD/ffmpeg-dist"
cd "$work/x264"
x264_flags=(--prefix="$prefix" --enable-static --disable-cli --disable-opencl --enable-pic)
if [[ "$platform" == windows ]]; then
  export LDFLAGS=-static
fi
./configure "${x264_flags[@]}"
make -j3
make install
cd "$work/ffmpeg"
flags=(--prefix="$prefix" --extra-version=ulti360.1 --disable-autodetect
  --enable-gpl --enable-libx264 --enable-static --disable-shared --disable-debug
  --disable-doc --disable-ffplay --disable-ffprobe --disable-network
  --pkg-config-flags=--static --extra-cflags="-I$prefix/include"
  --extra-ldflags="-L$prefix/lib")
if [[ "$platform" == windows ]]; then
  flags+=(--target-os=mingw32 --arch=x86_64 --cc=gcc --enable-w32threads
    --disable-pthreads --enable-d3d11va --enable-dxva2 --extra-ldflags=-static)
elif [[ "$platform" == macos ]]; then
  flags+=(--arch=arm64 --cc=clang --enable-videotoolbox --enable-audiotoolbox
    --extra-cflags=-mmacosx-version-min=13.0 --extra-ldflags=-mmacosx-version-min=13.0)
else
  exit 2
fi
printf '%q ' ./configure "${flags[@]}" > "$work/configure-command.txt"
printf '\n' >> "$work/configure-command.txt"
./configure "${flags[@]}"
make -j3
cd ../..
python "$recipe/source_tools.py" finalize "$platform"
