<div align="center">

<img src="assets/icon.png" width="112" alt="ulti360 logo">

# ulti360

### One 360° camera on the sideline. A broadcast-style video of every match.

Turn a whole day of DJI 360 footage into clean 16:9 ultimate frisbee videos that follow the play,<br>with the score, the clock and a goal animation on screen. Runs entirely on your computer.

[![Release](https://img.shields.io/github/v/release/stevensun1005/ulti360-downloads?include_prereleases&sort=date&display_name=tag&label=release&color=78d6b3)](https://github.com/stevensun1005/ulti360-downloads/releases)
[![Windows](https://img.shields.io/badge/Windows-x64-0078D6?logo=windows&logoColor=white)](https://github.com/stevensun1005/ulti360-downloads/releases/download/v0.13.1-beta.1/ulti360-Windows.zip)
[![macOS](https://img.shields.io/badge/macOS-Apple%20Silicon-111111?logo=apple&logoColor=white)](https://github.com/stevensun1005/ulti360-downloads/releases/download/v0.13.1-beta.1/ulti360-macOS-arm64.zip)
[![Local](https://img.shields.io/badge/processing-100%25%20local-2ea44f)](#faq)
[![Language](https://img.shields.io/badge/UI-English%20%7C%20中文-555)](#faq)

**English** · [简体中文](README.zh-CN.md)

<h3>
  <a href="https://github.com/stevensun1005/ulti360-downloads/releases/download/v0.13.1-beta.1/ulti360-Windows.zip">⬇️ Download for Windows</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/stevensun1005/ulti360-downloads/releases/download/v0.13.1-beta.1/ulti360-macOS-arm64.zip">⬇️ Download for Mac</a>
</h3>

<img src="assets/demo.webp" width="880" alt="A real ulti360 export: the camera follows play and the scoreboard animates a goal">

<sub>A real export, unedited: ulti360 framed the 360° footage, followed play and added the scoreboard and the goal animation.</sub>

</div>

---

## ✨ Why ulti360

<table>
<tr>
<td width="33%" valign="top">

### 🎥 Set it and play
One raised 360° camera at midfield sees the whole field. No camera operator, no missed plays.

</td>
<td width="33%" valign="top">

### 🧭 Follows the action
ulti360 tracks where the players are and pans a natural, wide 16:9 view to follow them, with no dizzy zooming.

</td>
<td width="33%" valign="top">

### 🏆 Broadcast-style score
Team names, a match clock and a goal animation, from goals you confirm with one key.

</td>
</tr>
<tr>
<td valign="top">

### 📅 A whole day at once
Import up to 200 clips, mark where each match starts, and get one video per match.

</td>
<td valign="top">

### 🔒 Your footage stays yours
Everything runs on your computer. Nothing is uploaded, and no account is needed.

</td>
<td valign="top">

### 📊 Ready for team stats
Each export carries a match file with confirmed points for [UltiZ](#-whats-new-in-013), the team stats app.

</td>
</tr>
</table>

## 🔥 Before → after

<p align="center"><img src="assets/before-after.jpg" width="880" alt="The raw 360° lens next to the ulti360 16:9 export at the same moment"></p>

## 🚀 Your first match in 4 steps

| | Step | What you do |
|:-:|---|---|
| 1️⃣ | **Import** | Drop in the day's `.OSV` clips. They sort themselves by clip number. |
| 2️⃣ | **Mark matches** | Click the first clip of each match. The first two minutes are trimmed for tripod setup. |
| 3️⃣ | **Draw the field** | Click around the field on the lens that faces the game, then preview the 16:9 view. |
| 4️⃣ | **Export** | Pick a folder. Each match becomes its own MP4, ready for YouTube. |

<p align="center"><img src="assets/workspace.png" width="880" alt="ulti360 workspace: media library, field drawing on the 360° lens, inspector and match timeline"></p>

## 🆕 What's new in 0.13

- 🥏 **Goal review.** Jump to any moment and see eight whole-field stills, then add the goal with **A** or **B**. Suggested goals open with one click, so there is no more hunting for timestamps in another player.
- 📐 **Field calibration** *(optional)*. Click four corners and two end-zone lines to map the field in metres.
- 📊 **UltiZ match file.** Every export writes a `.ultiz.json` with confirmed points, scoring teams and the clock.
- 🗄️ **NAS-friendly** *(0.13.1)*. Clips on a mapped network drive keep their durations.

<p align="center"><img src="assets/goal-review.png" width="880" alt="Goal review with suggested goals, the goal list and goal marks on the timeline"></p>

## 📦 Download

| Platform | Version | Download | Install |
|---|---|---|---|
| **Windows** x64 | 0.13.1 Beta | [**ulti360-Windows.zip**](https://github.com/stevensun1005/ulti360-downloads/releases/download/v0.13.1-beta.1/ulti360-Windows.zip) | Extract the whole folder and open `ulti360.exe`. Keep `resources` beside it. |
| **Mac** Apple Silicon, macOS 13+ | 0.13.1 Beta | [**ulti360-macOS-arm64.zip**](https://github.com/stevensun1005/ulti360-downloads/releases/download/v0.13.1-beta.1/ulti360-macOS-arm64.zip) | Extract and move `ulti360.app` to `/Applications`. Intel Macs are not supported. |

Both apps are the same 0.13.1 release. No Python, Node or FFmpeg install is needed. Download the app ZIP, not GitHub's "Source code" archive, which holds only this page. The Mac app is ad-hoc signed, not notarized; if macOS blocks it, follow [Apple's steps for opening an app](https://support.apple.com/en-ca/102445). Windows may show a download warning for a new app.

## 🎬 Filming tips

- **Go high.** Raise the camera as high as you safely can at midfield. Height means fewer hidden players.
- **Start before the pull.** The first two minutes of a match are trimmed by default; set **Trim start** to `00:00:00` to keep them.
- **Contrasting jerseys** help score suggestions tell the teams apart: A is light, B is dark.
- **Try a short export first** to check coverage, sharpness and sound.

## <a id="faq"></a>❓ FAQ

<details><summary><b>Which cameras work?</b></summary><br>DJI 360 cameras that record dual-lens <code>.OSV</code> files. Mount the camera raised and fixed near the middle of a sideline.</details>
<details><summary><b>Is the score automatic?</b></summary><br>ulti360 <i>suggests</i> goals from player movement, and you confirm each one in Goal review before it appears on screen. It cannot see the disc or judge a legal catch, so the final score is always the one you reviewed.</details>
<details><summary><b>Does it track the disc?</b></summary><br>No. The view follows where the players are and how they move, which keeps the play in frame without seeing the disc itself.</details>
<details><summary><b>Do I need the internet or an account?</b></summary><br>No. Video processing runs entirely on your computer.</details>
<details><summary><b>What output can I get?</b></summary><br>1080p by default, plus 720p, 2K and 4K, at 25 or 50 fps. Each export has a small ulti360 watermark in the corner.</details>
<details><summary><b>Can I use it for my club or for paid work?</b></summary><br>Yes, from 0.13 on: the <a href="LICENSE-ulti360.md">ulti360 License</a> allows any use of official releases, including commercial. Redistribution, modification and removing the watermark need permission. 0.12.0 and earlier keep <a href="LICENSE.md">PolyForm Noncommercial</a>.</details>
<details><summary><b>Where do I report a problem?</b></summary><br><a href="https://github.com/stevensun1005/ulti360-downloads/issues">Open an issue</a> with the app version, your OS/chip, the error text, and clip numbers. Logs are at <code>%APPDATA%\ulti360\logs\ulti360.jsonl</code> (Windows) or <code>~/Library/Application Support/ulti360/logs/ulti360.jsonl</code> (Mac). Check them for paths or team names before sharing, and never post private footage.</details>

## 📜 Licence and third-party software

ulti360 0.13 and later: [ulti360 License](LICENSE-ulti360.md). 0.12.0 and earlier: [PolyForm Noncommercial 1.0.0](LICENSE.md). FFmpeg, x264, Electron, OpenCV, ONNX Runtime and YOLOX keep their own terms; every Release includes matching FFmpeg source and build records. See [third-party notices](THIRD-PARTY.md).

---

<div align="center">

**If ulti360 helps your team, ⭐ star this page and share your match video.**

<sub>Made for ultimate frisbee teams · Windows & Apple Silicon · English / 中文</sub>

</div>
