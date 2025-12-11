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
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Criado em", value=member.created_at.strftime("%d/%m/%Y"), inline=False)
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
    embed.add_field(name="Membros", value=guild.member_count, inline=False)
    embed.add_field(name="Canais", value=len(guild.channels), inline=False)
    embed.add_field(name="Criado em", value=guild.created_at.strftime("%d/%m/%Y"), inline=False)
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