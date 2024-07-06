## Help

- [How to Install & Use Whisper AI Voice to Text](https://youtu.be/ABFqbY_rmEk)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [Download Model #63](https://github.com/openai/whisper/discussions/63)
- [ffmpeg](https://www.ffmpeg.org/)
- [Best FREE Speech to Text AI - Whisper AI](https://youtu.be/8SQV-B83tPU)
- [How to Install & Use Whisper AI Voice to Text](https://youtu.be/ABFqbY_rmEk)

## Start

### on local

```sh
python3 -m venv .venv;
source .venv/Scripts/activate; # windows
source .venv/bin/activate; # linux
pip install -r requirements.txt;

python main.py;

whisper \
    --model_dir temp \
    --model tiny audio.wav \
    --output_dir temp \
    -f json --language en;
```

```sh
# converter para audio com corte de tamanho
ffmpeg -y -i aula.mp4 -ss 00:00:13 -to 00:00:34 -c:v copy -c:a copy output_video.mp4 && ffmpeg -y -i output_video.mp4 audio.wav

# converter para audio sem corte de tamanho
ffmpeg -y -i aula.mp4 -c:v copy -c:a copy output_video.mp4 && ffmpeg -y -i output_video.mp4 audio.wav

# juntar um video com uma legenda
ffmpeg -i aula.mp4 -i aula.srt -c copy -c:s mov_text -metadata:s:s:0 language=pt -metadata:s:s:0 title=Portuguese aula_legendada.mp4 -y;
```
