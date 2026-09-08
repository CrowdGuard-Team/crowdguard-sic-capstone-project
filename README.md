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
- Model evaluation, result visualization, and Gemini API integration are currently planned for the next development stages.