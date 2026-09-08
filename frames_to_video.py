import cv2
import os
import configparser

sequence_path = "dataset/train/MOT20-01"
images_path = os.path.join(sequence_path, "img1")
seqinfo_path = os.path.join(sequence_path, "seqinfo.ini")

config = configparser.ConfigParser()
config.read(seqinfo_path)

fps = int(config["Sequence"]["frameRate"])
width = int(config["Sequence"]["imWidth"])
height = int(config["Sequence"]["imHeight"])

output_path = "mot20_01.mp4"

images = sorted([
    file_name
    for file_name in os.listdir(images_path)
    if file_name.endswith(".jpg")
])

writer = cv2.VideoWriter(
    output_path,
    cv2.VideoWriter_fourcc(*"mp4v"),
    fps,
    (width, height)
)

for image_name in images:
    frame_path = os.path.join(images_path, image_name)
    frame = cv2.imread(frame_path)

    if frame is not None:
        writer.write(frame)

writer.release()

print("Video created successfully:", output_path)