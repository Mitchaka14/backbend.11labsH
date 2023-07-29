# /Tdeepgram_request.py
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_token = os.getenv("D_API_TOKEN")


def DeepgramTranscription(audio_path):
    url = "https://api.deepgram.com/v1/listen?model=general&tier=base&detect_language=true&diarize=true"

    headers = {"Authorization": f"Token {api_token}"}

    with open(audio_path, "rb") as audio_file:
        response = requests.post(url, headers=headers, data=audio_file)

    response_data = response.json()

    # Write the response to a json file
    with open("Response/Dresponse.json", "w") as json_file:
        json.dump(response_data, json_file, indent=4)

    print("Response saved to 'Response/Dresponse.json'")

    return response_data


if __name__ == "__main__":
    audio_path = "Media/combined_vocals.wav"
    DeepgramTranscription(audio_path)
