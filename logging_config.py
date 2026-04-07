"""
Configuração de Logging centralizada

Configura o sistema de logging do bot com handlers para:
- Console (stdout)
- Arquivo (bot.log)
- Formatação padronizada
"""

import logging
import logging.handlers
import os
from config import Config


def setup_logging() -> None:
    """
    Configura o sistema de logging do bot
    
    Cria logs em:
    - Console: INFO e acima
    - Arquivo: DEBUG e acima (mais detalhado)
    """
    
    # Root logger
    root_logger = logging.getLogger()
    
    # Se já tem handlers, não adiciona novamente (evita duplicação)
    if root_logger.hasHandlers():
        return
    
    root_logger.setLevel(logging.DEBUG)
    
    # Criar diretório de logs se não existir
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Formato padronizado
    formatter = logging.Formatter(Config.LOG_FORMAT)
    
    # ==================== HANDLER CONSOLE ====================
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # ==================== HANDLER ARQUIVO ====================
    
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            Config.LOG_FILE,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,               # Manter 5 backups
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        console_handler.emit(
            logging.LogRecord(
                name="logging_config",
                level=logging.WARNING,
                pathname="",
                lineno=0,
                msg=f"Não foi possível criar handler de arquivo: {e}",
                args=(),
                exc_info=None
            )
        )
    
    # ==================== LOGGERS ESPECÍFICOS ====================
    
    # Discord.py - reduzir verbosidade
    logging.getLogger("discord").setLevel(logging.WARNING)
    logging.getLogger("discord.http").setLevel(logging.WARNING)
    
    # Bot específico
    bot_logger = logging.getLogger("bot")
    bot_logger.setLevel(logging.DEBUG)
    
    # Log inicial
    root_logger.info(f"{'='*50}")
    root_logger.info(f"🤖 {Config.BOT_NAME} v{Config.BOT_VERSION}")
    root_logger.info(f"Logging iniciado - Level: {Config.LOG_LEVEL}")
    root_logger.info(f"Arquivo de log: {Config.LOG_FILE}")
    root_logger.info(f"{'='*50}")


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger específico para um módulo
    
    Args:
        name: Nome do módulo/logger
    
    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(name)
