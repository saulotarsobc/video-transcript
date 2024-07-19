import dotenv
import os

from time import sleep

from utils.Logger import logger
from utils.Folders import Folders

from services.VideoService import VideoService
from services.TranscriptionService import TranscriptionService
from services.SubtitleService import SubtitleService
from services.OllamaService import OllamaService

# env
dotenv.load_dotenv()
VERBOSE     = os.getenv("VERBOSE") == "True"
MODEL       = os.getenv("MODEL") or "tiny"
PAUSE       = int(os.getenv("PAUSE") or 60)
BASE_URL    = os.getenv("BASE_URL")
APP_TOKEN   = os.getenv("APP_TOKEN")

logger.info(f"\n\nInitializing application: Verbose={VERBOSE}, Model={MODEL}, Pause={PAUSE}, Base Url={BASE_URL}\n")

# init services
video_service           = VideoService(BASE_URL, APP_TOKEN)
transcription_service   = TranscriptionService(MODEL, VERBOSE)
subtitle_service        = SubtitleService()

# create folders
Folders.create_directories()

if __name__ == "__main__":
    while True:
        ids = video_service.get_videos()
        data = video_service.get_videos_url(ids)

        if data is not None:
            for item in data:
                down = video_service.download_video(item["url"], item["file"]["name"])

                if down:
                    transcription = transcription_service.transcribe(item["file"]["name"], language="pt", task="transcribe")

                    if transcription is not None:
                        transcription_service.save_transcription(transcription, item["file"]["name"])

                        subtitle_service.json_to_srt(transcription, item["file"]["name"])

                        chat = OllamaService(file_name=item["file"]["name"])
                        chat.generate_summary(transcription["text"])

        else:
            logger.error(f"Error getting video url for video ids={ids}")

        # sleep(PAUSE)
        exit('Done!')
