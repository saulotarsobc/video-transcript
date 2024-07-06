import whisper
import json

import datetime


def format_time(seconds):
    delta = datetime.timedelta(seconds=seconds)
    time_str = str(delta)
    time_str = "0" + time_str if delta.total_seconds() < 36000 else time_str
    return time_str.replace(".", ",")


def write_srt(transcription, filename):
    with open(filename, "w", encoding="utf-8") as f:
        for i, segment in enumerate(transcription['segments']):
            start = format_time(segment['start'])
            end = format_time(segment['end'])
            text = segment['text']
            f.write(f"{i + 1}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")


model = whisper.load_model("base")

result = model.transcribe("audio.wav")

write_srt(result, "transcription.srt")
print(json.dumps(result, indent=2))
