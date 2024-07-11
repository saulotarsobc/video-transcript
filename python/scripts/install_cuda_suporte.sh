#! bash
python -m venv .venv;
source .venv/Scripts/activate; # windows

python.exe -m pip install --upgrade pip

pip install -U openai-whisper;
pip install numpy==1.23.5;
pip install python-dotenv==1.0.1;
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118;

echo "Run test:";
python code/transcript.py;
