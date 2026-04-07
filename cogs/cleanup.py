import discord
from discord.ext import commands
import asyncio

class Cleanup(commands.Cog):
    """Limpeza de mensagens e canal"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, quantidade: int = 10, usuario: discord.User = None):
        """Deleta uma quantidade de mensagens"""
        if quantidade <= 0:
            await ctx.send("❌ Quantidade deve ser maior que 0")
            return
        
        if quantidade > 1000:
            await ctx.send("❌ Máximo de 1000 mensagens por vez")
            return
        
        try:
            deleted = 0
            # Adiciona 1 à quantidade para incluir a mensagem do comando
            async for message in ctx.channel.history(limit=quantidade + 1):
                # Se especificou usuário, só deleta dele
                if usuario and message.author != usuario:
                    continue
                
                try:
                    await message.delete()
                    deleted += 1
                except:
                    pass
            
            embed = discord.Embed(
                title="✅ Limpeza concluída",
                description=f"**{deleted}** mensagens foram deletadas",
                color=discord.Color.green()
            )
            if usuario:
                embed.add_field(name="Usuário", value=usuario.mention, inline=False)
            
            msg = await ctx.send(embed=embed)
            # Deleta mensagem de confirmação após 5 segundos
            await asyncio.sleep(5)
            await msg.delete()
        
        except Exception as e:
            await ctx.send(f"❌ Erro: {str(e)}")
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, quantidade: int = 10):
        """Deleta mensagens do bot"""
        if quantidade <= 0:
            await ctx.send("❌ Quantidade deve ser maior que 0")
            return
        
        if quantidade > 1000:
            await ctx.send("❌ Máximo de 1000 mensagens por vez")
            return
        
        try:
            deleted = 0
            async for message in ctx.channel.history(limit=quantidade + 1):
                if message.author == self.bot.user or message.author.bot:
                    try:
                        await message.delete()
                        deleted += 1
                    except:
                        pass
            
            embed = discord.Embed(
                title="✅ Mensagens de bots deletadas",
                description=f"**{deleted}** mensagens de bot foram removidas",
                color=discord.Color.green()
            )
            
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
        
        except Exception as e:
            await ctx.send(f"❌ Erro: {str(e)}")
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def cleanup(self, ctx):
        """Deleta todas as mensagens do bot no canal (últimas 50)"""
        try:
            deleted = 0
            
            # Verifica últimas 50 mensagens
            async for message in ctx.channel.history(limit=50):
                if message.author == self.bot.user:
                    try:
                        await message.delete()
                        deleted += 1
                    except:
                        pass
            
            embed = discord.Embed(
                title="✅ Limpeza automática",
                description=f"**{deleted}** mensagens do NDB Bot foram removidas",
                color=discord.Color.green()
            )
            
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
        
        except Exception as e:
            await ctx.send(f"❌ Erro: {str(e)}")
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx, quantidade: int = 100):
        """Limpa messages de um canal"""
        if quantidade <= 0:
            await ctx.send("❌ Quantidade deve ser maior que 0")
            return
        
        if quantidade > 1000:
            await ctx.send("❌ Máximo de 1000 mensagens por vez")
            return
        
        try:
            # Cria lista de IDs de mensagens para deletar
            mensagens = []
            async for message in ctx.channel.history(limit=quantidade + 1):
                if message.id != ctx.message.id:  # Não deleta o comando
                    mensagens.append(message)
            
            # Deleta em bulk (máximo 100 por vez)
            for i in range(0, len(mensagens), 100):
                lote = mensagens[i:i+100]
                try:
                    await ctx.channel.delete_messages(lote)
                except:
                    # Se bulk delete falhar, deleta um por um
                    for msg in lote:
                        try:
                            await msg.delete()
                        except:
                            pass
            
            embed = discord.Embed(
                title="✅ Canal limpo",
                description=f"**{len(mensagens)}** mensagens foram deletadas",
                color=discord.Color.green()
            )
            
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
        
        except Exception as e:
            await ctx.send(f"❌ Erro: {str(e)}")


async def setup(bot):
    await bot.add_cog(Cleanup(bot))
