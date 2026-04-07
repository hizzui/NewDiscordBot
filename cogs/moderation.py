import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta

class Moderation(commands.Cog):
    """Sistema de moderação: banir, kickar, mutar, avisar"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "moderation_config.json"
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"users": {}, "tempbans": []}
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, membro: discord.Member, *, razao="Sem razão especificada"):
        """Coloca um membro para fora do servidor"""
        if membro == ctx.author:
            await ctx.send("❌ Você não pode kickar a si mesmo!")
            return
        
        if membro.top_role >= ctx.author.top_role:
            await ctx.send("❌ Você não tem permissão para isso!")
            return
        
        try:
            await membro.kick(reason=f"{ctx.author}: {razao}")
            embed = discord.Embed(
                title="🦶 Membro kickado",
                description=f"**{membro}** foi removido do servidor",
                color=discord.Color.orange()
            )
            embed.add_field(name="Razão", value=razao, inline=False)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erro ao kickar: {str(e)}")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, membro: discord.Member, *, razao="Sem razão especificada"):
        """Bane um membro do servidor"""
        if membro == ctx.author:
            await ctx.send("❌ Você não pode banir a si mesmo!")
            return
        
        if membro.top_role >= ctx.author.top_role:
            await ctx.send("❌ Você não tem permissão para isso!")
            return
        
        try:
            await membro.ban(reason=f"{ctx.author}: {razao}", delete_message_seconds=86400)
            embed = discord.Embed(
                title="🚫 Membro banido",
                description=f"**{membro}** foi banido do servidor",
                color=discord.Color.red()
            )
            embed.add_field(name="Razão", value=razao, inline=False)
            embed.add_field(name="Moderador", value=ctx.author.mention, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erro ao banir: {str(e)}")
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, usuario: str):
        """Remove um ban"""
        bans = await ctx.guild.bans()
        
        for ban in bans:
            if ban.user.name.lower() == usuario.lower() or str(ban.user.id) == usuario:
                try:
                    await ctx.guild.unban(ban.user, reason=f"Removido por {ctx.author}")
                    embed = discord.Embed(
                        title="✅ Ban removido",
                        description=f"**{ban.user}** teve o ban removido",
                        color=discord.Color.green()
                    )
                    await ctx.send(embed=embed)
                    return
                except Exception as e:
                    await ctx.send(f"❌ Erro: {str(e)}")
                    return
        
        await ctx.send(f"❌ Usuário **{usuario}** não encontrado na lista de bans")
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, membro: discord.Member, tempo_min: int = None, *, razao="Sem razão"):
        """Muta um usuário (remove permissão de enviar mensagens)"""
        if membro == ctx.author:
            await ctx.send("❌ Você não pode mutar a si mesmo!")
            return
        
        muted_role = discord.utils.get(ctx.guild.roles, name="Mutado")
        if not muted_role:
            try:
                muted_role = await ctx.guild.create_role(
                    name="Mutado",
                    reason="Role para usuários mutados"
                )
                # Remove permissão de enviar mensagens
                for canal in ctx.guild.text_channels:
                    await canal.set_permissions(muted_role, send_messages=False)
            except Exception as e:
                await ctx.send(f"❌ Erro ao criar role: {str(e)}")
                return
        
        try:
            await membro.add_roles(muted_role, reason=f"{ctx.author}: {razao}")
            embed = discord.Embed(
                title="🔇 Membro mutado",
                description=f"**{membro}** foi mutado",
                color=discord.Color.orange()
            )
            if tempo_min:
                embed.add_field(name="Duração", value=f"{tempo_min} minutos")
            embed.add_field(name="Razão", value=razao, inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erro ao mutar: {str(e)}")
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, membro: discord.Member):
        """Remove mute de um usuário"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Mutado")
        
        if not muted_role:
            await ctx.send("❌ Nenhum usuário está mutado")
            return
        
        try:
            await membro.remove_roles(muted_role, reason=f"Desmutado por {ctx.author}")
            embed = discord.Embed(
                title="🔊 Membro desmutado",
                description=f"**{membro}** pode enviar mensagens novamente",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Erro: {str(e)}")
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, membro: discord.Member, *, razao="Sem razão"):
        """Avisa um usuário"""
        user_id = str(membro.id)
        
        if "users" not in self.config:
            self.config["users"] = {}
        
        if user_id not in self.config["users"]:
            self.config["users"][user_id] = {"warns": 0, "motivos": []}
        
        self.config["users"][user_id]["warns"] += 1
        self.config["users"][user_id]["motivos"].append({
            "razao": razao,
            "moderador": str(ctx.author),
            "data": datetime.now().isoformat()
        })
        self.save_config()
        
        warns = self.config["users"][user_id]["warns"]
        
        embed = discord.Embed(
            title="⚠️ Aviso",
            description=f"**{membro}** recebeu um aviso",
            color=discord.Color.orange()
        )
        embed.add_field(name="Aviso #", value=warns, inline=False)
        embed.add_field(name="Razão", value=razao, inline=False)
        embed.add_field(name="Total de avisos", value=f"{warns}/3", inline=False)
        await ctx.send(embed=embed)
        
        # Auto-ban em 3 avisos
        if warns >= 3:
            try:
                await membro.ban(reason="Excedeu limite de avisos (3/3)")
                await ctx.send(f"🚫 **{membro}** foi banido automaticamente (3 avisos)")
            except:
                pass
    
    @commands.command()
    async def warnings(self, ctx, membro: discord.Member = None):
        """Mostra avisos de um usuário"""
        if not membro:
            membro = ctx.author
        
        user_id = str(membro.id)
        
        if user_id not in self.config.get("users", {}):
            await ctx.send(f"**{membro}** não tem avisos")
            return
        
        user_data = self.config["users"][user_id]
        warns = user_data["warns"]
        
        embed = discord.Embed(
            title=f"⚠️ Avisos de {membro}",
            description=f"Total: {warns}/3",
            color=discord.Color.orange()
        )
        
        for i, aviso in enumerate(user_data["motivos"], 1):
            embed.add_field(
                name=f"Aviso #{i}",
                value=f"Razão: {aviso['razao']}\nModerador: {aviso['moderador']}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unwarn(self, ctx, membro: discord.Member):
        """Remove um aviso"""
        user_id = str(membro.id)
        
        if user_id not in self.config.get("users", {}) or self.config["users"][user_id]["warns"] == 0:
            await ctx.send(f"**{membro}** não tem avisos para remover")
            return
        
        self.config["users"][user_id]["warns"] -= 1
        self.config["users"][user_id]["motivos"].pop()
        self.save_config()
        
        await ctx.send(f"✅ Um aviso de **{membro}** foi removido")


async def setup(bot):
    await bot.add_cog(Moderation(bot))
