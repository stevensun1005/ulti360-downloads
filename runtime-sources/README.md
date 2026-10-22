# Runtime FFmpeg sources / 运行时 FFmpeg 源码

## English

The app has three FFmpeg consumers. The separate export executable uses the source package described in [../ffmpeg](../ffmpeg/README.md). This folder covers Electron's dynamically linked playback library and OpenCV's video-reading libraries.

- Electron **44.4.5** → Chromium **152.0.7977.130** → FFmpeg commit **2b68d2babae73714846961fb0ee47e3b3d2e39a9**. The source ZIP contains Chromium FFmpeg's source/configuration, Chromium's build directory, and the Electron source tree including DEPS, build/args/release.gn, patches/ffmpeg and patch/build scripts. Use the release build arguments, `is_component_ffmpeg=true`, and the matching native target (`target_os="win" target_cpu="x64"` or `target_os="mac" target_cpu="arm64"`). Electron's separate ffmpeg.gn target disables proprietary codecs and is a different build profile from its ordinary runtime. Follow the included Electron source's build instructions to obtain standard toolchains and the remaining Chromium checkout. No ulti360 source is required to rebuild the library.
- OpenCV **5.0.0.93 Windows**: the upstream source snapshot includes the byte-identical videoio DLL, FFmpeg/libvpx/AOM source archives, wrapper source and Docker/MinGW recipes. Extract opencv-ffmpeg-windows-sources.tar.gz and follow ffmpeg/build_via_docker.sh or ffmpeg/build_videoio_plugin.sh with its supplied sources. The DLL is dynamically loaded and replaceable; any separately obtained OpenH264 runtime has its own terms.
- OpenCV **Mac**: the app replaces Homebrew's GPL-enabled libraries with our LGPL-2.1-or-later FFmpeg **7.1.1** shared libraries, without optional external codecs. On native Apple Silicon with Python 3.13 and Xcode command-line tools, extract the runtime corresponding-source ZIP, copy its archives/ files to runtime-build/archives/, then run `python build/build.py`. Its source manifest records exact archives, commands, compiler and dependency information. install.py copies matching libraries and removes only obsolete dependencies no surviving application import requires. Signing changes bytes; it does not change compiled source.

Gitiles gzip output can differ between requests for the same commit. sources.json therefore retains the original Gitiles URLs and pins immutable copies hosted in the upstream-inputs Release. These are source archives, not private app code. The app's noncommercial license does not restrict FFmpeg/library grants. License texts remain in each original archive. LGPL libraries can be replaced; reverse engineering needed to debug their modifications is permitted. Mac modified copies require local re-signing.

## 中文

应用中有三处使用 FFmpeg。独立导出程序的源码见 [../ffmpeg](../ffmpeg/README.md)；本目录覆盖 Electron 动态播放库与 OpenCV 视频读取库。

- Electron **44.4.5** → Chromium **152.0.7977.130** → FFmpeg 提交 **2b68d2babae73714846961fb0ee47e3b3d2e39a9**。源码包包含 Chromium FFmpeg 源码/配置、Chromium build 目录、Electron 源码中的 DEPS、build/args/release.gn、patches/ffmpeg 和补丁/构建脚本。使用发布参数、`is_component_ffmpeg=true` 及对应原生目标（`target_os="win" target_cpu="x64"` 或 `target_os="mac" target_cpu="arm64"`）。Electron 独立 ffmpeg.gn 目标关闭专有编解码，与正常运行时发布配置不同。按包内 Electron 构建文档准备标准工具链及其余 Chromium 检出；重建该库不需要 ulti360 私有源码。
- OpenCV **5.0.0.93 Windows**：上游源码快照包含与实际 videoio DLL 字节相同的库、FFmpeg/libvpx/AOM 源码包、封装层和 Docker/MinGW 构建脚本。解压 opencv-ffmpeg-windows-sources.tar.gz，按 ffmpeg/build_via_docker.sh 或 ffmpeg/build_videoio_plugin.sh 使用随包源码构建。DLL 动态加载、允许替换；另行获取的 OpenH264 运行时适用其自身条款。
- OpenCV **Mac**：应用使用自行构建的 LGPL-2.1-or-later **FFmpeg 7.1.1** 动态库替换启用 GPL 的 Homebrew 库，不启用可选外部编解码库。在原生 M 芯片、Python 3.13 与 Xcode 命令行工具环境下，解压运行时对应源码包，把 archives/ 中的文件复制到 runtime-build/archives/ 后运行 `python build/build.py`。清单记录源码、命令、编译器及依赖。install.py 安装匹配的库，仅移除现存应用导入不再需要的旧依赖。签名改变字节，不改变编译源码。

相同提交的 Gitiles gzip 输出字节可能变化，因此 sources.json 保留原始来源，同时锁定 upstream-inputs Release 中保存的源码压缩包。它们不含私有应用代码；应用非商业许可不限制库本身的授权，原许可保存在各上游源码内。LGPL 库允许替换，并允许为调试其修改所必需的应用逆向工程；修改后的 Mac 副本需要本机重新签名。
