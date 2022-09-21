import logging
import sys

class Logger:
    logger = None
    
    def __init__(self) -> None:    
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.setFormatter(formatter)

        file_handler = logging.FileHandler('logs.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)


        self.logger.addHandler(file_handler)
        self.logger.addHandler(stdout_handler)