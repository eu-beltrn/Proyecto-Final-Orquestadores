import os
import logging

class CentralizedLogger:
    """
    Componente de Observabilidad. Centraliza los registros de eventos
    y actúa como base de monitoreo para el pipeline.
    """
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Evitar duplicar handlers en la consola
        if not self.logger.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)
            
    def info(self, msg: str): 
        self.logger.info(msg)
        
    def warning(self, msg: str): 
        self.logger.warning(msg)
        
    def error(self, msg: str): 
        self.logger.error(msg)
        
    def critical(self, msg: str): 
        self.logger.critical(msg)