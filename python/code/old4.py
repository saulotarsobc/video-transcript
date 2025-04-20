import os
from time import sleep
import requests
import whisper
import json
import dotenv

from utils.Logger import Logger
from utils.json_to_srt import json_to_srt


# env
dotenv.load_dotenv()
VERBOSE = os.getenv("VERBOSE") == "True"
MODEL = os.getenv("MODEL") or "tiny"
PAUSE = int(os.getenv("PAUSE") or 60)

# init
## create folders
os.makedirs("./temp/models", exist_ok=True)
os.makedirs("./temp/videos", exist_ok=True)
os.makedirs("./temp/transcriptions", exist_ok=True)

## load model
model = whisper.load_model(
    WHISPER_MODEL,
    download_root="./temp/models",
)

## init logger
logger = Logger()

def getVideos():
    """
    A function that retrieves the list of global videos.

    Parameters:
        - None

    Returns:
        - The list of global videos.
    """
    return global_videos


def removeVideoById(id):
    """
    Removes a video from the global videos list by its id.

    Parameters:
        id: The id of the video to be removed.

    Returns:
        None
    """
    global global_videos
    global_videos = [video for video in global_videos if video["id"] != id]
    logger.info(f"Removed video with id={id}")


def videoDownload(ffile_name, url):
    """
    Downloads a video file from the provided URL and saves it in the specified location.

    Parameters:
        ffile_name (str): The name of the file to be downloaded.
        url (str): The URL from which the file will be downloaded.

    Returns:
        bool: True if the download is successful, False otherwise.
    """
    logger.info(f"Downloading {ffile_name}...")

    try:
        os.makedirs(f"./temp/videos/{ffile_name}", exist_ok=True)
        r = requests.get(url, allow_redirects=True)
        with open(f"./temp/videos/{ffile_name}/video.mp4", "wb") as f:
            f.write(r.content)

        logger.log(f"Downloaded {ffile_name}!")

        return True

    except Exception as e:
        logger.error(f"Error downloading {ffile_name}: {str(e)}")

    return False


def generetePrompt(name, course):
    """
    A function that generates a prompt for transcribing a video based on the provided name and course information.

    Parameters:
        name (str): The name of the video.
        course (dict): A dictionary containing information about the course, including 'name' and 'subtitle'.

    Returns:
        str: The prompt generated for transcribing the video.
    """
    prompt = f'Gere a transcricão de vídeo que tem como tema"{name}", {course["name"]}. {course["subtitle"]}'
    logger.info(f"Prompt: {prompt}")
    return prompt


def transcribe(prompt, ffile_name, language, task):
    """
    A function that transcribes a video file based on the provided prompt, file name, language, task, and initial prompt.

    Parameters:
        prompt (str): The prompt for the transcription.
        ffile_name (str): The name of the video file to transcribe.
        language (str): The language of the video.
        task (str): The transcription task.
        initial_prompt (str): The initial prompt for the transcription.

    Returns:
        The transcription result if successful, otherwise None.
    """
    logger.info(f"Transcribing ./temp/videos/{ffile_name}/video.mp4 ...")

    try:
        result = model.transcribe(
            audio=f"./temp/videos/{ffile_name}/video.mp4",
            language=language,
            task=task,
            initial_prompt=prompt,
        )

        logger.log(f"Transcribed {ffile_name}!")
        return result

    except Exception as e:
        logger.error(
            f"Error transcribing video {ffile_name}: {str(e)}"
        )
        return None


def saveTranscription(transcription, ffile_name):
    """
    Saves a transcription to a JSON file.

    Args:
        transcription (dict): The transcription data to be saved.
        ffile_name (str): The name of the file to save the transcription in.

    Returns:
        None

    This function creates a directory for the given file name if it does not already exist.
    It then saves the transcription data to a JSON file with the specified file name.
    The transcription data is written with UTF-8 encoding and indented with 4 spaces.

    Example:
        saveTranscription({'segments': [{'start': 0.0, 'end': 2.0, 'text': 'Hello world!'}]}, 'example')
    """
    logger.info(
        f"Saving transcription in ./temp/transcriptions/{ffile_name}/transcription.json ..."
    )

    os.makedirs(f"./temp/transcriptions/{ffile_name}", exist_ok=True)

    with open(
        f"./temp/transcriptions/{ffile_name}/transcription.json", "w", encoding="utf-8"
    ) as f:
        json.dump(transcription, f, ensure_ascii=False, indent=4)

    logger.log(
        f"Saved transcription in ./temp/transcriptions/{ffile_name}/transcription.json!"
    )


if __name__ == "__main__":
    while True:

        videos = getVideos()

        while len(getVideos()) > 0:
            logger.info(f"Getting videos...")
            logger.log(f"Got {len(global_videos)} videos!")

            for video in videos:
                logger.info(f"Remaining videos: {len(global_videos)}")

                downloaded = videoDownload(video["ffile_name"], video["url"])
                prompt = generetePrompt(video["name"], video["course"])

                result = transcribe(
                    prompt, video["ffile_name"], "pt", "transcribe", prompt
                )

                if result is not None:
                    ## save transcription in json
                    saveTranscription(result, video["ffile_name"])

                    ## save transcription in .srt
                    json_to_srt(result, video["ffile_name"])

                    ## remove video from global_videos
                    removeVideoById(video["id"])

                elif result is None:
                    logger.error("Error transcribing video")

        sleep(PAUSE)
