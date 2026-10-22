# ulti360 0.12.0 Beta 2

## English

Windows x64 and Apple Silicon/macOS 13+. This distribution repair replaces the old FFmpeg executables with native FFmpeg 7.1-ulti360.1 built from locked FFmpeg/x264 source. App and tracking behavior remain 0.12.0. Download the app ZIP for your platform; the ffmpeg-corresponding-source ZIP contains third-party source and build material, not the app.

Both native packages must pass a real packaged-worker test: synthetic dual-lens OSV to 25-frame 720p H.264/AAC MP4, followed by full decode. The test reports record actual encoders and source/signing hashes. Original 0.12.0 native GUI/layout checks remain recorded; this repair does not add a full-match accuracy qualification. Scores require human review.

Mac is ad-hoc signed, not notarized. Follow Apple's per-app opening process for a trusted download; Intel Macs are unsupported. Windows is a complete portable folder: extract it and keep resources beside ulti360.exe. Project code is PolyForm Noncommercial; bundled third-party components retain their own terms. Exact FFmpeg/x264 source, GPL licenses, scripts and configuration are supplied beside both app ZIPs and in the separate FFmpeg build Release.

## 中文

适用于 Windows x64 与 Apple Silicon/macOS 13+。此次分发修订把旧 FFmpeg 替换为从锁定 FFmpeg/x264 源码原生构建的 7.1-ulti360.1，应用与跟拍行为仍为 0.12.0。下载对应平台的应用 ZIP；ffmpeg-corresponding-source ZIP 是第三方源码和构建材料，不是软件安装包。

两平台均须通过实际打包引擎测试：双镜头模拟 OSV 导出 25 帧 720p H.264/AAC MP4，并完整解码；报告记录实际编码器、源码和签名校验值。原 0.12.0 的本机界面和布局检查记录仍适用；此次修订没有新增整场准确率验证，比分仍需人工复核。

Mac 为临时签名、未公证，可信下载被拦截时按 Apple 单个应用打开流程操作，不支持 Intel Mac。Windows 解压完整目录，保留 resources 后打开 ulti360.exe。项目自有代码采用 PolyForm Noncommercial，第三方组件保留各自许可。FFmpeg/x264 对应源码、GPL 许可、脚本与配置在两平台软件 ZIP 旁及单独 FFmpeg 构建 Release 中提供。
