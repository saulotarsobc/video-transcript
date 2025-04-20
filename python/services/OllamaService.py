import ollama
from utils.Logger import logger

class OllamaService:
    def __init__(self, model=None, file_name=None):
        self.model = model
        self.file_name = file_name

    def save_sumary(self, summary):
        logger.info(f"Starting OllamaService.save_sumary for {self.file_name}...")
        try:
            with open('./temp/summaries/' + self.file_name + '.txt', 'w', encoding='utf-8') as f:
                f.write(summary)

            logger.info("Success on OllamaService.save_sumary")

        except Exception as e:
            logger.error("Error on OllamaService.save_sumary")

    def chat(self, content):
        logger.info(f"Starting OllamaService.chat for {self.file_name}...")
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': content,
                }],
                
            )

            self.save_sumary(response['message']['content'])

            logger.info("Success on OllamaService.chat")

        except Exception as e:
            logger.info("Error on OllamaService.chat")
            logger.error(f'Error: {e}')


    def generate_summary(self, content):
        logger.info(f"Starting OllamaService.generate_summary for {self.file_name}...")
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': 'Gere um breve resumo de: ' + content,
                }],
            )

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
