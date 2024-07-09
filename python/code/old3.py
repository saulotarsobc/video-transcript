import whisper
import json
import datetime
import logging
import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

BASE_URL = os.getenv('BASE_URL')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route('/transcribe/<int:id>', methods=['POST'])
def transcribe(id):

    if id is None:
        return {'error': 'id is required'}, 400

    try:
        body = request.get_json() or {}

        language = body.get('language') or 'pt'
        task = body.get('task') or 'transcribe'
        initial_prompt = body.get('initial_prompt') or ''
        model_name = body.get('model_name') or 'tiny'

        file = f'./temp/{id}.mp4'
        model = whisper.load_model(model_name, download_root="temp")

        result = model.transcribe(
            audio=file,
            language=language,
            task=task,
            initial_prompt=initial_prompt,
            # verbose=True,
            # logprob_threshold=0.5,
            # word_timestamps=True
        )

        return result, 200
    except Exception as e:
        logger.error(e)
        return {'error': str(e)}, 500


if __name__ == '__main__':
    port = os.getenv('PORT')
    debug = os.getenv('ENV') == 'development'
    logger.info(f'Iniciando aplicação Flask. Debug={debug}, Port={port}')
    app.run(host='0.0.0.0', port=port, debug=debug)
