"""
Configurações centralizadas do NDB Bot

Este arquivo contém todas as configurações do bot em um único lugar,
facilitando manutenção e alterações.
"""

import os
from typing import Final
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


class Config:
    """Classe para armazenar configurações do bot"""
    
    # ==================== DISCORD ====================
    
    DISCORD_TOKEN: Final[str] = os.getenv("DISCORD_TOKEN", "")
    COMMAND_PREFIX: Final[str] = "!"
    BOT_NAME: Final[str] = "NDB Bot"
    BOT_VERSION: Final[str] = "1.0.0"
    
    # Intents do bot
    INTENTS_MESSAGE_CONTENT: Final[bool] = True
    INTENTS_VOICE_STATES: Final[bool] = True
    
    # ==================== TWITCH API ====================
    
    TWITCH_CLIENT_ID: Final[str] = os.getenv("TWITCH_CLIENT_ID", "")
    TWITCH_CLIENT_SECRET: Final[str] = os.getenv("TWITCH_CLIENT_SECRET", "")
    TWITCH_TOKEN: Final[str] = os.getenv("TWITCH_TOKEN", "")
    TWITCH_CHECK_INTERVAL: Final[int] = 15  # minutos
    
    # ==================== TIMEOUTS ====================
    
    HELP_MENU_TIMEOUT: Final[int] = 300  # 5 minutos
    REACTION_TIMEOUT: Final[int] = 300   # 5 minutos
    TRIVIA_QUESTION_TIMEOUT: Final[int] = 10  # segundos
    PAYDAY_COOLDOWN: Final[int] = 86400  # 24 horas em segundos
    
    # ==================== ECONOMIA ====================
    
    STARTING_BALANCE: Final[int] = 0
    PAYDAY_AMOUNT: Final[int] = 100
    SLOTS_MIN_BET: Final[int] = 10
    SLOTS_MAX_BET: Final[int] = 1000
    
    # Multiplicadores de slots
    SLOTS_JACKPOT_MULTIPLIER: Final[int] = 20  # 3x7
    SLOTS_THREE_MATCH_MULTIPLIER: Final[int] = 10  # 3 símbolos iguais
    SLOTS_TWO_MATCH_MULTIPLIER: Final[int] = 2  # 2 símbolos iguais
    
    # ==================== MODERAÇÃO ====================
    
    WARN_THRESHOLD: Final[int] = 3  # Número de avisos para auto-ban
    MUTE_ROLE_NAME: Final[str] = "Mutado"
    
    # ==================== TRIVIA ====================
    
    TRIVIA_QUESTIONS_PER_SESSION: Final[int] = 5
    TRIVIA_QUESTION_TIMEOUT_SECS: Final[int] = 10
    
    # ==================== LOGGING ====================
    
    LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Final[str] = "bot.log"
    LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # ==================== ARQUIVOS DE CONFIGURAÇÃO ====================
    
    CONFIG_DIR: Final[str] = "config"
    DATA_DIR: Final[str] = "data"
    
    # Arquivos JSON de persistência
    MODERATION_CONFIG_FILE: Final[str] = "data/moderation_config.json"
    ECONOMY_CONFIG_FILE: Final[str] = "data/economy_config.json"
    CUSTOMCOM_CONFIG_FILE: Final[str] = "data/customcom_config.json"
    STREAMS_CONFIG_FILE: Final[str] = "data/streams_config.json"
    TRIVIA_SCORES_FILE: Final[str] = "data/trivia_scores.json"
    
    # ==================== VALIDAÇÃO ====================
    
    @classmethod
    def validate(cls) -> bool:
        """
        Valida se as configurações obrigatórias estão definidas
        
        Returns:
            bool: True se válido, False caso contrário
        """
        required_vars = [
            ("DISCORD_TOKEN", cls.DISCORD_TOKEN),
            ("TWITCH_CLIENT_ID", cls.TWITCH_CLIENT_ID),
            ("TWITCH_TOKEN", cls.TWITCH_TOKEN),
        ]
        
        missing = []
        for var_name, var_value in required_vars:
            if not var_value:
                missing.append(var_name)
        
        if missing:
            print(f"❌ Variáveis de ambiente faltando: {', '.join(missing)}")
            return False
        
        print("✅ Todas as variáveis de ambiente configuradas")
        return True
    
    @classmethod
    def info(cls) -> None:
        """Exibe informações sobre as configurações"""
        print(f"\n{'='*50}")
        print(f"🤖 {cls.BOT_NAME} v{cls.BOT_VERSION}")
        print(f"{'='*50}")
        print(f"Prefix: {cls.COMMAND_PREFIX}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"Twitch Check Interval: {cls.TWITCH_CHECK_INTERVAL} min")
        print(f"Help Timeout: {cls.HELP_MENU_TIMEOUT}s")
        print(f"{'='*50}\n")


# Validar configurações na importação
if __name__ == "__main__":
    Config.validate()
    Config.info()
