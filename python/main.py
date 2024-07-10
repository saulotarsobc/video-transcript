import os
from time import sleep
import requests
import whisper
import json
import dotenv
import datetime

from utils.Logger import logger
from utils.json_to_srt import json_to_srt


# env
dotenv.load_dotenv()
VERBOSE = os.getenv("VERBOSE") == "True"
MODEL = os.getenv("MODEL") or "tiny"
PAUSE = int(os.getenv("PAUSE") or 60)
APP_TOKEN = os.getenv("APP_TOKEN")
BASE_URL = os.getenv("BASE_URL")

logger.info(
    f"\nInitializing application... >>> Verbose={VERBOSE}, Model={MODEL}, Pause={PAUSE}, Base Url={BASE_URL}\n"
)

# init
## create folders
os.makedirs("./temp/models", exist_ok=True)
os.makedirs("./temp/videos", exist_ok=True)
os.makedirs("./temp/transcriptions", exist_ok=True)
os.makedirs("./temp/srts", exist_ok=True)

## load model
model = whisper.load_model(MODEL, download_root="./temp/models")


def get_headers():
    headers = {}
    headers["Content-Type"] = "application/json"
    headers["X-App-Token"] = os.getenv("APP_TOKEN")
    return headers


def get_videos():
    # TODO: conseguir a lista de ids de videos para transcrição
    return [3487]


def get_videos_url(ids):
    logger.info(f"Getting video url for video ids={ids}...")

    url = f"{BASE_URL}/bot/get-urls"
    payload = json.dumps({"ids": ids})
    headers = get_headers()

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 201:
        logger.info(f"Got video url for video ids={ids}")
        return response.json()
    else:
        logger.error(f"Error getting video url for video ids={ids}")
        return None


def download_video(url, ffile_name):
    logger.info(f"Downloading {ffile_name}...")
    try:
        r = requests.get(url, allow_redirects=True)
        with open(f"./temp/videos/{ffile_name}", "wb") as f:
            f.write(r.content)

        logger.log(f"Downloaded {ffile_name}!")

        return True

    except Exception as e:
        logger.error(f"Error downloading {ffile_name}: {str(e)}")

    return False


def transcribe(ffile_name, language, task):
    logger.info(f"Transcribing ./temp/videos/{ffile_name} ...")

    try:
        result = model.transcribe(
            audio=f"./temp/videos/{ffile_name}",
            language=language,
            task=task,
            initial_prompt="Gere a transcrição de um video",
            verbose=VERBOSE,
        )

        logger.log(f"Transcribed {ffile_name}!")
        return result

    except Exception as e:
        logger.error(f"Error transcribing /temp/videos/{ffile_name}: {str(e)}")
        return None


def saveTranscription(transcription, ffile_name):
    final_file_name = f"{ffile_name.split('.')[0]}.json"
    try:
        with open(
            f"./temp/transcriptions/{final_file_name}", "w", encoding="utf-8"
        ) as f:
            json.dump(transcription, f, ensure_ascii=False, indent=4)

        logger.log(f"Saved transcription in ./temp/transcriptions/{final_file_name}!")

    except Exception as e:
        logger.error(f"Error saving transcription {final_file_name}: {str(e)}")


if __name__ == "__main__":
    while True:
        ids = get_videos()
        data = get_videos_url(ids)

        if data is not None:
            for item in data:
                down = download_video(item["url"], item["file"]["name"])

                if down:
                    transcription = transcribe(
                        item["file"]["name"],
                        language="pt",
                        task="transcribe",
                    )

                    if transcription is not None:
                        saveTranscription(transcription, item["file"]["name"])
                        json_to_srt(transcription, item["file"]["name"])

        else:
            logger.error(f"Error getting video url for video ids={ids}")

        sleep(PAUSE)
