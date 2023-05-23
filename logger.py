import os
import logging

class Logger:
    def __init__(self):
        # Создание и настройка логгеров для каждого файла логов
        self.short_logger = self.setup_logger('short_logs.log')
        self.full_logger = self.setup_logger('full_logs.log')
        self.math_equirec_logger = self.setup_logger('math_equirec_logs.log')
        self.math_cubic_logger = self.setup_logger('math_cubic_logs.log')
        self.setup_handlers()
        
    def setup_logger(self, log_file):
        logger = logging.getLogger(log_file)
        logger.setLevel(logging.INFO)
        return logger
    
    def setup_handlers(self):
        # Создание папки, если она отсутствует
        log_folder = 'logs'
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
            
        short_file_handler = logging.FileHandler(os.path.join(log_folder, 'short_logs.log'))
        short_formatter = logging.Formatter('%(asctime)s:%(message)s')
        short_file_handler.setFormatter(short_formatter)
        self.short_logger.addHandler(short_file_handler)
        
        full_file_handler = logging.FileHandler(os.path.join(log_folder, 'full_logs.log'))
        full_formatter = logging.Formatter('%(asctime)s line %(lineno)d: %(message)s')
        full_file_handler.setFormatter(full_formatter)
        self.full_logger.addHandler(full_file_handler)
        
        math_equirec_logs = logging.FileHandler(os.path.join(log_folder, 'math_equirec_logs.log'))
        math_equirec_formatter = logging.Formatter('%(asctime)s:%(message)s')
        math_equirec_logs.setFormatter(math_equirec_formatter)
        self.math_equirec_logger.addHandler(math_equirec_logs)
        
        math_cubic_logs = logging.FileHandler(os.path.join(log_folder, 'math_cubic_logs.log'))
        math_cubic_formatter = logging.Formatter('%(asctime)s: %(message)s')
        math_cubic_logs.setFormatter(math_cubic_formatter)
        self.math_cubic_logger.addHandler(math_cubic_logs)
        
        
    def short_logs(self, message):
        self.short_logger.info(message)
        
        
    def full_logs(self, message):
        self.full_logger.info(message)
        
        
    def math_equirec_logs(self, message):
        self.math_equirec_logger.info(message)
        
        
    def math_cubic_logs(self, message):
        self.math_cubic_logger.info(message)