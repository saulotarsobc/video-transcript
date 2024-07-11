#! bash
echo -e "\033[0;33m\n\nCreate virtual environment:\033[0m"
python -m venv .venv;
source .venv/Scripts/activate; # windows
echo -e "\033[0;33mActivate virtual environment: $VIRTUAL_ENV\033[0m"

echo -e "\n\n\033[0;33mInstall requirements:\033[0m"
python.exe -m pip install --upgrade pip
pip install -U openai-whisper;
pip install numpy==1.23.5;
pip install python-dotenv==1.0.1;
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118;
echo -e "\033[0;33mDone!\033[0m"


echo -e "\n\n\033[0;33mRun test:\033[0m"
python code/transcript.py;