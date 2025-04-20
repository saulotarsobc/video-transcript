import ollama
from utils.Logger import logger

class OllamaService:
    def __init__(self, model=None, file_name=None, language=None):
        self.client = ollama.Client()
        self.model = model
        self.file_name = file_name
        self.language = language

    def save_sumary(self, summary):
        logger.info(f"Starting OllamaService.save_sumary for {self.file_name}...")
        try:
            with open('./temp/summaries/' + self.file_name + '.txt', 'w', encoding='utf-8') as f:
                f.write(summary)

            logger.info("Success on OllamaService.save_sumary")

        except Exception as e:
            logger.error("Error on OllamaService.save_sumary")

    def generate_summary(self, content):
        logger.info(f"Starting OllamaService.generate_summary for {self.file_name}...")

        prompt = f"""Extraia as seguintes informações da transcrição abaixo, sem interpretações ou reordenação. Use frases diretas e apenas com base no conteúdo presente.

1. Tema central
2. Pontos principais
3. Conclusões citadas

Responda na linguagem: {self.language if self.language else 'pt-BR'}
Transcrição:
{content}"""

        logger.info(f"Prompt: {prompt}")
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                     {
                        'role': 'system',
                        'content': 'Você é um assistente que resume transcrições de áudio de forma direta, objetiva, sem adicionar interpretações, apenas com base no conteúdo fornecido.'
                      },
                     {
                        'role': 'user',
                        'content': prompt,
                    }
                ])

            self.save_sumary(response['message']['content'])

            logger.info("Success on OllamaService.generate_summary")

        except Exception as e:
            logger.info("Error on OllamaService.generate_summary")
            logger.error(f'Error: {e}')

# Uso da classe
if __name__ == "__main__":
    logger.info("Starting OllamaService test...")
    chat = OllamaService(file_name='test')
    chat.chat('conte de 1 até 5 em ingles')
