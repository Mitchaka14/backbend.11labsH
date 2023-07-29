# /formartingAndRetrival.py
import json
import srt
from datetime import timedelta

srt_file_path = "Response/Wresponse.srt"
json_file_path = "Response/Dresponse.json"
output_srt_file_path = "Response/D+Wresponse.srt"


def combine_srt_json():
    with open(srt_file_path, "r") as srt_file, open(json_file_path, "r") as json_file:
        srt_data = list(srt.parse(srt_file.read()))
        json_data = json.load(json_file)

        for word in json_data["results"]["channels"][0]["alternatives"][0]["words"]:
            for subtitle in srt_data:
                start_time = subtitle.start.total_seconds()
                end_time = subtitle.end.total_seconds()
                if start_time <= word["start"] and end_time >= word["end"]:
                    speaker = f"S{word['speaker'] + 1}"  # Adjust speaker notation to S1, S2, etc.
                    if not subtitle.content.startswith(speaker):
                        subtitle.content = f"{speaker}:\n{subtitle.content}"

        with open(output_srt_file_path, "w") as output_srt_file:
            output_srt_file.write(srt.compose(srt_data))


def get_lines_by_speaker(speaker_id):
    with open(output_srt_file_path, "r") as srt_file:
        srt_data = list(srt.parse(srt_file.read()))

        lines_by_speaker = [
            subtitle.content
            for subtitle in srt_data
            if subtitle.content.startswith(f"Speaker {speaker_id}:")
        ]

    return lines_by_speaker


def update_srt_line(time_within_range, new_text):
    with open(output_srt_file_path, "r") as srt_file:
        srt_data = list(srt.parse(srt_file.read()))

        time_within_range = timedelta(seconds=time_within_range)

        for subtitle in srt_data:
            if (
                subtitle.start <= time_within_range
                and subtitle.end >= time_within_range
            ):
                subtitle.content = new_text

        # Write updated SRT back to the file
        with open(output_srt_file_path, "w") as srt_file:
            srt_file.write(srt.compose(srt_data))


def get_line_by_time(time_within_range):
    with open(output_srt_file_path, "r") as srt_file:
        srt_data = list(srt.parse(srt_file.read()))

        time_within_range = timedelta(seconds=time_within_range)

        for subtitle in srt_data:
            if (
                subtitle.start <= time_within_range
                and subtitle.end >= time_within_range
            ):
                return subtitle.content

    return None


def update_srt_line_by_index(line_number, new_text):
    with open(output_srt_file_path, "r") as srt_file:
        srt_data = list(srt.parse(srt_file.read()))

        # Adjust line_number to zero-based index
        srt_data[line_number - 1].content = new_text

        # Write updated SRT back to the file
        with open(output_srt_file_path, "w") as srt_file:
            srt_file.write(srt.compose(srt_data))


def get_all_lines_formatted():
    with open(output_srt_file_path, "r") as srt_file:
        srt_data = list(srt.parse(srt_file.read()))

        formatted_lines = []
        previous_end_time = 0

        for subtitle in srt_data:
            # Check for gap between subtitles
            if subtitle.start.total_seconds() > previous_end_time:
                formatted_lines.append(
                    {"fromMs": previous_end_time * 1000, "description": "S0"}
                )

            formatted_lines.append(
                {
                    "fromMs": subtitle.start.total_seconds() * 1000,
                    "description": subtitle.content.split(":")[0],
                }
            )

            previous_end_time = subtitle.end.total_seconds()

        return formatted_lines


if __name__ == "__main__":
    speaker_id = 1  # Change this to your speaker id
    time_within_range = 2  # Time within the range of a subtitle
    new_text = "What? Red Hair Shanks?"

    # Combine SRT and JSON files
    # combine_srt_json()

    # # Get all lines by a speaker
    # lines_by_speaker = get_lines_by_speaker(speaker_id)
    # print(f"Lines by Speaker {speaker_id}: {lines_by_speaker}")

    # # Update a line in the SRT file
    # update_srt_line(time_within_range, new_text)
    update_srt_line_by_index(2, new_text)
    print(get_all_lines_formatted())
    # # Get a line by time range
    # line = get_line_by_time(time_within_range)
    # print(f"Line from {time_within_range} to {time_within_range}: {line}")
