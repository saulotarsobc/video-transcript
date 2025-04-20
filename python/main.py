import dotenv
import os
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
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
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# init services
transcription_service   = TranscriptionService(model_name=WHISPER_MODEL, verbose=VERBOSE)
subtitle_service        = SubtitleService()

# Create directories
folders = Folders()
folders.create_directories()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-video', methods=['POST'])
def process_video():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Missing file'}), 400

        video_file = request.files['file']
        original_filename = secure_filename(video_file.filename)
        
        socketio.emit('status', {'message': f'Starting to process {original_filename}'})
        
        # Save uploaded file
        video_path = os.path.join('temp', 'videos', original_filename)
        video_file.save(video_path)
        socketio.emit('status', {'message': 'File uploaded successfully'})

        # Transcribe
        socketio.emit('status', {'message': 'Starting transcription...'})
        transcription = transcription_service.transcribe(
            original_filename, 
            language="pt",
            task="transcribe"
        )

        if transcription is not None:
            socketio.emit('status', {'message': 'Saving transcription...'})
            transcription_service.save_transcription(transcription, original_filename)
            
            socketio.emit('status', {'message': 'Generating subtitles...'})
            subtitle_service.json_to_srt(transcription, original_filename)
            
            socketio.emit('status', {'message': 'Generating summary...'})
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
            
            socketio.emit('status', {'message': 'Processing completed!'})
            return jsonify({'message': 'Video processed successfully'}), 200
        
        return jsonify({'error': 'Transcription failed'}), 500

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        socketio.emit('status', {'message': f'Error: {str(e)}'})
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    logger.info("================= Starting application =================")
    logger.info(f"Initializing application | Port: {PORT} | Ollam Model: {OLLAMA_MODEL} | Whisper Model {WHISPER_MODEL}")
    socketio.run(app, host='0.0.0.0', port=PORT, debug=DEBUG)
