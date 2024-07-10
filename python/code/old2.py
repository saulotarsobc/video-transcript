import whisper
import json

import datetime


def format_time(seconds):
    hours = int(seconds / 3600)
    seconds %= 3600
    minutes = int(seconds / 60)
    seconds %= 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)

    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


def json_to_srt(json_data):
    srt_content = ""
    segments = json_data.get("segments", [])
    segment_id = 1

    for segment in segments:
        start_time = segment.get("start", 0.0)
        end_time = segment.get("end", 0.0)
        text = segment.get("text", "")

        # Format start and end times into HH:MM:SS,MMM
        start_time_formatted = format_time(start_time)
        end_time_formatted = format_time(end_time)

        # Construct the subtitle block in .srt format
        srt_content += f"{segment_id}\n"
        srt_content += f"{start_time_formatted} --> {end_time_formatted}\n"
        srt_content += f"{text}\n\n"

        segment_id += 1

    return srt_content.strip()


def write_srt(srt_content, ffile_name):
    with open(ffile_name, "w", encoding="utf-8") as f:
        f.write(srt_content)


# =======================
file = "audio.wav"


model = whisper.load_model("tiny", download_root="temp")
result_json = model.transcribe(file)
srt_content = json_to_srt(result_json)

write_srt(srt_content, file.split(".")[0] + ".srt")
write_srt(json.dumps(result_json, indent=2), file.split(".")[0] + ".json")
