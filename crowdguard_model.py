import os
import cv2
import numpy as np
import pandas as pd

from collections import defaultdict, deque
from ultralytics import YOLO


# Load YOLO model once when the app starts
model = YOLO("yolo11n.pt")


def risk_assessment(person_count, occupancy, avg_speed):
    count_score = min(person_count / 150, 1.0)
    occupancy_score = min(occupancy / 0.20, 1.0)

    if avg_speed is None:
        slowness_score = 0.5
    else:
        slowness_score = 1 - min(avg_speed / 100, 1.0)

    risk_score = (
        0.50 * count_score
        + 0.30 * occupancy_score
        + 0.20 * slowness_score
    )

    if risk_score >= 0.75:
        risk_level = "HIGH"
    elif risk_score >= 0.50:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return round(risk_score, 3), risk_level


def process_crowdguard(video_path, output_folder="outputs"):
    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.splitext(os.path.basename(video_path))[0]

    output_video = os.path.join(
        output_folder,
        f"{filename}_crowdguard.mp4"
    )

    output_metrics = os.path.join(
        output_folder,
        f"{filename}_metrics.csv"
    )

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    writer = cv2.VideoWriter(
        output_video,
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    track_history = defaultdict(lambda: deque(maxlen=10))
    metrics_rows = []

    for frame_number in range(1, total_frames + 1):
        ret, frame = cap.read()

        if not ret:
            break

        result = model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml",
            classes=[0],
            conf=0.20,
            imgsz=1280,
            verbose=False
        )[0]

        person_count = 0
        total_box_area = 0
        speeds = []

        if result.boxes is not None and len(result.boxes) > 0:
            boxes = result.boxes.xyxy.cpu().numpy()

            if result.boxes.id is not None:
                ids = result.boxes.id.int().cpu().tolist()
            else:
                ids = [-1] * len(boxes)

            person_count = len(boxes)

            for box, track_id in zip(boxes, ids):
                x1, y1, x2, y2 = box

                box_width = x2 - x1
                box_height = y2 - y1

                total_box_area += box_width * box_height

                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2

                if track_id != -1:
                    history = track_history[track_id]

                    if len(history) > 0:
                        px, py = history[-1]

                        distance = np.sqrt(
                            (cx - px) ** 2
                            + (cy - py) ** 2
                        )

                        speeds.append(distance * fps)

                    history.append((cx, cy))

                cv2.rectangle(
                    frame,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 255, 0),
                    2
                )

                if track_id != -1:
                    cv2.putText(
                        frame,
                        f"ID {track_id}",
                        (int(x1), max(20, int(y1) - 5)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.45,
                        (0, 255, 0),
                        1
                    )

        occupancy = (
            total_box_area / (width * height)
            if width > 0 and height > 0
            else 0
        )

        avg_speed = (
            float(np.mean(speeds))
            if speeds
            else None
        )

        risk_score, risk_level = risk_assessment(
            person_count,
            occupancy,
            avg_speed
        )

        metrics_rows.append({
            "frame": frame_number,
            "time_sec": frame_number / fps if fps else 0,
            "people": person_count,
            "occupancy": occupancy,
            "speed": avg_speed,
            "risk_score": risk_score,
            "risk_level": risk_level
        })

        speed_display = 0 if avg_speed is None else avg_speed

        cv2.rectangle(
            frame,
            (10, 10),
            (480, 165),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            frame,
            f"People: {person_count}",
            (25, 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Occupancy: {occupancy:.2%}",
            (25, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Speed: {speed_display:.1f} px/s",
            (25, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Risk: {risk_level} ({risk_score:.2f})",
            (25, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2
        )

        writer.write(frame)

    cap.release()
    writer.release()

    metrics_df = pd.DataFrame(metrics_rows)
    metrics_df.to_csv(output_metrics, index=False)

    return output_video, output_metrics, metrics_df