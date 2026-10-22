# FFmpeg source build / FFmpeg 源码构建

## English

These build scripts are GPL-2.0-or-later. `sources.json` locks FFmpeg 7.1 and x264 to downloadable source archives and SHA-256 values. Upstream source/license texts remain unchanged. FFmpeg is a separate executable; the ulti360 project license does not restrict its GPL grants.

Requirements: Apple Silicon with Xcode command-line tools, or Windows with MSYS2 UCRT64 GCC, make, pkgconf, NASM and Python. Run `bash ffmpeg/build.sh macos` or `bash ffmpeg/build.sh windows` from this repository's root. Mac deployment target is macOS 13.0. The GitHub workflow runs both native platforms.

Only x264 is enabled as an external FFmpeg library. Autodetection and network input are disabled; OS-provided libraries/frameworks and standard toolchain runtime are recorded separately. Native codecs/filters and x264 remain available for local OSV probe, preview, extraction, export and audio. Runtime imports are inspected to reject untracked non-system libraries.

Each platform emits a binary ZIP, a corresponding-source ZIP, a manifest and checksums in `ffmpeg-dist/`. The source ZIP contains the exact unmodified source archives, these scripts, configuration command, compiler information, binary build/license output, dependency inspection and licenses. Extract it, run `bash build/build.sh <platform>` from its root to rebuild. Source archive hashes and binary hashes identify the delivered pair; byte-identical reproduction across different compilers/signatures is not claimed.

Apple signing of the delivered application is recorded separately and does not change the compiled source. The Mac app remains ad-hoc signed until separately signed/notarized with Developer ID. Functional, signing and source-delivery checks are distinct from legal certification or sports-recognition accuracy.

## 中文

本构建脚本采用 GPL-2.0-or-later。`sources.json` 锁定 FFmpeg 7.1 与 x264 的源码包和 SHA-256；上游源码及许可原文不变。FFmpeg 作为独立进程运行，ulti360 项目许可不限制其 GPL 授权。

需要 M 芯片 Mac 和 Xcode 命令行工具，或安装 MSYS2 UCRT64 GCC、make、pkgconf、NASM、Python 的 Windows。在仓库根目录运行 `bash ffmpeg/build.sh macos` 或 `bash ffmpeg/build.sh windows`；Mac 最低部署目标为 macOS 13.0。GitHub 工作流分别在两平台原生执行。

外部 FFmpeg 库只启用 x264，关闭自动探测与网络输入，单独记录操作系统库/框架及标准工具链运行时。保留本机 OSV 读取、预览、抽帧、导出和音频所需的内置编解码/滤镜及 x264；检查运行依赖，拒绝未记录的非系统库。

每个平台在 `ffmpeg-dist/` 输出二进制 ZIP、对应源码 ZIP、清单与校验文件。源码 ZIP 包含精确原始源码包、脚本、配置命令、编译器信息、二进制构建/许可输出、依赖检查和许可。解压后在包根目录运行 `bash build/build.sh <platform>` 可重建。源码与二进制哈希对应交付版本，不声称不同编译器/签名下字节完全一致。

Apple 签名处理另行记录，不改变编译源码。Mac 软件在完成 Developer ID 签名/公证前仍属临时本机签名。功能、签名及源码交付检查不等于法律认证或比赛识别准确率。
