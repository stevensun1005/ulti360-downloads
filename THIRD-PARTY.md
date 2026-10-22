# Third-Party Components

## English

The noncommercial license for ulti360's project-owned code and documentation is in the [project license](LICENSE.md). Third-party code, models, and tools listed here retain their own terms; the project license does not change or restrict those grants.

### License files

Each platform gathers notices from win/licenses/ or mac/licenses/ and retains notices bundled in its runtime. Third-party Markdown notices receive a bilingual cover page while their original bytes are preserved in an adjacent .original.txt file; the translation does not replace the license. A platform's notice folder may include copied notices for the other platform, so inspect the binaries actually shipped in each package.

### FFmpeg redistribution

The current Windows portable package bundles FFmpeg 7.1 Gyan essentials as a static executable via imageio-ffmpeg. Its inspected version output includes --enable-gpl, --enable-version3, and --enable-libx264, and the app invokes it as a separate process. The September 24, 2026 native Mac build copied an FFmpeg 7.1 arm64 executable from imageio-ffmpeg 0.6.0; `ffmpeg -version` reports --enable-gpl and --enable-libx264, and `ffmpeg -L` states GPL version 2 or later. Complete corresponding source and build configuration for this binary have not been assembled with this project. Codec checks are not a license review.

Public distribution of an executable containing FFmpeg, including binaries in a public GitHub repository, requires meeting applicable GPL and third-party library license obligations and providing complete corresponding source, build configuration, licenses, and required notices matching the **actual binary distributed**. [FFmpeg's official legal guidance](https://ffmpeg.org/legal.html) recommends hosting corresponding source alongside the binary. Links to the FFmpeg homepage, generic release source, or a third-party build repository alone do not establish that corresponding source has been delivered. Review each platform before release; this document does not claim compliance or assume the repository's visibility.

### Sources and versions

| Component | License and notes |
|---|---|
| [YOLOX-S](https://github.com/Megvii-BaseDetection/YOLOX) | Apache 2.0; the [official model](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.onnx) has SHA-256 c5c2d13e59ae883e6af3b45daea64af4833a4951c92d116ec270d9ddbe998063. |
| [Python 3.13](https://www.python.org/downloads/) | PSF license and bundled notices. |
| [NumPy 2.5.3](https://github.com/numpy/numpy) | BSD-style license and third-party notices. |
| [OpenCV headless 5.0.0.93](https://github.com/opencv/opencv-python) | OpenCV and included third-party licenses. |
| [imageio-ffmpeg 0.6.0](https://github.com/imageio/imageio-ffmpeg) | The Python package has a BSD-style license; its FFmpeg executable has separate obligations. |
| [Windows FFmpeg 7.1](https://www.gyan.dev/ffmpeg/builds/) | Gyan static build; the [FFmpeg source](https://ffmpeg.org/releases/ffmpeg-7.1.tar.xz), [build repository](https://github.com/GyanD/codexffmpeg), and win/licenses/FFmpeg-GPLv3.txt support review, but these links alone do not prove a complete corresponding-source delivery. |
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

当前 Windows 便携包通过 imageio-ffmpeg 附带 FFmpeg 7.1 Gyan essentials 静态可执行文件。已检查该文件的版本信息：启用了 --enable-gpl、--enable-version3、--enable-libx264 等选项，并以独立进程调用。2026 年 9 月 24 日的 Mac 本机构建从原生 imageio-ffmpeg 0.6.0 包中复制了 FFmpeg 7.1 arm64 可执行文件；`ffmpeg -version` 显示 --enable-gpl 与 --enable-libx264，`ffmpeg -L` 声明 GPL 第 2 版或以后版本。该二进制的完整对应源码和构建配置尚未随本项目备齐。编解码能力检查不是许可审查。

若向公众分发包含 FFmpeg 的可执行包（包括公开 GitHub 仓库中的二进制），需要同时履行适用的 GPL 与第三方库许可义务，准备与**实际所分发二进制**匹配的完整对应源码、构建配置、许可与必要通知。[FFmpeg 官方法律说明](https://ffmpeg.org/legal.html)建议在二进制同一下载位置提供对应源码。仅列出 FFmpeg 首页、通用版本源码或第三方构建仓库的链接，不等于已经完成对应源码交付。发布前逐个平台核对；本文件不声称已完成该工作，也不假定仓库是公开或私有。

### 来源和版本

| 组件 | 许可与说明 |
|---|---|
| [YOLOX-S](https://github.com/Megvii-BaseDetection/YOLOX) | Apache 2.0；[官方模型](https://github.com/Megvii-BaseDetection/YOLOX/releases/download/0.1.1rc0/yolox_s.onnx) 的 SHA-256 为 c5c2d13e59ae883e6af3b45daea64af4833a4951c92d116ec270d9ddbe998063。 |
| [Python 3.13](https://www.python.org/downloads/) | PSF 许可及随附通知。 |
| [NumPy 2.5.3](https://github.com/numpy/numpy) | BSD 类许可及其第三方通知。 |
| [OpenCV headless 5.0.0.93](https://github.com/opencv/opencv-python) | OpenCV 与包含的第三方许可。 |
| [imageio-ffmpeg 0.6.0](https://github.com/imageio/imageio-ffmpeg) | Python 包采用 BSD 类许可；其中的 FFmpeg 可执行文件另有许可要求。 |
| [Windows FFmpeg 7.1](https://www.gyan.dev/ffmpeg/builds/) | Gyan 静态版；[FFmpeg 源码](https://ffmpeg.org/releases/ffmpeg-7.1.tar.xz)、[构建仓库](https://github.com/GyanD/codexffmpeg)及 win/licenses/FFmpeg-GPLv3.txt 可供核对，不能单凭这些链接断言对应源码齐备。 |
| [PyInstaller 6.22.3](https://github.com/pyinstaller/pyinstaller) | GPL 与 bootloader 例外，见平台许可目录。 |
| [Electron 44.4.5](https://github.com/electron/electron/releases/tag/v44.4.5) | MIT；便携包保留 Electron LICENSE 和 LICENSES.chromium.html。 |
| [ONNX Runtime DirectML](https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html) 与 [PyOpenCL](https://documen.tician.de/pyopencl/) | Windows GPU 路径使用；相应许可和运行依赖记录在 win/licenses/。 |
| [ONNX Runtime Core ML](https://onnxruntime.ai/docs/execution-providers/CoreML-ExecutionProvider.html) | Mac 自动人员识别使用；许可及第三方通知位于 mac/licenses/onnxruntime/ 和随包运行时。 |

比赛原始素材未随项目提供；视频处理在本机进行。本项目不表示与 DJI、Blackmagic Design 或 Megvii 有合作关系。
