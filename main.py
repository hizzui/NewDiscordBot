import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Importar configurações centralizadas
from config import Config
from logging_config import setup_logging, get_logger

# Configurar logging
setup_logging()
logger = get_logger(__name__)

load_dotenv()

# Configurar intents
intents = discord.Intents.default()
intents.message_content = Config.INTENTS_MESSAGE_CONTENT
intents.voice_states = Config.INTENTS_VOICE_STATES

# Criar bot com prefix e intents
bot = commands.Bot(command_prefix=Config.COMMAND_PREFIX, intents=intents)
bot.remove_command('help')  # Desabilitar o comando help padrão


async def update_presence():
    """Atualiza a presença do bot em tempo real"""
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{Config.COMMAND_PREFIX}ajuda | {len(bot.guilds)} servidores"
    )
    await bot.change_presence(activity=activity, status=discord.Status.idle)
    logger.debug(f"Presença atualizada: {len(bot.guilds)} servidores")


# Event listener para quando o bot se conecta
@bot.event
async def on_ready():
    """Configura a presença do bot quando se conecta"""
    try:
        await update_presence()
        logger.info(f"✅ Bot Online: {bot.user}")
        logger.info(f"📊 Servidores conectados: {len(bot.guilds)}")
        logger.info(f"👥 Usuários totais: {sum(guild.member_count for guild in bot.guilds)}")
    except Exception as e:
        logger.error(f"Erro ao configurar presença: {e}")


@bot.event
async def on_guild_join(guild):
    """Atualiza presença quando bot entra em um servidor"""
    try:
        await update_presence()
        logger.info(f"✅ Bot adicionado a: {guild.name} ({len(bot.guilds)} servidores totais)")
    except Exception as e:
        logger.error(f"Erro ao atualizar presença: {e}")


@bot.event
async def on_guild_remove(guild):
    """Atualiza presença quando bot é removido de um servidor"""
    try:
        await update_presence()
        logger.info(f"❌ Bot removido de: {guild.name} ({len(bot.guilds)} servidores totais)")
    except Exception as e:
        logger.error(f"Erro ao atualizar presença: {e}")


async def load_cogs():
    """Carrega todos os cogs da pasta cogs/"""
    cogs_loaded = 0
    cogs_failed = 0
    
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"✅ Carregado: {filename}")
                cogs_loaded += 1
            except Exception as e:
                logger.error(f"❌ Erro ao carregar {filename}: {e}")
                cogs_failed += 1
    
    logger.info(f"Cogs: {cogs_loaded} carregados, {cogs_failed} falhados")
    return cogs_loaded > 0


async def main():
    """Função principal - inicia o bot"""
    # Validar configurações
    if not Config.validate():
        logger.error("Configurações inválidas. Abortando...")
        exit(1)
    
    # Exibir informações
    Config.info()
    
    # Iniciar bot
    async with bot:
        # Carregar cogs
        if not await load_cogs():
            logger.warning("Nenhum cog foi carregado com sucesso!")
        
        # Obter token e iniciar
        TOKEN = Config.DISCORD_TOKEN
        if not TOKEN:
            logger.error("DISCORD_TOKEN não foi configurado em .env")
            exit(1)
        
        try:
            await bot.start(TOKEN)
        except discord.LoginFailure:
            logger.error("Token inválido. Verifique DISCORD_TOKEN em .env")
            exit(1)
        except Exception as e:
            logger.error(f"Erro ao iniciar bot: {e}")
            exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot interrompido pelo usuário")
    except Exception as e:
        logger.critical(f"Erro crítico: {e}", exc_info=True)
