import requests
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("Whisper_Token")


def WhisperTranscription(audio_path):
    print(f"Processing audio file: {audio_path}")
    url = f"https://api.openai.com/v1/audio/translations"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "model": "whisper-1",
        "response_format": "srt",
    }
    with open(audio_path, "rb") as audio_file:
        files = {"file": audio_file}
        response = requests.post(url, headers=headers, data=data, files=files)

    if response.status_code != 200:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")

    # Write the response to a .srt file
    with open("Response/Wresponse.srt", "w") as srt_file:
        srt_file.write(response.text)

    print("Response saved to 'Response/Wresponse.srt'")

    return response.text


if __name__ == "__main__":
    audio_path = "Media/combined_vocals.wav"
    WhisperTranscription(audio_path)
