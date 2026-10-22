# Third-Party Components

## English

The noncommercial license for ulti360's project-owned code and documentation is in the [project license](LICENSE.md). Third-party code, models, and tools listed here retain their own terms; the project license does not change or restrict those grants.

### License files

Each platform gathers notices from win/licenses/ or mac/licenses/ and retains notices bundled in its runtime. Third-party Markdown notices receive a bilingual cover page while their original bytes are preserved in an adjacent .original.txt file; the translation does not replace the license. A platform's notice folder may include copied notices for the other platform, so inspect the binaries actually shipped in each package.

### FFmpeg redistribution

Distribution revision 2 uses our native FFmpeg **7.1-ulti360.1** builds on Windows x64 and Apple Silicon. They replace the earlier imageio wheel executables. The only external codec library enabled is x264; both FFmpeg and x264 are supplied under GPL-2.0-or-later. FFmpeg runs as a separate process. The app's noncommercial license does not restrict these GPL components.

Each app Release provides a platform-specific **ffmpeg-corresponding-source** ZIP alongside the app ZIP. It contains the exact FFmpeg 7.1 and pinned x264 source archives, their SHA-256 values, unmodified license texts, configure command, build scripts, compiler and dependency records. The [FFmpeg build Release](https://github.com/stevensun1005/ulti360-downloads/releases/tag/ffmpeg-7.1-ulti360.1) also hosts the source and raw binaries; [public build recipes](https://github.com/stevensun1005/ulti360-downloads/tree/main/ffmpeg) document reproduction. The package's resources/licenses/ffmpeg-ulti360/source-manifest.json links the shipped executable to its corresponding source. On Mac, both the pre-signing and ad-hoc-signed hashes are recorded because signing changes executable bytes.

No optional external codecs other than x264 are linked. Native OS libraries and compiler runtimes are recorded as system/toolchain dependencies, with runtime notices retained. Historical notice copies can remain in the license folder; the manifest identifies the actual FFmpeg used. See [FFmpeg legal guidance](https://ffmpeg.org/legal.html). Source-delivery and media checks do not constitute a legal certification or a qualification of every match-export workload.

### Sources and versions

| Component | License and notes |
|---|---|
| [YOLOX-S](https://github.com/Megvii-BaseDetection/YOLOX) | Apache 2.0; the [official model](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.onnx) has SHA-256 c5c2d13e59ae883e6af3b45daea64af4833a4951c92d116ec270d9ddbe998063. |
| [Python 3.13](https://www.python.org/downloads/) | PSF license and bundled notices. |
| [NumPy 2.5.3](https://github.com/numpy/numpy) | BSD-style license and third-party notices. |
| [OpenCV headless 5.0.0.93](https://github.com/opencv/opencv-python) | OpenCV and included third-party licenses. |
| [imageio-ffmpeg 0.6.0](https://github.com/imageio/imageio-ffmpeg) | The Python package has a BSD-style license; its FFmpeg executable has separate obligations. |
| [FFmpeg 7.1-ulti360.1](https://github.com/stevensun1005/ulti360-downloads/releases/tag/ffmpeg-7.1-ulti360.1) | GPL-2.0-or-later; native FFmpeg plus x264, exact source and build records supplied alongside binaries. |
| [PyInstaller 6.22.3](https://github.com/pyinstaller/pyinstaller) | GPL with bootloader exception; see platform notice folders. |
| [Electron 44.4.5](https://github.com/electron/electron/releases/tag/v44.4.5) | MIT; the portable package retains Electron LICENSE and LICENSES.chromium.html. |
| [ONNX Runtime DirectML](https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html) and [PyOpenCL](https://documen.tician.de/pyopencl/) | Used by the Windows GPU path; associated notices and runtime dependencies are recorded in win/licenses/. |
| [ONNX Runtime Core ML](https://onnxruntime.ai/docs/execution-providers/CoreML-ExecutionProvider.html) | Used by Mac automatic person detection; license and third-party notices are in mac/licenses/onnxruntime/ and the bundled runtime. |

Original match footage is not included with the project; video processing runs locally. This project does not imply an affiliation with DJI, Blackmagic Design, or Megvii.

## 中文

ulti360 项目自有代码和文档的非商业许可见[项目许可证](LICENSE.md)；本页列出的第三方代码、模型和工具继续适用各自许可，项目许可证不改变或限制这些第三方授权。

### 许可文件

两个平台从各自的 win/licenses/ 或 mac/licenses/ 收集许可文本，并把实际运行时自带的通知文件保留在发布包内。第三方原本为 Markdown 的许可说明以双语封面解释，原文字节保存在相邻的 .original.txt 文件；翻译不替代原许可。两侧许可目录可能包含另一平台的通知副本，实际随包二进制仍须分别核对。

### FFmpeg 再分发

分发修订 2 在 Windows x64 与 Apple Silicon 上使用自行构建的 **FFmpeg 7.1-ulti360.1**，替换旧 imageio 安装包中的可执行文件。唯一启用的外部编解码库为 x264；FFmpeg 与 x264 按 GPL-2.0-or-later 提供，并以独立进程运行。应用的非商业许可不限制这些 GPL 组件的授权。

每次应用 Release 都在软件 ZIP 旁提供对应平台的 **ffmpeg-corresponding-source** 源码包，包含实际使用的 FFmpeg 7.1 与锁定提交的 x264 源码压缩包、SHA-256、许可原文、configure 命令、构建脚本、编译器和依赖记录。[FFmpeg 构建 Release](https://github.com/stevensun1005/ulti360-downloads/releases/tag/ffmpeg-7.1-ulti360.1) 同时保留源码与原始二进制；[公开构建脚本](https://github.com/stevensun1005/ulti360-downloads/tree/main/ffmpeg) 说明如何重建。安装包 resources/licenses/ffmpeg-ulti360/source-manifest.json 关联实际程序与对应源码。Mac 临时签名改变二进制字节，因此同时记录签名前后的校验值。

不链接 x264 之外的可选外部编解码库；系统库与编译运行时记录在依赖清单内，保留运行时通知。许可目录可能留有历史通知副本，实际 FFmpeg 以清单为准。参见 [FFmpeg 官方说明](https://ffmpeg.org/legal.html)。源码交付与媒体测试不等于法律认证，也不代表完成所有整场导出工作负载验证。

### 来源和版本

| 组件 | 许可与说明 |
|---|---|
| [YOLOX-S](https://github.com/Megvii-BaseDetection/YOLOX) | Apache 2.0；[官方模型](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.onnx) 的 SHA-256 为 c5c2d13e59ae883e6af3b45daea64af4833a4951c92d116ec270d9ddbe998063。 |
| [Python 3.13](https://www.python.org/downloads/) | PSF 许可及随附通知。 |
| [NumPy 2.5.3](https://github.com/numpy/numpy) | BSD 类许可及其第三方通知。 |
| [OpenCV headless 5.0.0.93](https://github.com/opencv/opencv-python) | OpenCV 与包含的第三方许可。 |
| [imageio-ffmpeg 0.6.0](https://github.com/imageio/imageio-ffmpeg) | Python 包采用 BSD 类许可；其中的 FFmpeg 可执行文件另有许可要求。 |
| [FFmpeg 7.1-ulti360.1](https://github.com/stevensun1005/ulti360-downloads/releases/tag/ffmpeg-7.1-ulti360.1) | GPL-2.0-or-later；原生 FFmpeg 与 x264，对应源码及构建记录随软件提供。 |
| [PyInstaller 6.22.3](https://github.com/pyinstaller/pyinstaller) | GPL 与 bootloader 例外，见平台许可目录。 |
| [Electron 44.4.5](https://github.com/electron/electron/releases/tag/v44.4.5) | MIT；便携包保留 Electron LICENSE 和 LICENSES.chromium.html。 |
| [ONNX Runtime DirectML](https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html) 与 [PyOpenCL](https://documen.tician.de/pyopencl/) | Windows GPU 路径使用；相应许可和运行依赖记录在 win/licenses/。 |
| [ONNX Runtime Core ML](https://onnxruntime.ai/docs/execution-providers/CoreML-ExecutionProvider.html) | Mac 自动人员识别使用；许可及第三方通知位于 mac/licenses/onnxruntime/ 和随包运行时。 |

比赛原始素材未随项目提供；视频处理在本机进行。本项目不表示与 DJI、Blackmagic Design 或 Megvii 有合作关系。
