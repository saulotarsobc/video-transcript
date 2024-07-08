import whisper
import torch

# Verifica se CUDA está disponível
if torch.cuda.is_available():
    print("CUDA is available")
    device = torch.device('cuda')
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available, using CPU")
    device = torch.device('cpu')

# Carrega o modelo Whisper na GPU (ou CPU se CUDA não estiver disponível)
model = whisper.load_model(
    "large",
    download_root="./temp/models",
    device=device,
)

# Transcreve o arquivo de áudio
result = model.transcribe(
    audio='audio.mp3',
    language='pt',
    task='transcribe',
    verbose=False,
    temperature=0.0,
)

# Exibe a transcrição
print(result)
