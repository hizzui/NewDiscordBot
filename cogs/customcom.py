import discord
from discord.ext import commands
import json
import os

class CustomCom(commands.Cog):
    """Permite que usuários criem comandos personalizados"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "customcom_config.json"
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    @commands.group()
    async def customcom(self, ctx):
        """Gerencia comandos personalizados"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="🛠️ Comandos Personalizados",
                description="Use um dos subcomandos abaixo:",
                color=discord.Color.purple()
            )
            embed.add_field(
                name="Subcomandos",
                value="`!customcom create [nome] [resposta]` - Cria comando\n"
                      "`!customcom list` - Lista comandos\n"
                      "`!customcom delete [nome]` - Delete comando\n"
                      "`!customcom show [nome]` - Mostra resposta",
                inline=False
            )
            await ctx.send(embed=embed)
    
    @customcom.command()
    @commands.has_permissions(manage_guild=True)
    async def create(self, ctx, nome: str, *, resposta: str):
        """Cria um comando personalizado"""
        nome = nome.lower()
        
        if len(nome) < 2:
            await ctx.send("❌ Nome muito curto (mínimo 2 caracteres)")
            return
        
        if len(resposta) > 2000:
            await ctx.send("❌ Resposta muito longa (máximo 2000 caracteres)")
            return
        
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.config:
            self.config[guild_id] = {}
        
        if nome in self.config[guild_id]:
            await ctx.send(f"❌ Comando **{nome}** já existe!")
            return
        
        self.config[guild_id][nome] = {
            "resposta": resposta,
            "criado_por": str(ctx.author),
            "criado_em": str(ctx.message.created_at)
        }
        self.save_config()
        
        embed = discord.Embed(
            title="✅ Comando criado",
            description=f"Comando **!{nome}** criado com sucesso",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @customcom.command()
    async def list(self, ctx):
        """Lista todos os comandos personalizados"""
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.config or not self.config[guild_id]:
            await ctx.send("Nenhum comando personalizado neste servidor")
            return
        
        comandos = list(self.config[guild_id].keys())
        
        embed = discord.Embed(
            title="📋 Comandos Personalizados",
            description=f"Total: {len(comandos)}",
            color=discord.Color.blue()
        )
        
        # Limita a 20 por pagina
        for cmd in comandos[:20]:
            info = self.config[guild_id][cmd]
            embed.add_field(
                name=f"!{cmd}",
                value=f"Criado por: {info['criado_por']}",
                inline=False
            )
        
        if len(comandos) > 20:
            embed.set_footer(text=f"... e mais {len(comandos) - 20} comandos")
        
        await ctx.send(embed=embed)
    
    @customcom.command()
    @commands.has_permissions(manage_guild=True)
    async def delete(self, ctx, nome: str):
        """Deleta um comando personalizado"""
        nome = nome.lower()
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.config or nome not in self.config[guild_id]:
            await ctx.send(f"❌ Comando **{nome}** não encontrado")
            return
        
        del self.config[guild_id][nome]
        self.save_config()
        
        embed = discord.Embed(
            title="✅ Comando deletado",
            description=f"Comando **!{nome}** foi removido",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @customcom.command(name="show")
    async def show_com(self, ctx, nome: str):
        """Mostra o conteúdo de um comando"""
        nome = nome.lower()
        guild_id = str(ctx.guild.id)
        
        if guild_id not in self.config or nome not in self.config[guild_id]:
            await ctx.send(f"❌ Comando **{nome}** não encontrado")
            return
        
        info = self.config[guild_id][nome]
        
        embed = discord.Embed(
            title=f"Comando: !{nome}",
            description=info["resposta"],
            color=discord.Color.purple()
        )
        embed.set_footer(text=f"Criado por {info['criado_por']}")
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Listener para executar comandos personalizados"""
        if message.author.bot:
            return
        
        if not message.guild:
            return
        
        guild_id = str(message.guild.id)
        
        if guild_id not in self.config:
            return
        
        # Verifica se é comando
        if not message.content.startswith("!"):
            return
        
        # Extrai nome do comando
        try:
            cmd_name = message.content[1:].split()[0].lower()
        except:
            return
        
        if cmd_name not in self.config[guild_id]:
            return
        
        # Pega resposta e envia
        resposta = self.config[guild_id][cmd_name]["resposta"]
        
        # Substitui variáveis simples
        resposta = resposta.replace("{author}", message.author.mention)
        resposta = resposta.replace("{guild}", message.guild.name)
        resposta = resposta.replace("{timestamp}", str(message.created_at))
        
        await message.channel.send(resposta)


async def setup(bot):
    await bot.add_cog(CustomCom(bot))
