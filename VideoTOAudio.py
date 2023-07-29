# ./VideoTOAudio.py
import os
import subprocess
import shutil


def extract_audio_from_video(video_path, output_dir):
    # Define the output paths
    output_video_path = os.path.join(output_dir, "oVideo.mp4")
    output_audio_path = os.path.join(output_dir, "oAudio.mp3")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Copy the input video to the output video path
    shutil.copy(video_path, output_video_path)

    # Extract audio from the video
    command = f'ffmpeg -i "{output_video_path}" -ab 160k -ac 2 -ar 44100 -vn "{output_audio_path}"'
    subprocess.call(command, shell=True)

    # Get the length of the audio
    command = f'ffprobe -i "{output_audio_path}" -show_entries format=duration -v quiet -of csv="p=0"'
    result = subprocess.run(command, shell=True, capture_output=True)
    duration = float(result.stdout.decode().strip())

    return duration


if __name__ == "__main__":
    video_path = "trialMedia/bandicam 2023-07-23 20-51-46-536.mp4"
    output_dir = "trialMedia"
    extract_audio_from_video(video_path, output_dir)
