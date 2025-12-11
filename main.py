import discord 
from discord.ext import commands
import random
import asyncio
import yt_dlp
from discord.ext.commands import Bot
from discord import FFmpegPCMAudio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

music_queues = {}
is_playing = {}
current_song = {}

class MusicPlayer:
    def __init__(self, bot):
        self.bot = bot
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'default_search': 'ytsearch',
            'quiet': True,
            'no_warnings': True,
        }
    
    async def search_youtube(self, query):
        ydl_opts = self.ydl_opts.copy()
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                loop = asyncio.get_event_loop()
                info = await loop.run_in_executor(None, lambda: ydl.extract_info(query, download=False))
                if info:
                    return {
                        'title': info.get('title'),
                        'url': info.get('webpage_url'),
                        'duration': info.get('duration'),
                        'thumbnail': info.get('thumbnail'),
                        'source': 'YouTube'
                    }
        except Exception as e:
            return None
    
    async def get_audio_url(self, url):
        ydl_opts = self.ydl_opts.copy()
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                loop = asyncio.get_event_loop()
                info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))
                if info:
                    return info.get('url')
        except:
            return None

music_player = MusicPlayer(bot)

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")

@bot.command()
async def ping(ctx: commands.Context):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Latência: {latency}ms")

@bot.command()
async def oi(ctx: commands.Context):
    await ctx.send(f"Olá {ctx.author.mention}! 👋")

@bot.command()
async def echo(ctx: commands.Context, *, texto: str):
    await ctx.send(texto)

@bot.command()
async def ajuda(ctx: commands.Context):
    embed = discord.Embed(title="📋 Comandos Disponíveis", color=discord.Color.blue())
    embed.add_field(name="!ping", value="Mostra a latência do bot", inline=False)
    embed.add_field(name="!oi", value="Sauda você", inline=False)
    embed.add_field(name="!echo [texto]", value="Repete o que você escrever", inline=False)
    embed.add_field(name="!user [@usuario]", value="Mostra informações do usuário", inline=False)
    embed.add_field(name="!dado [lados]", value="Rola um dado", inline=False)
    embed.add_field(name="!moeda", value="Joga uma moeda", inline=False)
    embed.add_field(name="!servidor", value="Mostra info do servidor", inline=False)
    embed.add_field(name="!avatar [@usuario]", value="Mostra o avatar", inline=False)
    embed.add_field(name="!calc [operação]", value="Calcula uma operação", inline=False)
    embed.add_field(name="!vote [pergunta]", value="Cria uma votação", inline=False)
    embed.add_field(name="🎵 COMANDOS DE MÚSICA", value="━━━━━━━━━━━━━━━━━━", inline=False)
    embed.add_field(name="!play [música/link]", value="Toca uma música do YouTube", inline=False)
    embed.add_field(name="!pause", value="Pausa a música", inline=False)
    embed.add_field(name="!resume", value="Retoma a música", inline=False)
    embed.add_field(name="!skip", value="Pula para próxima música", inline=False)
    embed.add_field(name="!stop", value="Para a música e limpa a fila", inline=False)
    embed.add_field(name="!fila", value="Mostra a fila de músicas", inline=False)
    embed.add_field(name="!atual", value="Mostra música tocando agora", inline=False)
    embed.add_field(name="!volume [0-100]", value="Ajusta o volume", inline=False)
    
    embed.add_field(name="!ajuda", value="Mostra este menu", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def user(ctx: commands.Context, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Informações de {member.name}", color=discord.Color.green())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Nome de Usuário", value=f"@{member.name}", inline=False)
    embed.add_field(name="Display Name", value=member.display_name, inline=True)
    embed.add_field(name="Bot", value="✅ Sim" if member.bot else "❌ Não", inline=True)
    embed.add_field(name="Conta Criada em", value=member.created_at.strftime("%d/%m/%Y às %H:%M"), inline=False)
    embed.add_field(name="Entrou no Servidor em", value=member.joined_at.strftime("%d/%m/%Y às %H:%M"), inline=False)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Atividade", value=member.activity.name if member.activity else "Nenhuma", inline=True)
    roles = [role.mention for role in member.roles if role.name != "@everyone"]
    embed.add_field(name="Cargos", value=", ".join(roles) if roles else "Nenhum cargo", inline=False)
    embed.add_field(name="Cor do Perfil", value=str(member.color), inline=True)
    embed.add_field(name="Tem Permissão de Admin", value="✅ Sim" if member.guild_permissions.administrator else "❌ Não", inline=True)
    embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def dado(ctx: commands.Context, lados: int = 6):
    resultado = random.randint(1, lados)
    await ctx.send(f"🎲 Resultado: {resultado}")

@bot.command()
async def moeda(ctx: commands.Context):
    resultado = "Cara" if random.random() > 0.5 else "Coroa"
    await ctx.send(f"🪙 {resultado}!")

@bot.command()
async def servidor(ctx: commands.Context):
    guild = ctx.guild
    embed = discord.Embed(title=f"Informações de {guild.name}", color=discord.Color.purple())
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="ID do Servidor", value=guild.id, inline=False)
    embed.add_field(name="Dono", value=guild.owner.mention if guild.owner else "Desconhecido", inline=True)
    embed.add_field(name="Região", value=str(guild.region) if hasattr(guild, 'region') else "Automática", inline=True)
    embed.add_field(name="Membros Totais", value=guild.member_count, inline=True)
    embed.add_field(name="Membros Humanos", value=sum(1 for m in guild.members if not m.bot), inline=True)
    embed.add_field(name="Bots", value=sum(1 for m in guild.members if m.bot), inline=True)
    embed.add_field(name="Canais de Texto", value=len([c for c in guild.channels if isinstance(c, discord.TextChannel)]), inline=True)
    embed.add_field(name="Canais de Voz", value=len([c for c in guild.channels if isinstance(c, discord.VoiceChannel)]), inline=True)
    embed.add_field(name="Categorias", value=len([c for c in guild.channels if isinstance(c, discord.CategoryChannel)]), inline=True)
    embed.add_field(name="Cargos", value=len(guild.roles), inline=True)
    embed.add_field(name="Emojis", value=len(guild.emojis), inline=True)
    embed.add_field(name="Verificação", value=guild.verification_level.name.title(), inline=True)
    embed.add_field(name="Filtro de Conteúdo", value=guild.explicit_content_filter.name.title(), inline=True)
    embed.add_field(name="Servidor Criado em", value=guild.created_at.strftime("%d/%m/%Y às %H:%M"), inline=False)
    embed.add_field(name="Boosters", value=guild.premium_subscription_count, inline=True)
    embed.add_field(name="Nível de Boost", value=f"Nível {guild.premium_tier}", inline=True)
    embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def avatar(ctx: commands.Context, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"Avatar de {member.name}", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def calc(ctx: commands.Context, *, operacao: str):
    try:
        resultado = eval(operacao)
        await ctx.send(f"📊 {operacao} = {resultado}")
    except:
        await ctx.send("❌ Operação inválida!")

@bot.command()
async def vote(ctx: commands.Context, *, pergunta: str):
    embed = discord.Embed(title="📊 Votação", description=pergunta, color=discord.Color.blue())
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")

@bot.command()
async def play(ctx: commands.Context, *, query: str):
    if not ctx.author.voice:
        embed = discord.Embed(description="❌ Você precisa estar em um canal de voz!", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    channel = ctx.author.voice.channel
    
    if ctx.voice_client is None:
        await channel.connect()
    elif ctx.voice_client.channel != channel:
        await ctx.voice_client.move_to(channel)
    
    search_embed = discord.Embed(description="🔍 Buscando música...", color=discord.Color.yellow())
    msg = await ctx.send(embed=search_embed)
    
    song_info = await music_player.search_youtube(query)
    
    if not song_info:
        error_embed = discord.Embed(description="❌ Não encontrei essa música!", color=discord.Color.red())
        await msg.edit(embed=error_embed)
        return
    
    if ctx.guild.id not in music_queues:
        music_queues[ctx.guild.id] = []
        is_playing[ctx.guild.id] = False
    
    music_queues[ctx.guild.id].append(song_info)
    
    embed = discord.Embed(title="🎵 Adicionado à Fila", color=discord.Color.green())
    embed.add_field(name="Título", value=song_info['title'], inline=False)
    embed.add_field(name="Duração", value=f"{song_info['duration']//60}:{song_info['duration']%60:02d}", inline=True)
    embed.add_field(name="Posição na Fila", value=len(music_queues[ctx.guild.id]), inline=True)
    if song_info.get('thumbnail'):
        embed.set_thumbnail(url=song_info['thumbnail'])
    await msg.edit(embed=embed)
    
    if not is_playing[ctx.guild.id]:
        await play_next_song(ctx)

async def play_next_song(ctx):
    guild_id = ctx.guild.id
    
    if guild_id not in music_queues or not music_queues[guild_id]:
        is_playing[guild_id] = False
        current_song[guild_id] = None
        return
    
    is_playing[guild_id] = True
    song = music_queues[guild_id].pop(0)
    current_song[guild_id] = song
    
    audio_url = await music_player.get_audio_url(song['url'])
    
    if not audio_url:
        await ctx.send("❌ Erro ao obter áudio da música")
        await play_next_song(ctx)
        return
    
    try:
        source = FFmpegPCMAudio(audio_url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn")
        
        def after_playing(error):
            if error:
                print(f"Erro ao tocar: {error}")
            asyncio.run_coroutine_threadsafe(play_next_song(ctx), bot.loop)
        
        ctx.voice_client.play(source, after=after_playing)
        
        embed = discord.Embed(title="🎵 Tocando Agora", color=discord.Color.green())
        embed.add_field(name="Título", value=song['title'], inline=False)
        embed.add_field(name="Duração", value=f"{song['duration']//60}:{song['duration']%60:02d}", inline=True)
        embed.add_field(name="Próximas na Fila", value=len(music_queues[guild_id]) or "Nenhuma", inline=True)
        if song.get('thumbnail'):
            embed.set_thumbnail(url=song['thumbnail'])
        embed.set_footer(text="Use !pause, !resume, !skip, !stop para controlar")
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Erro ao reproduzir: {e}")
        await play_next_song(ctx)

@bot.command()
async def pause(ctx: commands.Context):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        embed = discord.Embed(description="⏸️ Música pausada", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="❌ Nenhuma música tocando", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def resume(ctx: commands.Context):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        embed = discord.Embed(description="▶️ Música retomada", color=discord.Color.green())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="❌ Nenhuma música pausada", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def skip(ctx: commands.Context):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        embed = discord.Embed(description="⏭️ Música pulada", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="❌ Nenhuma música tocando", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def stop(ctx: commands.Context):
    if ctx.voice_client:
        ctx.voice_client.stop()
        music_queues[ctx.guild.id] = []
        is_playing[ctx.guild.id] = False
        current_song[ctx.guild.id] = None
        embed = discord.Embed(description="⏹️ Música parada. Fila limpa.", color=discord.Color.red())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="❌ Bot não está em nenhum canal de voz", color=discord.Color.red())
        await ctx.send(embed=embed)

@bot.command()
async def fila(ctx: commands.Context):
    guild_id = ctx.guild.id
    
    if guild_id not in music_queues or not music_queues[guild_id]:
        embed = discord.Embed(description="📭 Fila vazia", color=discord.Color.yellow())
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(title="📋 Fila de Músicas", color=discord.Color.blue())
    
    for i, song in enumerate(music_queues[guild_id], 1):
        duration = f"{song['duration']//60}:{song['duration']%60:02d}"
        embed.add_field(
            name=f"#{i} - {song['title'][:50]}",
            value=f"⏱️ {duration}",
            inline=False
        )
    
    embed.set_footer(text=f"Total: {len(music_queues[guild_id])} música(s)")
    await ctx.send(embed=embed)

@bot.command()
async def atual(ctx: commands.Context):
    guild_id = ctx.guild.id
    
    if guild_id not in current_song or not current_song[guild_id]:
        embed = discord.Embed(description="❌ Nenhuma música tocando", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
    
    song = current_song[guild_id]
    embed = discord.Embed(title="🎵 Tocando Agora", color=discord.Color.green())
    embed.add_field(name="Título", value=song['title'], inline=False)
    embed.add_field(name="Duração", value=f"{song['duration']//60}:{song['duration']%60:02d}", inline=True)
    embed.add_field(name="Fonte", value=song['source'], inline=True)
    if song.get('thumbnail'):
        embed.set_thumbnail(url=song['thumbnail'])
    await ctx.send(embed=embed)

@bot.command()
async def disconnect(ctx: commands.Context):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        embed = discord.Embed(description="👋 Bot desconectado do canal de voz", color=discord.Color.blue())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description="❌ Bot não está em nenhum canal de voz", color=discord.Color.red())
        await ctx.send(embed=embed)

TOKEN = "SEU_TOKEN_AQUI"
bot.run(TOKEN)