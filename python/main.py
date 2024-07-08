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
VERBOSE = os.getenv('VERBOSE') == 'True'
MODEL = os.getenv('MODEL') or 'tiny'
PAUSE = int(os.getenv('PAUSE') or 60)

# init
os.makedirs('./temp/models', exist_ok=True)
model = whisper.load_model(
    MODEL,
    download_root="./temp/models",
)


logger = Logger()


# debug
global_videos = [
    {
        'id': 1,
        'fileName': 'esportes-diversao-garantida',
        'name': 'Esportes — Com estas dicas a diversão é garantida!',
        'url': 'https://download-a.akamaihd.net/files/content_assets/a5/502018215_T_cnt_1_r720P.mp4',
        'course': {
                'name': 'Quadro Branco',
                'subtitle': 'Nesse video vamos aprender como nos divertir da forma correta!'
        },
    },
    {
        'id': 2,
        'fileName': 'amigos-de-jeova-jeremias',
        'name': 'Vamos Aprender com os Amigos de Jeová — Jeremias',
        'url': 'https://download-a.akamaihd.net/files/media_publication/92/ljf_T_002_r240P.mp4',
        'course': {
                'name': 'Vamos Aprender com os Amigos de Jeová',
                'subtitle': 'Nesse video vamos aprender comoo demostar a coragem que os Amigos de Jeová tem! Em especial o profeta Jeremias.'
        },
    },
    {
        'id': 3,
        'fileName': 'boletim-4',
        'name': 'Boletim do Corpo Governante (2024) — n.º 4',
        'url': 'https://download-a.akamaihd.net/files/content_assets/2a/1112024011_T_cnt_1_r360P.mp4',
        'course': {
                'name': 'Boletim do Corpo Governante',
                'subtitle': 'Nesse boletim veremos o que nossos irmão estão achando sobre o congresso Regional de 2024'
        },
    },
]


def getVideos():
    return global_videos


def removeVideoById(id):
    global global_videos
    global_videos = [video for video in global_videos if video['id'] != id]
    logger.info(f'Removed video with id={id}')


def videoDownload(fileName, url):
    """
    Downloads a video file from the provided URL and saves it in the specified location.

    Parameters:
        fileName (str): The name of the file to be downloaded.
        url (str): The URL from which the file will be downloaded.

    Returns:
        bool: True if the download is successful, False otherwise.
    """
    logger.info(f'Downloading {fileName}...')

    try:
        os.makedirs(f'./temp/videos/{fileName}', exist_ok=True)
        r = requests.get(url, allow_redirects=True)
        with open(f'./temp/videos/{fileName}/video.mp4', 'wb') as f:
            f.write(r.content)

        logger.log(f'Downloaded {fileName}!')

        return True

    except Exception as e:
        logger.error(f'Error downloading {fileName}: {str(e)}')

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
    prompt = f'Gere a transcricão do video de "{name}" do {course["name"]}. Esse curso tem como subtitulo: {course["subtitle"]}'
    logger.info(f'Prompt: {prompt}')
    return prompt


def transcribe(prompt, fileName, language, task, initial_prompt):
    """
    A function that transcribes a video file based on the provided prompt, file name, language, task, and initial prompt.

    Parameters:
        prompt (str): The prompt for the transcription.
        fileName (str): The name of the video file to transcribe.
        language (str): The language of the video.
        task (str): The transcription task.
        initial_prompt (str): The initial prompt for the transcription.

    Returns:
        The transcription result if successful, otherwise None.
    """
    logger.info(f'Transcribing ./temp/videos/{fileName}/video.mp4 ...')

    try:
        result = model.transcribe(
            audio=f'./temp/videos/{fileName}/video.mp4',
            language=language,
            task=task,
            initial_prompt=prompt,
            verbose=VERBOSE,
        )

        logger.log(f'Transcribed {fileName}!')
        return result

    except Exception as e:
        logger.error(
            f'Error transcribing /temp/videos/{fileName}/video.mp4: {str(e)}')
        return None


def saveTranscription(transcription, fileName):
    """
    Saves a transcription to a JSON file.

    Args:
        transcription (dict): The transcription data to be saved.
        fileName (str): The name of the file to save the transcription in.

    Returns:
        None

    This function creates a directory for the given file name if it does not already exist.
    It then saves the transcription data to a JSON file with the specified file name.
    The transcription data is written with UTF-8 encoding and indented with 4 spaces.

    Example:
        saveTranscription({'segments': [{'start': 0.0, 'end': 2.0, 'text': 'Hello world!'}]}, 'example')
    """
    logger.info(
        f'Saving transcription in ./temp/transcriptions/{fileName}/transcription.json ...')

    os.makedirs(f'./temp/transcriptions/{fileName}', exist_ok=True)

    with open(f'./temp/transcriptions/{fileName}/transcription.json', 'w', encoding='utf-8') as f:
        json.dump(transcription, f, ensure_ascii=False, indent=4)

    logger.log(
        f'Saved transcription in ./temp/transcriptions/{fileName}/transcription.json!')


if __name__ == '__main__':
    while True:

        videos = getVideos()

        while len(getVideos()) > 0:
            logger.info(f'Getting videos...')
            logger.log(f'Got {len(global_videos)} videos!')

            for video in videos:
                logger.info(f'Remaining videos: {len(global_videos)}')

                downloaded = videoDownload(video['fileName'], video['url'])
                prompt = generetePrompt(video['name'], video['course'])

                result = transcribe(
                    prompt, video['fileName'], 'pt', 'transcribe', prompt)

                if result is not None:
                    saveTranscription(result, video['fileName'])
                    json_to_srt(result, video['fileName'])
                    removeVideoById(video['id'])

                elif result is None:
                    logger.error('Error transcribing video')

        sleep(PAUSE)
