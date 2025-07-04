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
        
        socketio.emit('status', {'step': 1, 'message': f'Starting to process {original_filename}'})
        
        # Save uploaded file
        video_path = os.path.join('temp', 'videos', original_filename)
        video_file.save(video_path)
        socketio.emit('status', {'step': 2, 'message': 'File uploaded successfully'})

        # Transcribe
        socketio.emit('status', {'step': 3, 'message': 'Starting transcription...'})
        try:
            transcription = transcription_service.transcribe(
                original_filename, 
                language="pt",
                task="transcribe"
            )
            
            if not transcription:
                logger.error("Transcription returned None")
                raise Exception("Transcription failed - no output generated")
                
            logger.info(f"Transcription successful, text length: {len(transcription.get('text', ''))}")
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            socketio.emit('status', {'step': 3, 'message': f'Transcription failed: {str(e)}'})
            return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

        # Continue with rest of process if transcription successful
        if transcription is not None:
            socketio.emit('status', {'step': 4, 'message': 'Saving transcription...'})
            transcription_service.save_transcription(transcription, original_filename)
            
            socketio.emit('status', {'step': 5, 'message': 'Generating subtitles...'})
            subtitle_service.json_to_srt(transcription, original_filename)
            
            socketio.emit('status', {'step': 6, 'message': 'Generating summary...'})
            chat = OllamaService(model=OLLAMA_MODEL, file_name=original_filename, language="pt-BR")
            summary = chat.generate_summary(transcription["text"])
            
            # Read the generated summary from file
            summary_path = os.path.join('temp', 'summaries', f'{original_filename}.txt')
            if os.path.exists(summary_path):
                with open(summary_path, 'r', encoding='utf-8') as f:
                    summary_text = f.read()
                
                socketio.emit('status', {
                    'step': 7, 
                    'message': 'Processing completed!',
                    'summary': summary_text,
                    'success': True
                })
                return jsonify({
                    'message': 'Video processed successfully',
                    'summary': summary_text,
                    'success': True
                }), 200

    except Exception as e:
        logger.error(f"Process error: {str(e)}")
        socketio.emit('status', {'message': f'Error: {str(e)}'})
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    logger.info("================= Starting application =================")
    logger.info(f"Initializing application | Port: {PORT} | Ollam Model: \"{OLLAMA_MODEL}\" | Whisper Model \"{WHISPER_MODEL}\"")
    socketio.run(app, host='0.0.0.0', port=PORT, debug=DEBUG)
