import dotenv
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

from utils.Logger import logger
from utils.Folders import Folders

from services.TranscriptionService import TranscriptionService
from services.SubtitleService import SubtitleService
from services.OllamaService import OllamaService

# env
dotenv.load_dotenv()
PORT            = os.getenv("PORT")
VERBOSE         = os.getenv("VERBOSE") == 'True'
WHISPER_MODEL   = os.getenv("WHISPER_MODEL") or "tiny"
DEBUG           = os.getenv("DEBUG") == 'True'
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL") or "llama3.2"

# init Flask
app = Flask(__name__)

# init services
transcription_service   = TranscriptionService(WHISPER_MODEL, VERBOSE)
subtitle_service        = SubtitleService()

# Create directories
folders = Folders()
folders.create_directories()

@app.route('/process-video', methods=['POST'])
def process_video():
    try:
        if 'file' not in request.files or 'name' not in request.form:
            return jsonify({'error': 'Missing file or name'}), 400

        video_file = request.files['file']
        original_filename = secure_filename(video_file.filename)
        display_name = request.form['name']
        
        logger.info(f"Processing video: {display_name} (File: {original_filename})")
        
        # Save uploaded file to temp/videos with original filename
        video_path = os.path.join('temp', 'videos', original_filename)
        video_file.save(video_path)

        transcription = transcription_service.transcribe(
            original_filename, 
            language="pt",
            task="transcribe"
        )

        if transcription is not None:
            transcription_service.save_transcription(transcription, original_filename)
            subtitle_service.json_to_srt(transcription, original_filename)
            
            chat = OllamaService(model=OLLAMA_MODEL, file_name=original_filename)
            prompt = f"""Analyze the following transcript and create a comprehensive summary. Focus on:
1. Main topic or central theme
2. Key points and important details
3. Major conclusions or outcomes
4. Important names, dates, or specific data mentioned

Please structure the summary in clear paragraphs and maintain a professional tone.

Transcript:
{transcription["text"]}

Generate a summary in Portuguese:"""

            chat.generate_summary(prompt)
            
            return jsonify({'message': 'Video processed successfully'}), 200
        
        return jsonify({'error': 'Transcription failed'}), 500

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    logger.info(f"\n\nInitializing application: Wispher Model: {WHISPER_MODEL} | Ollama Model: {OLLAMA_MODEL}\n")
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
