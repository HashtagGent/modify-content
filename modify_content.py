import os
from flask import Flask, request, send_file
import random
import datetime
import moviepy.editor as mp
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Modify Video Function
def modify_video(input_path, output_path):
    clip = mp.VideoFileClip(input_path)
    brightness_factor = random.uniform(0.95, 1.05)
    rotation_angle = random.choice([-1, 1])
    clip = clip.fx(mp.vfx.colorx, brightness_factor).rotate(rotation_angle)

    # Save using original format (keep existing extension)
    clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    clip.close()
    return output_path


# Modify Image Function
def modify_photo(input_path, output_path):
    image = Image.open(input_path)
    width, height = image.size
    crop_width = width - 30  # Crop 30px horizontally
    left = (width - crop_width) // 2
    right = left + crop_width
    image = image.crop((left, 0, right, height))

    # Save using the original format (keep existing extension)
    image.save(output_path)
    return output_path


@app.route("/process", methods=["POST"])
def process_file():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400
    
    file = request.files["file"]
    file_type = file.filename.split(".")[-1].lower()
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    input_path = os.path.join(UPLOAD_FOLDER, f"{timestamp}.{file_type}")
    output_path = os.path.join(OUTPUT_FOLDER, f"{timestamp}_modified.{file_type}")  # Keep original format

    file.save(input_path)

    if file_type == "mp4":
        output_path = modify_video(input_path, output_path)
        mime_type = "video/mp4"

    elif file_type in ["jpg", "png"]:
        output_path = modify_photo(input_path, output_path)
        mime_type = f"image/{file_type}"  # Keep original MIME type

    else:
        return {"error": "Unsupported file type"}, 400

    return send_file(output_path, as_attachment=True, mimetype=mime_type, download_name=f"{timestamp}_modified.{file_type}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
