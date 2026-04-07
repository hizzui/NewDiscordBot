import discord
from discord.ext import commands
import random
import re

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def dado(self, ctx: commands.Context, lados: int = 6):
        resultado = random.randint(1, lados)
        await ctx.send(f"Resultado: {resultado}")
    
    @commands.command()
    async def moeda(self, ctx: commands.Context):
        resultado = "Cara" if random.random() > 0.5 else "Coroa"
        await ctx.send(f"{resultado}!")
    
    @commands.command()
    async def vote(self, ctx: commands.Context, *, pergunta: str):
        embed = discord.Embed(title="Votação", description=pergunta, color=discord.Color.blue())
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
    
    @commands.command()
    async def calc(self, ctx: commands.Context, *, operacao: str):
        if not re.match(r'^[\d+\-*/(). ]+$', operacao):
            await ctx.send("Apenas números e operadores básicos (+, -, *, /, parênteses) são permitidos!")
            return
        try:
            resultado = eval(operacao)
            if isinstance(resultado, (int, float)):
                await ctx.send(f"{operacao} = {resultado}")
            else:
                await ctx.send("Resultado inválido!")
        except Exception as e:
            await ctx.send("Operação inválida!")

async def setup(bot):
    await bot.add_cog(Fun(bot))
