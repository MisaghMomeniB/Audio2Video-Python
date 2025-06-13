# 🎞️ Audio2Video (Python)

A lightweight Python tool to **merge audio and video streams** into a synchronized MP4. Ideal for generating narrated videos, podcasts with visuals, or data visualizations with voiceovers.

---

## 📋 Table of Contents

1. [Overview](#overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Code Structure](#code-structure)  
7. [Implementation Details](#implementation-details)  
8. [Enhancement Ideas](#enhancement-ideas)  
9. [Contributing](#contributing)  
10. [License](#license)

---

## 💡 Overview

Audio2Video is a small, focused Python script (or module) that uses `ffmpeg-python` to combine a silent video (or image sequence) with an audio track into a single video file. Perfect for generating narrated visual content programmatically.

---

## ✅ Features

- 🎵 Adds an audio file (e.g., `.wav` or `.mp3`) to a silent video or image sequence  
- 🛠️ Supports custom frame rate, resolution, and audio sync  
- 💾 Outputs a finalized `.mp4` with embedded audio  
- 🔁 Can be used as CLI or imported as a Python module

---

## 🛠️ Prerequisites

- Python **3.7+**  
- [ffmpeg](https://ffmpeg.org/) installed and accessible in your `PATH`  
- Python dependencies:

```bash
pip install ffmpeg-python
````

---

## ⚙️ Installation

```bash
git clone https://github.com/MisaghMomeniB/Audio2Video-Python.git
cd Audio2Video-Python
pip install -r requirements.txt  # includes ffmpeg-python
```

---

## 🚀 Usage

### As CLI script

```bash
python audio2video.py \
  --video input.mp4 \
  --audio narration.wav \
  --output final_output.mp4 \
  --framerate 30
```

### As module

```python
from audio2video import merge_audio_video

merge_audio_video(
    video_path='input.mp4',
    audio_path='narration.wav',
    output_path='output.mp4',
    frame_rate=30
)
```

---

## 📁 Code Structure

```
Audio2Video-Python/
├── audio2video.py       # main script & module
├── requirements.txt
└── README.md
```

* `merge_audio_video(...)`: core function wrapping ffmpeg commands
* CLI `argparse` implementation to parse flags

---

## 🔍 Implementation Details

* Uses **ffmpeg-python** to build pipelines like:

  ```python
  (
    ffmpeg
    .input(video_path)
    .input(audio_path)
    .output(output_path, vcodec='copy', acodec='aac', strict='experimental', r=frame_rate)
    .run(overwrite_output=True)
  )
  ```
* Ensures final output uses correct format, codec, and frame rate for smooth playback
* Handles errors when files are missing or incompatible

---

## 💡 Enhancement Ideas

* Add support for:

  * Image sequence → video conversion
  * Custom transitions or fade effects
  * Embedding multiple audio tracks (e.g., music + voiceover)
  * CLI flags for codec choice (e.g., H.264 vs HEVC)
* Provide progress logs or real-time progress bar

---

## 🤝 Contributing

Contributions welcome:

1. Fork the repo
2. Create a branch (`feature/...`)
3. Document your changes and add tests
4. Send a Pull Request

---

## 📄 License

Licensed under the **MIT License**. See `LICENSE` for details.
