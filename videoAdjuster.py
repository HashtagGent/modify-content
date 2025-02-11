import random
import datetime
import os
import time
import moviepy.editor as mp
import ffmpeg

def modify_video(input_path, output_path):
    clip = mp.VideoFileClip(input_path)
    brightness_factor = random.uniform(0.95, 1.05)
    rotation_angle = random.choice([-1, 1])
    
    # Apply brightness and rotation adjustments
    clip = clip.fx(mp.vfx.colorx, brightness_factor).rotate(rotation_angle)

    # Adjust audio (if exists)
    if clip.audio:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        base_name = os.path.basename(input_path).split('.')[0]
        audio_path = f"temp_audio_{base_name}_{timestamp}.wav"
        new_audio_path = f"temp_audio_pitch_{base_name}_{timestamp}.wav"

        # Export and modify audio
        clip.audio.write_audiofile(audio_path, codec='pcm_s16le')
        pitch_factor = random.uniform(0.95, 1.05)

        ffmpeg.input(audio_path).output(new_audio_path, af=f"rubberband=pitch={pitch_factor}").run(overwrite_output=True)
        time.sleep(0.5)

        new_audio_clip = mp.AudioFileClip(new_audio_path)
        clip = clip.set_audio(new_audio_clip)

        # Write final video
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4)

        # Cleanup
        new_audio_clip.close()
        os.remove(audio_path)
        os.remove(new_audio_path)
    else:
        print("No audio found. Processing video only.")
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", threads=4)

    clip.close()

if __name__ == "__main__":
    input_video = "input.mp4"  # Replace with actual file path from Make.com
    output_video = "output.mp4"  # Replace with the desired output path
    modify_video(input_video, output_video)
