import json
import os
from utils.Logger import logger

class SubtitleService:
    def __init__(self):
        self.srt_folder = "./temp/srts"

    @staticmethod
    def format_time(seconds):
        hours = int(seconds / 3600)
        seconds %= 3600
        minutes = int(seconds / 60)
        seconds %= 60
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)

        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def to_str(self, json_data):
        srt_content = ""
        segments = json_data.get("segments", [])
        segment_id = 1

        for segment in segments:
            start_time = segment.get("start", 0.0)
            end_time = segment.get("end", 0.0)
            text = segment.get("text", "")

            start_time_formatted = self.format_time(start_time)
            end_time_formatted = self.format_time(end_time)

            srt_content += f"{segment_id}\n"
            srt_content += f"{start_time_formatted} --> {end_time_formatted}\n"
            srt_content += f"{text}\n\n"

            segment_id += 1

        return srt_content.strip()

    def write_srt(self, srt_content, file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(srt_content)

    def json_to_srt(self, json_data, file_name):
        final_file_name = f"{file_name.split('.')[0]}.srt"
        file_path = f"{self.srt_folder}/{final_file_name}"
        
        srt_content = self.to_str(json_data)
        self.write_srt(srt_content, file_path)
        
        logger.info(f"Saved transcription in {file_path}!")
