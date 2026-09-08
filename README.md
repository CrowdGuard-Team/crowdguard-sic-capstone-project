# CrowdGuard - SIC Capstone Project

CrowdGuard is an AI-powered crowd monitoring and early risk assessment system developed as part of the Samsung Innovation Campus (SIC) Capstone Project.

The system uses computer vision to detect and track pedestrians in crowd videos, calculate crowd-level metrics, assess potential risk levels, and later generate AI-based summaries and recommendations.

## Current Features

- Pedestrian detection using YOLO11n
- Multi-object tracking using ByteTrack
- People counting
- Occupancy estimation
- Relative movement speed estimation
- Risk assessment with Low, Medium, and High levels
- Processed video output with visual annotations
- CSV export of frame-level metrics
- Flask-based web interface
- Video upload functionality

## Planned Features

- Display processed video and analysis results on the web interface
- Crowd metrics dashboard
- Gemini API integration for AI-generated summaries and recommendations
- Final testing and model evaluation

## Project Structure

```text
crowdguard-sic-capstone-project/
│
├── app.py
├── crowdguard_model.py
├── gemini_service.py
├── frames_to_video.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── index.html
│   ├── analyze.html
│   └── results.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│
├── uploads/
└── outputs/
```

## Dataset

This project uses the **MOT20 dataset** for crowd monitoring development and evaluation.

Dataset source:

https://huggingface.co/datasets/Lekim89/MOT20

The dataset is not included in this repository because of its size.

For development, we are currently using the **MOT20-01 training sequence**.

### 1. Install Hugging Face CLI

```bash
pip install -U huggingface_hub
```

### 2. Download MOT20-01

```bash
hf download Lekim89/MOT20 \
  --repo-type dataset \
  --include "train/MOT20-01/*" \
  --local-dir dataset
```

The downloaded sequence will be located at:

```text
dataset/train/MOT20-01/
```

### Download Other MOT20 Sequences

Other MOT20 sequences can be downloaded using the same command by changing the sequence name.

For example, to download `MOT20-02`:

```bash
hf download Lekim89/MOT20 \
  --repo-type dataset \
  --include "train/MOT20-02/*" \
  --local-dir dataset
```

The same approach can be used for the other available sequences by replacing `MOT20-02` with the required sequence name.

### Convert MOT20 Frames to Video

MOT20 sequences are provided as consecutive image frames rather than MP4 videos.

The included `frames_to_video.py` script converts the frames into a video that can be used with CrowdGuard.

By default, the script is configured to use the `MOT20-01` sequence:

```python
sequence_path = "dataset/train/MOT20-01"
```

To use another sequence, change `MOT20-01` to the name of the downloaded sequence.

For example:

```python
sequence_path = "dataset/train/MOT20-02"
```

Then run:

```bash
python frames_to_video.py
```

Make sure the selected sequence has already been downloaded into the `dataset/train/` directory before running the script.

> **Note:** The `dataset/` directory and generated video files are excluded from Git using `.gitignore`.

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Nujud11/crowdguard-sic-capstone-project.git
cd crowdguard-sic-capstone-project
```

### 2. Create a Virtual Environment

```bash
python3 -m venv crowdguard-env
source crowdguard-env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Notes

- The dataset, uploaded videos, generated outputs, model weights, virtual environment, and environment variables are excluded from Git using `.gitignore`.
- The current system is still under development.
- Model evaluation, web-based result visualization, and Gemini API integration are currently planned for the next development stages.