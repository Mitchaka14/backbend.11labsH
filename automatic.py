# /automatic.py
import os
import shutil
from VideoTOAudio import extract_audio_from_video
from vocal_separation import separate_vocals
from Twhisper_request import WhisperTranscription
from Tdeepgram_request import DeepgramTranscription
from formartingAndRetrival import combine_srt_json


def clear_directory(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


class Automatic:
    def __init__(self, video_path):
        self.video_path = video_path
        self.use_deepgram = True

    def run(self):
        # Clear the Media and Response directories
        clear_directory("Media")
        clear_directory("Response")

        # Extract audio from video
        output_dir = "Media"
        duration = extract_audio_from_video(self.video_path, output_dir)

        # Separate vocals
        input_audio_path = os.path.join(output_dir, "oAudio.mp3")
        separate_vocals(input_audio_path, output_dir)

        # Transcribe audio
        audio_path = os.path.join(output_dir, "combined_vocals.wav")

        # Always run WhisperTranscription
        WhisperTranscription(audio_path)

        # Only run DeepgramTranscription if use_deepgram is True
        if self.use_deepgram:
            DeepgramTranscription(audio_path)

        combine_srt_json()

        return "Done"


if __name__ == "__main__":
    video_path = "testMedia/Gorosei (Five Elders) First Appearance and Already Talking About Luffy.mp4"
    auto = Automatic(video_path)
    status = auto.run()
    print(status)
