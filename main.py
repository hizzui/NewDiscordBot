import discord 
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
    embed.add_field(name="Dono", value=guild.owner.mention, inline=True)
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

TOKEN = "TOKEN_DO_SEU_BOT"
bot.run(TOKEN)