import os
import json
import whisper
from utils.Logger import logger

class TranscriptionService:
    def __init__(self, model_name, verbose):
        self.model = whisper.load_model(model_name, download_root="./temp/models")
        self.verbose = verbose

    def transcribe(self, file_name, language, task):
        logger.info(f"Transcribing ./temp/videos/{file_name} ...")
        try:
            result = self.model.transcribe(
                audio=f"./temp/videos/{file_name}",
                language=language,
                task=task,
                initial_prompt="Gere a transcrição de um video",
                verbose=self.verbose,
            )
            
            logger.log(f"Transcribed {file_name}!")
            
            return result
        
        except Exception as e:
            logger.error(f"Error transcribing /temp/videos/{file_name}: {str(e)}")
            return None

    def save_transcription(self, transcription, file_name):
        final_file_name = f"{file_name.split('.')[0]}.json"
        
        try:
            with open(f"./temp/transcriptions/{final_file_name}", "w", encoding="utf-8") as f:
                json.dump(transcription, f, ensure_ascii=False, indent=4)
            
            logger.log(f"Saved transcription in ./temp/transcriptions/{final_file_name}!")
        
        except Exception as e:
            logger.error(f"Error saving transcription {final_file_name}: {str(e)}")
