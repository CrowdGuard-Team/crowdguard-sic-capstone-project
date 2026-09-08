import os  # noqa: I001

import subprocess

from flask import Flask, render_template, request, send_from_directory

from werkzeug.utils import secure_filename

from crowdguard_model import process_crowdguard


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

            return render_template(
                "results.html",
                filename=filename,
                output_video=browser_video,
                output_metrics=output_metrics,
                metrics=metrics_df.to_dict(orient="records")
            )

        return "Unsupported video format.", 400

    return render_template("analyze.html")



if __name__ == "__main__":
    app.run(debug=True)

