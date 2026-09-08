import os  # noqa: I001

import subprocess

from flask import Flask, render_template, request, send_from_directory

from werkzeug.utils import secure_filename

from crowdguard_model import process_crowdguard

from gemini_service import generate_crowd_assessment


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"mp4", "mov", "avi"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/outputs/<path:filename>")
def serve_output(filename):
    return send_from_directory("outputs", filename)


@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    if request.method == "POST":

        if "video" not in request.files:
            return "No video file was uploaded.", 400

        video = request.files["video"]

        if video.filename == "":
            return "No video file was selected.", 400

        if video and allowed_file(video.filename):

            filename = secure_filename(video.filename)

            video_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )


            video.save(video_path)

            output_video, output_metrics, metrics_df = process_crowdguard(video_path)
            
            browser_video = output_video.replace(".mp4", "_browser.mp4")

            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i", output_video,
                    "-c:v", "libx264",
                    "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart",
                    browser_video,
                ],
                check=True
            )

            peak_people = int(metrics_df["people"].max())
            peak_occupancy = float(metrics_df["occupancy"].max() * 100)

            valid_speeds = metrics_df["speed"].dropna()
            avg_speed = float(valid_speeds.mean()) if not valid_speeds.empty else 0.0

            risk_order = {
                "LOW": 1,
                "MEDIUM": 2,
                "HIGH": 3,
            }

            risk_levels = metrics_df["risk_level"].astype(str).str.upper()

            overall_risk = risk_levels.mode().iloc[0]

            peak_risk = max(
                risk_levels,
                key=lambda risk: risk_order.get(risk, 0)
            )

            summary_metrics = {
                "peak_people": peak_people,
                "peak_occupancy": peak_occupancy,
                "avg_speed": avg_speed,
                "overall_risk": overall_risk,
                "peak_risk": peak_risk,
            }

            ai_assessment = generate_crowd_assessment(summary_metrics)

            return render_template(
                "results.html",
                filename=filename,
                output_video=browser_video,
                output_metrics=output_metrics,
                metrics=metrics_df.to_dict(orient="records"),
                summary=summary_metrics,
                ai_assessment=ai_assessment,
            )

        return "Unsupported video format.", 400

    return render_template("analyze.html")


if __name__ == "__main__":
    app.run(debug=True)

