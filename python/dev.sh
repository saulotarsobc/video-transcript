#! bash
python3 -m venv .venv;

source .venv/Scripts/activate; # windows

pip install numpy==1.23.5;
pip install python-dotenv==1.0.1;
pip install requests==2.32.3;
pip install -U openai-whisper;

