import logging

class Logger:
    def __init__(self):
        # Создание и настройка логгера для класса
        self.logger = self.setup_logger()
        self.setup_handlers()
        
    def setup_logger(self):
        logger = logging.getLogger('logger')
        logger.setLevel(logging.INFO)
        return logger
    
    def setup_handlers(self):
        # Настройка файловых обработчиков для каждого метода
        short_file_handler = logging.FileHandler('short_logs.log')
        short_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        short_file_handler.setFormatter(short_formatter)
        self.short_logs_handler = short_file_handler
        
        full_file_handler = logging.FileHandler('full_logs.log')
        full_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        full_file_handler.setFormatter(full_formatter)
        self.full_logs_handler = full_file_handler
        
    def short_logs(self, message):
        self.logger.addHandler(self.short_logs_handler)
        self.logger.info(message)
        self.logger.removeHandler(self.short_logs_handler)
        
    def full_logs(self, message):
        self.logger.addHandler(self.full_logs_handler)
        self.logger.info(message)
        self.logger.removeHandler(self.full_logs_handler)


        
        # добавить функцию для общего логирования
        # добавить для регистрации какие типы открываются файлов