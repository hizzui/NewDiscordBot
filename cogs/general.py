"""
Cog de Utilidades Gerais e Menu de Ajuda
Estrutura similar ao Red-DiscordBot
"""

import discord
from discord.ext import commands
import asyncio
import logging
from typing import Optional
from config import Config


class General(commands.Cog):
    """Comandos gerais e menu de ajuda"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    # ==================== EVENTOS ====================
    
    @commands.Cog.listener()
    async def on_ready(self):
        """Evento disparado quando o bot está pronto"""
        print(f"Bot online como {self.bot.user}")

    # ==================== COMANDOS DE INFORMAÇÃO ====================
    
    @commands.command(
        name="ping",
        brief="Mostra a latência do bot",
        help="Retorna a latência atual do bot em milissegundos"
    )
    async def ping(self, ctx: commands.Context) -> None:
        """Mostra a latência do bot"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! 🏓 Latência: {latency}ms")

    @commands.command(
        name="oi",
        brief="O bot sauda você",
        help="Receba uma saudação do bot"
    )
    async def oi(self, ctx: commands.Context) -> None:
        """Sauda o usuário"""
        await ctx.send(f"Olá {ctx.author.mention}! 👋")

    @commands.command(
        name="echo",
        brief="Repete seu texto",
        help="O bot repete qualquer texto que você enviar"
    )
    async def echo(self, ctx: commands.Context, *, texto: str) -> None:
        """Repete o texto do usuário"""
        await ctx.send(texto)

    # ==================== MENU DE AJUDA ====================
    
    @commands.command(
        name="ajuda",
        brief="Menu de ajuda",
        help="Exibe todos os comandos disponíveis."
    )
    async def ajuda(self, ctx: commands.Context) -> None:
        """Menu de ajuda simplificado - sem paginação"""
        self.logger.info(f"[AJUDA] Comando executado por {ctx.author}")
        
        embed = discord.Embed(
            title="📚 Menu de Ajuda - NDB Bot",
            description="Bem-vindo ao **NewDiscordBot**! Aqui estão todos os comandos disponíveis.",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="🔧 Gerais",
            value="`!ping` - Mostra a latência do bot\n"
                  "`!oi` - Cumprimento amigável\n"
                  "`!echo [texto]` - Repete o texto\n"
                  "`!ajuda` - Mostra este menu",
            inline=False
        )
        
        embed.add_field(
            name="😂 Diversão",
            value="`!dado` - Rola um dado\n"
                  "`!moeda` - Joga uma moeda\n"
                  "`!vote [opção1|opção2|...]` - Cria votação\n"
                  "`!calc [expressão]` - Calcula expressão",
            inline=False
        )
        
        embed.add_field(
            name="💰 Economia",
            value="`!balance` - Seu saldo\n"
                  "`!pay [user] [amount]` - Paga alguém\n"
                  "`!slots [amount]` - Joga caça-níqueis\n"
                  "`!payday` - Recebe ganhos diários\n"
                  "`!leaderboard` - Top 10 mais ricos",
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ Informações",
            value="`!user [@user]` - Info do usuário\n"
                  "`!servidor` - Info do servidor\n"
                  "`!avatar [@user]` - Avatar do usuário",
            inline=False
        )
        
        embed.add_field(
            name="🔨 Moderação",
            value="`!kick [@user]` - Remove usuário\n"
                  "`!ban [@user]` - Bane usuário\n"
                  "`!unban [user_id]` - Desbane\n"
                  "`!mute [@user]` - Silencia\n"
                  "`!unmute [@user]` - Desfaz silêncio\n"
                  "`!warn [@user]` - Aviso\n"
                  "`!warnings [@user]` - Ver avisos\n"
                  "`!unwarn [@user]` - Remove aviso",
            inline=False
        )
        
        embed.add_field(
            name="🧹 Limpeza",
            value="`!purge [number]` - Deleta mensagens\n"
                  "`!clean` - Alias para purge\n"
                  "`!cleanup [number]` - Alias para purge\n"
                  "`!clear [number]` - Alias para purge",
            inline=False
        )
        
        embed.add_field(
            name="🎮 Trivia",
            value="`!trivia` - Inicia trivia\n"
                  "`!trivia_score` - Seu placar\n"
                  "`!trivia_top` - Top 10 trivias",
            inline=False
        )
        
        embed.add_field(
            name="📺 Twitch",
            value="`!stream add [channel]` - Monitora canal\n"
                  "`!stream remove [channel]` - Para monitorar\n"
                  "`!stream list` - Canais monitorados\n"
                  "`!stream check [channel]` - Status do canal",
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Personalizados",
            value="`!customcom create [name] [response]` - Cria comando\n"
                  "`!customcom delete [name]` - Deleta comando\n"
                  "`!customcom list` - Lista comandos\n"
                  "`!customcom show [name]` - Mostra resposta",
            inline=False
        )
        
        embed.set_footer(
            text=f"Solicitado por {ctx.author} | Use !help [comando] para mais info",
            icon_url=ctx.author.avatar.url
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        self.logger.info(f"[AJUDA] Enviando embed")
        await ctx.send(embed=embed)
        self.logger.info(f"[AJUDA] Embed enviado com sucesso")

    # ==================== MÉTODOS PRIVADOS ====================
    
    def _get_help_pages(self) -> list:
        """
        Retorna as páginas do menu de ajuda.
        Estrutura similar ao Red-DiscordBot.
        """
        return [
            # Página 1: Início
            {
                "title": "📋 Central de Ajuda - NDB Bot",
                "description": (
                    "Bem-vindo! Use ◀️ e ▶️ para navegar entre as páginas de ajuda.\n"
                    "Este bot possui diversos comandos organizados por categoria."
                ),
                "color": discord.Color.blue(),
                "fields": [
                    {
                        "name": "📖 Categorias Disponíveis",
                        "value": (
                            "1️⃣ **Início** - Você está aqui!\n"
                            "2️⃣ **Moderação** - Gerenciar membros\n"
                            "3️⃣ **Economia** - Sistema de créditos\n"
                            "4️⃣ **Trivia** - Quiz com 50+ perguntas\n"
                            "5️⃣ **Customização** - Criar comandos personalizados\n"
                            "6️⃣ **Streams** - Monitorar livestreams Twitch\n"
                            "7️⃣ **Utilitários** - Comandos gerais\n"
                            "8️⃣ **Limpeza** - Deletar mensagens"
                        ),
                        "inline": False
                    },
                    {
                        "name": "💡 Como Usar",
                        "value": (
                            "• Use as reações para navegar entre páginas\n"
                            "• Digite `!comando --help` para mais info sobre um comando\n"
                            "• Todos os comandos começam com `!`"
                        ),
                        "inline": False
                    },
                ]
            },
            
            # Página 2: Moderação
            {
                "title": "🔒 Moderação",
                "description": "Gerenciar e disciplinar membros do servidor",
                "color": discord.Color.red(),
                "fields": [
                    {
                        "name": "Banimento & Remoção",
                        "value": (
                            "`!kick [@user] [razão]` - Remove membro\n"
                            "`!ban [@user] [razão]` - Bane permanentemente\n"
                            "`!unban [user]` - Remove banimento"
                        ),
                        "inline": False
                    },
                    {
                        "name": "Silenciamento",
                        "value": (
                            "`!mute [@user]` - Muta usuário (cria role Mutado)\n"
                            "`!unmute [@user]` - Remove silenciamento"
                        ),
                        "inline": False
                    },
                    {
                        "name": "Sistema de Avisos",
                        "value": (
                            "`!warn [@user] [razão]` - Avisa usuário (3 avisos = auto-ban)\n"
                            "`!warnings [@user]` - Ver avisos do usuário\n"
                            "`!unwarn [@user]` - Remove um aviso"
                        ),
                        "inline": False
                    },
                ]
            },
            
            # Página 3: Economia
            {
                "title": "💰 Economia & Moeda",
                "description": "Ganhe e gaste créditos com nosso sistema econômico",
                "color": discord.Color.gold(),
                "fields": [
                    {
                        "name": "Saldo & Transferências",
                        "value": (
                            "`!balance [@user]` - Mostra seu saldo\n"
                            "`!pay [@user] [valor]` - Transfere créditos\n"
                            "`!leaderboard [top]` - Ranking de maiores saldos"
                        ),
                        "inline": False
                    },
                    {
                        "name": "Ganhos & Apostas",
                        "value": (
                            "`!payday` - Recebe R$100 por dia (cooldown 24h)\n"
                            "`!slots [aposta]` - Joga caça-níqueis\n"
                            "🎰 Jackpot (3x7) = 20x a aposta"
                        ),
                        "inline": False
                    },
                ]
            },
            
            # Página 4: Trivia & Diversão
            {
                "title": "🎲 Trivia & Diversão",
                "description": "Jogos e desafios para aproveitar com a comunidade",
                "color": discord.Color.green(),
                "fields": [
                    {
                        "name": "Trivia (50+ perguntas)",
                        "value": (
                            "`!trivia` - Inicia sessão de 5 perguntas\n"
                            "`!trivia_score [@user]` - Mostra pontos de alguém\n"
                            "`!trivia_top` - Ranking global de trivia"
                        ),
                        "inline": False
                    },
                    {
                        "name": "Outros Jogos",
                        "value": (
                            "`!dado [lados]` - Rola um dado\n"
                            "`!moeda` - Joga uma moeda\n"
                            "`!vote [pergunta]` - Cria votação rápida\n"
                            "`!calc [operação]` - Realiza cálculos"
                        ),
                        "inline": False
                    },
                ]
            },
            
            # Página 5: Customização
            {
                "title": "🛠️ Customização",
                "description": "Crie seus próprios comandos sem programação!",
                "color": discord.Color.purple(),
                "fields": [
                    {
                        "name": "Gerenciamento de Comandos",
                        "value": (
                            "`!customcom create [nome] [resposta]` - Cria novo comando\n"
                            "`!customcom list` - Lista todos os comandos customizados\n"
                            "`!customcom delete [nome]` - Remove comando\n"
                            "`!customcom show [nome]` - Mostra conteúdo"
                        ),
                        "inline": False
                    },
                    {
                        "name": "Variáveis Disponíveis",
                        "value": (
                            "`{author}` - Seu nome\n"
                            "`{guild}` - Nome do servidor\n"
                            "`{timestamp}` - Data/hora atual"
                        ),
                        "inline": False
                    },
                ]
            },
            
            # Página 6: Streams
            {
                "title": "📡 Streams (Twitch)",
                "description": "Monitore seus streamers favoritos em tempo real! 🎥",
                "color": discord.Color.from_rgb(145, 70, 255),
                "fields": [
                    {
                        "name": "Configuração",
                        "value": (
                            "`!streamset channel [#canal]` - Define canal para notificações\n"
                            "`!streamset credentials` - Mostra status das credenciais"
                        ),
                        "inline": False
                    },
                    {
                        "name": "Monitoramento",
                        "value": (
                            "`!stream add twitch [usuário]` - Monitora streamer\n"
                            "`!stream remove [usuário]` - Remove monitoramento\n"
                            "`!stream list` - Lista streamers em monitoramento\n"
                            "`!stream check [usuário]` - Verifica se está ao vivo"
                        ),
                        "inline": False
                    },
                    {
                        "name": "⚡ Automático",
                        "value": "Bot verifica a cada 15 minutos e avisa quando streamer vai ao vivo!",
                        "inline": False
                    },
                ]
            },
            
            # Página 7: Utilitários
            {
                "title": "⚙️ Utilitários & Informações",
                "description": "Comandos gerais e de informação",
                "color": discord.Color.greyple(),
                "fields": [
                    {
                        "name": "Bot & Servidor",
                        "value": (
                            "`!ping` - Mostra a latência do bot\n"
                            "`!servidor` - Informações do servidor\n"
                            "`!user [@user]` - Info detalhada do usuário\n"
                            "`!avatar [@user]` - Mostra avatar ampliado"
                        ),
                        "inline": False
                    },
                    {
                        "name": "Texto",
                        "value": (
                            "`!oi` - Sauda você\n"
                            "`!echo [texto]` - Repete seu texto\n"
                            "`!calc [conta]` - Faz cálculos (Exemplo: !calc 2*5+3)"
                        ),
                        "inline": False
                    },
                ]
            },
            
            # Página 8: Limpeza
            {
                "title": "🧹 Limpeza de Mensagens",
                "description": "Limpe canais de forma eficiente com estes comandos",
                "color": discord.Color.from_rgb(200, 200, 200),
                "fields": [
                    {
                        "name": "Deleção de Mensagens",
                        "value": (
                            "`!purge [qty] [@user]` - Deleta X mensagens (opcionalmente de um usuário)\n"
                            "`!clean [qty]` - Deleta apenas mensagens de bots\n"
                            "`!cleanup` - Auto-limpa mensagens do bot\n"
                            "`!clear [qty]` - Deleta X mensagens do canal"
                        ),
                        "inline": False
                    },
                ]
            },
        ]


# ==================== SETUP ====================

async def setup(bot: commands.Bot) -> None:
    """Carrega a Cog"""
    await bot.add_cog(General(bot))
