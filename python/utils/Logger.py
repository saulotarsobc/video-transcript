
from colorama import init, Fore

init(autoreset=True)


class Logger:
    def log(self, message):
        """
        A method that logs a message with a green color.

        Parameters:
            message (str): The message to be logged.

        Returns:
            None
        """
        print(f"{Fore.GREEN}\n{message}")

    def info(self, message):
        """
        A method that logs a message with a yellow color.

        Parameters:
            message (str): The message to be logged.

        Returns:
            None
        """
        print(f"{Fore.YELLOW}\n{message}")

    def error(self, message):
        """
        Print an error message in red color.

        Args:
            message (str): The error message to be printed.

        Returns:
            None
        """
        print(f"{Fore.RED}\n{message}")
