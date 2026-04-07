import discord
from discord.ext import commands, tasks
import json
import os
import random
from datetime import datetime, timedelta

class Economy(commands.Cog):
    """Sistema de economia: banco, slots, payday"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "economy_config.json"
        self.config = self.load_config()
        self.payday_loop.start()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}, "last_payday": {}}
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    def get_balance(self, user_id):
        user_id = str(user_id)
        if user_id not in self.config["users"]:
            self.config["users"][user_id] = 100  # Saldo inicial
            self.save_config()
        return self.config["users"][user_id]
    
    def set_balance(self, user_id, amount):
        self.config["users"][str(user_id)] = max(0, amount)
        self.save_config()
    
    @commands.command()
    async def balance(self, ctx, usuario: discord.User = None):
        """Mostra seu saldo ou de outro usuário"""
        if not usuario:
            usuario = ctx.author
        
        saldo = self.get_balance(usuario.id)
        
        embed = discord.Embed(
            title=f"💰 Saldo de {usuario.name}",
            description=f"**{saldo:,}** créditos",
            color=discord.Color.gold()
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def pay(self, ctx, usuario: discord.User, amount: int):
        """Transfere créditos para outro usuário"""
        if amount <= 0:
            await ctx.send("❌ Valor deve ser maior que 0")
            return
        
        saldo_autor = self.get_balance(ctx.author.id)
        
        if saldo_autor < amount:
            await ctx.send(f"❌ Saldo insuficiente! Você tem {saldo_autor:,}")
            return
        
        self.set_balance(ctx.author.id, saldo_autor - amount)
        saldo_usuario = self.get_balance(usuario.id)
        self.set_balance(usuario.id, saldo_usuario + amount)
        
        embed = discord.Embed(
            title="✅ Transferência realizada",
            description=f"**{ctx.author}** transferiu {amount:,} créditos para **{usuario}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @commands.command()
    async def slots(self, ctx, aposta: int = 10):
        """Joga máquina caça-níqueis"""
        saldo = self.get_balance(ctx.author.id)
        
        if aposta <= 0:
            await ctx.send("❌ Aposta deve ser maior que 0")
            return
        
        if saldo < aposta:
            await ctx.send(f"❌ Saldo insuficiente! Você tem {saldo:,}")
            return
        
        # Emojis dos cilindros
        emojis = ["🍒", "🍪", "🍀", "💎", "🎰", "🎲", "👑", "2️⃣", "7️⃣"]
        
        # Sorteia 3 rótulos
        rolo1 = random.choice(emojis)
        rolo2 = random.choice(emojis)
        rolo3 = random.choice(emojis)
        
        # Calcula ganho
        ganho = 0
        if rolo1 == rolo2 == rolo3:
            ganho = aposta * 20
            resultado = "🎉 JACKPOT!"
        elif rolo1 == rolo2 or rolo2 == rolo3 or rolo1 == rolo3:
            ganho = aposta * 2
            resultado = "✨ Combinação!"
        else:
            ganho = -aposta
            resultado = "❌ Perdeu"
        
        novo_saldo = saldo + ganho
        self.set_balance(ctx.author.id, novo_saldo)
        
        embed = discord.Embed(
            title="🎰 Máquina Caça-Níqueis",
            description=f"{rolo1} {rolo2} {rolo3}",
            color=discord.Color.purple()
        )
        embed.add_field(name="Resultado", value=resultado, inline=False)
        embed.add_field(name="Aposta", value=f"-{aposta:,}", inline=True)
        embed.add_field(name="Ganho", value=f"+{ganho:,}" if ganho >= 0 else f"{ganho:,}", inline=True)
        embed.add_field(name="Novo saldo", value=f"{novo_saldo:,}", inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def payday(self, ctx):
        """Recebe créditos diariamente"""
        user_id = str(ctx.author.id)
        
        if user_id in self.config["last_payday"]:
            ultima_data = datetime.fromisoformat(self.config["last_payday"][user_id])
            agora = datetime.now()
            diferenca = agora - ultima_data
            
            if diferenca < timedelta(hours=24):
                tempo_restante = timedelta(hours=24) - diferenca
                horas = int(tempo_restante.total_seconds() // 3600)
                minutos = int((tempo_restante.total_seconds() % 3600) // 60)
                await ctx.send(f"⏰ Você já recebeu hoje! Volte em {horas}h {minutos}m")
                return
        
        payday_amount = 100
        saldo = self.get_balance(ctx.author.id)
        novo_saldo = saldo + payday_amount
        self.set_balance(ctx.author.id, novo_saldo)
        self.config["last_payday"][user_id] = datetime.now().isoformat()
        self.save_config()
        
        embed = discord.Embed(
            title="💰 Payday!",
            description=f"Você recebeu **{payday_amount:,}** créditos",
            color=discord.Color.green()
        )
        embed.add_field(name="Novo saldo", value=f"{novo_saldo:,}", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def leaderboard(self, ctx, top: int = 10):
        """Mostra top jogadores por saldo"""
        if top > 50:
            top = 50
        
        # Ordena por saldo
        usuarios = sorted(
            self.config["users"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:top]
        
        embed = discord.Embed(
            title=f"🏆 Top {len(usuarios)} Jogadores",
            color=discord.Color.gold()
        )
        
        for i, (user_id, saldo) in enumerate(usuarios, 1):
            try:
                user = await self.bot.fetch_user(int(user_id))
                embed.add_field(
                    name=f"{i}. {user.name}",
                    value=f"{saldo:,} créditos",
                    inline=False
                )
            except:
                embed.add_field(
                    name=f"{i}. ID: {user_id}",
                    value=f"{saldo:,} créditos",
                    inline=False
                )
        
        await ctx.send(embed=embed)
    
    @tasks.loop(hours=24)
    async def payday_loop(self):
        """Loop para resetar payday diariamente (opcional)"""
        pass
    
    @payday_loop.before_loop
    async def before_payday_loop(self):
        await self.bot.wait_until_ready()
    
    def cog_unload(self):
        self.payday_loop.cancel()


async def setup(bot):
    await bot.add_cog(Economy(bot))
