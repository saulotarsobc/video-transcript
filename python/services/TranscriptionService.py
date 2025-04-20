import os
import json
import whisper
import torch
from utils.Logger import logger

class TranscriptionService:
    def __init__(self, model_name, verbose):
        self.model_name = model_name
        self.verbose = verbose
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(self.model_name, download_root="./temp/models")
        self.model = self.model.to(self.device)

        logger.info(f"Using device: {self.device}")

    def transcribe(self, file_name, language="pt", task="transcribe"):
        logger.info(f"Transcribing {file_name} with language {language} and task {task} with model \"{self.model_name}\"")
        try:
            result = self.model.transcribe(
                audio= f"./temp/videos/{file_name}",
                language=language,
                task=task,
                verbose=self.verbose
            )
            
            # Filter out low confidence segments
            filtered_segments = [
                seg for seg in result["segments"]
                if seg["avg_logprob"] > -0.3 and seg["compression_ratio"] > 1.0
            ]
            
            # Rebuild the text from filtered segments
            if filtered_segments:
                result["segments"] = filtered_segments
                result["text"] = " ".join(seg["text"].strip() for seg in filtered_segments)

            return result
        
        except Exception as e:
            logger.error(f"Error transcribing {file_name}: {str(e)}")
            return None

    def save_transcription(self, transcription, file_name):
        final_file_name = f"{file_name.split('.')[0]}.json"
        try:
            with open(f"./temp/transcriptions/{final_file_name}", "w", encoding="utf-8") as f:
                json.dump(transcription, f, ensure_ascii=False, indent=4)
            
            logger.log(f"Saved transcription in ./temp/transcriptions/{final_file_name}!")
        
        except Exception as e:
            logger.error(f"Error saving transcription {final_file_name}: {str(e)}")

