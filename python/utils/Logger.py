import logging
import os
import colorama

# Inicializar colorama
colorama.init()

class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        level_name = record.levelname
        if self.use_color and level_name in self.LEVEL_COLORS:
            level_name_colored = self.LEVEL_COLORS[level_name] + level_name + colorama.Fore.RESET
            record.levelname = level_name_colored
        return logging.Formatter.format(self, record)

    LEVEL_COLORS = {
        'DEBUG':    colorama.Fore.CYAN,
        'INFO':     colorama.Fore.GREEN,
        'WARNING':  colorama.Fore.YELLOW,
        'ERROR':    colorama.Fore.RED,
        'CRITICAL': colorama.Fore.RED,
    }

class Logger:
    def __init__(self):
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler()
            ]
        )
        formatter = ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s", use_color=True)
        for handler in logging.root.handlers:
            handler.setFormatter(formatter)
        self.logger = logging.getLogger()

    def log(self, msg):
        self.logger.info(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

logger = Logger()
