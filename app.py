import os  # noqa: I001

from flask import Flask, render_template, request

from werkzeug.utils import secure_filename


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

            return f"Video uploaded successfully: {filename}"

        return "Unsupported video format.", 400

    return render_template("analyze.html")



if __name__ == "__main__":
    app.run(debug=True)

