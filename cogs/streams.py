import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime
import aiohttp

class Streams(commands.Cog):
    """Monitora e notifica sobre streamers do Twitch e YouTube via API real"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config_file = "streams_config.json"
        self.config = self.load_config()
        self.notified_streamers = set()
        self.twitch_token = os.getenv("TWITCH_TOKEN")
        self.twitch_client_id = os.getenv("TWITCH_CLIENT_ID")
        self.check_streams.start()
    
    def load_config(self):
        """Carrega configuração de arquivo"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"notify_channel": None, "streamers": []}
    
    def save_config(self):
        """Salva configuração em arquivo"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)
    
    async def check_twitch_status(self, usuario):
        """Verifica status REAL de uma live na Twitch via API"""
        if not self.twitch_token or not self.twitch_client_id:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://api.twitch.tv/helix/users?login={usuario}"
                headers = {
                    "Client-ID": self.twitch_client_id,
                    "Authorization": f"Bearer {self.twitch_token}"
                }
                
                async with session.get(url, headers=headers) as resp:
                    if resp.status != 200:
                        return None
                    data = await resp.json()
                    if not data.get("data"):
                        return None
                    
                    user_id = data["data"][0]["id"]
                    
                    stream_url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
                    async with session.get(stream_url, headers=headers) as stream_resp:
                        if stream_resp.status != 200:
                            return None
                        stream_data = await stream_resp.json()
                        if stream_data.get("data"):
                            stream = stream_data["data"][0]
                            return {
                                "online": True,
                                "title": stream.get("title"),
                                "game": stream.get("game_name"),
                                "viewers": stream.get("viewer_count"),
                                "url": f"https://twitch.tv/{usuario}"
                            }
                        return {"online": False}
        except Exception as e:
            print(f"Erro ao checar Twitch: {e}")
            return None
    
    @commands.group()
    @commands.has_permissions(manage_guild=True)
    async def streamset(self, ctx):
        """Configurações de streams"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="⚙️ Configuração de Streams",
                description="Direcionar notificações de streams",
                color=discord.Color.purple()
            )
            embed.add_field(
                name="Subcomandos",
                value="`!streamset channel [#canal]` - Define canal\n"
                      "`!streamset show` - Mostra config\n"
                      "`!streamset credentials` - Como obter credenciais Twitch",
                inline=False
            )
            await ctx.send(embed=embed)
    
    @streamset.command(name="channel")
    async def set_channel(self, ctx, canal: discord.TextChannel):
        """Define canal de notificações"""
        self.config["notify_channel"] = canal.id
        self.save_config()
        embed = discord.Embed(
            title="✅ Canal configurado",
            description=f"Notificações em {canal.mention}",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @streamset.command(name="show")
    async def show_config(self, ctx):
        """Mostra configuração"""
        notify_channel = self.config.get("notify_channel")
        canal_text = f"<#{notify_channel}>" if notify_channel else "Não configurado"
        
        embed = discord.Embed(
            title="📡 Configuração de Streams",
            color=discord.Color.purple()
        )
        embed.add_field(name="Canal", value=canal_text, inline=False)
        embed.add_field(name="Streamers", value=f"{len(self.config.get('streamers', []))}", inline=False)
        embed.add_field(name="Status API", value="Pronto para Twitch ✅" if self.twitch_token else "Configure token ⚠️", inline=False)
        await ctx.send(embed=embed)
    
    @streamset.command(name="credentials")
    async def show_credentials(self, ctx):
        """Instruções para obter credenciais Twitch"""
        embed = discord.Embed(
            title="🔑 Como obter credenciais Twitch",
            description="Siga estes passos para habilitar monitoramento automático:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="1. Crie uma aplicação",
            value="Acesse: https://dev.twitch.tv/console/apps\nClique em 'Create Application'",
            inline=False
        )
        embed.add_field(
            name="2. Copie as credenciais",
            value="Copie: Client ID e Client Secret",
            inline=False
        )
        embed.add_field(
            name="3. Gere um token OAuth",
            value="No painel do Twitch, gere um token de aplicação",
            inline=False
        )
        embed.add_field(
            name="4. Configure no bot",
            value="Adicione ao `.env`:\n`TWITCH_CLIENT_ID=seu_id`\n`TWITCH_TOKEN=seu_token`",
            inline=False
        )
        embed.add_field(
            name="5. Reinicie o bot",
            value="Os comandos de stream farão verificações em tempo real!",
            inline=False
        )
        await ctx.send(embed=embed)
    
    @commands.group()
    async def stream(self, ctx):
        """Gerencia monitoramento de streamers"""
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="📡 Gerenciar Streams",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Subcomandos",
                value="`!stream add twitch [usuario]` - Adicionar\n"
                      "`!stream remove [usuario]` - Remover\n"
                      "`!stream list` - Listar\n"
                      "`!stream check [usuario]` - Checar AGORA (requer API)",
                inline=False
            )
            await ctx.send(embed=embed)
    
    @stream.command(name="add")
    @commands.has_permissions(manage_guild=True)
    async def add_stream(self, ctx, tipo: str, usuario: str):
        """Adiciona streamer ao monitoramento"""
        if tipo.lower() not in ["twitch", "youtube"]:
            await ctx.send("❌ Use: `twitch` ou `youtube`")
            return
        
        for s in self.config.get("streamers", []):
            if s["nome"].lower() == usuario.lower() and s["guild_id"] == ctx.guild.id:
                await ctx.send(f"⚠️ Já monitorando **{usuario}**")
                return
        
        if "streamers" not in self.config:
            self.config["streamers"] = []
        
        self.config["streamers"].append({
            "tipo": tipo.lower(),
            "nome": usuario,
            "guild_id": ctx.guild.id,
            "adicionado_por": str(ctx.author),
            "data": datetime.now().isoformat()
        })
        self.save_config()
        
        embed = discord.Embed(
            title="✅ Streamer adicionado",
            description=f"Monitorando **{usuario}**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    
    @stream.command(name="remove")
    @commands.has_permissions(manage_guild=True)
    async def remove_stream(self, ctx, usuario: str):
        """Remove streamer"""
        original_count = len(self.config.get("streamers", []))
        self.config["streamers"] = [
            s for s in self.config.get("streamers", [])
            if not (s["nome"].lower() == usuario.lower() and s["guild_id"] == ctx.guild.id)
        ]
        self.save_config()
        
        if len(self.config["streamers"]) < original_count:
            await ctx.send(f"✅ Deixamos de monitorar **{usuario}**")
        else:
            await ctx.send(f"❌ **{usuario}** não encontrado")
    
    @stream.command(name="list")
    async def list_streams(self, ctx):
        """Lista streamers do servidor"""
        streamers = [
            s for s in self.config.get("streamers", [])
            if s["guild_id"] == ctx.guild.id
        ]
        
        if not streamers:
            await ctx.send("Nenhum streamer monitorado")
            return
        
        embed = discord.Embed(
            title="📡 Streamers do Servidor",
            description=f"Total: {len(streamers)}",
            color=discord.Color.purple()
        )
        
        for s in streamers:
            emoji = "🟣" if s["tipo"] == "twitch" else "🔴"
            embed.add_field(
                name=f"{emoji} {s['nome']}",
                value=f"Adicionado por: {s['adicionado_por']}",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @stream.command(name="check")
    async def check_streamer(self, ctx, usuario: str):
        """Verifica status atual via API Twitch"""
        if not self.twitch_token:
            await ctx.send("❌ Configure credenciais com `!streamset credentials`")
            return
        
        async with ctx.typing():
            status = await self.check_twitch_status(usuario)
            
            if status is None:
                await ctx.send(f"❌ Erro ao buscar **{usuario}**")
                return
            
            if status["online"]:
                embed = discord.Embed(
                    title="🔴 AO VIVO!",
                    description=f"**{usuario}** está transmitindo",
                    color=discord.Color.red()
                )
                embed.add_field(name="Título", value=status["title"][:100], inline=False)
                embed.add_field(name="Jogo", value=status["game"] or "Sem categoria", inline=True)
                embed.add_field(name="Viewers", value=f"{status['viewers']:,}", inline=True)
                embed.add_field(name="Link", value=f"[Assistir]({status['url']})", inline=False)
            else:
                embed = discord.Embed(
                    title="⚫ Offline",
                    description=f"**{usuario}** não está transmitindo",
                    color=discord.Color.gray()
                )
            
            await ctx.send(embed=embed)
    
    @tasks.loop(minutes=15)
    async def check_streams(self):
        """Verifica streamers a cada 15 minutos - REQUER API Twitch configurada"""
        if not self.config.get("notify_channel") or not self.twitch_token:
            return
        
        notify_channel = self.bot.get_channel(self.config["notify_channel"])
        if not notify_channel:
            return
        
        for streamer in self.config.get("streamers", []):
            if streamer["tipo"] != "twitch":
                continue
            
            streamer_key = f"{streamer['nome']}_{notify_channel.guild.id}"
            status = await self.check_twitch_status(streamer["nome"])
            
            if status and status.get("online") and streamer_key not in self.notified_streamers:
                embed = discord.Embed(
                    title="🔴 LIVE NA TWITCH!",
                    description=f"**{streamer['nome']}** está transmitindo!",
                    color=discord.Color.red()
                )
                embed.add_field(name="📺 Título", value=status.get("title", "N/A")[:100], inline=False)
                embed.add_field(name="🎮 Jogo", value=status.get("game", "Sem categoria"), inline=True)
                embed.add_field(name="👥 Viewers", value=f"{status.get('viewers', 0):,}", inline=True)
                embed.add_field(name="🔗", value=f"[Assistir agora]({status['url']})", inline=False)
                
                await notify_channel.send(embed=embed)
                self.notified_streamers.add(streamer_key)
            
            elif not status or not status.get("online"):
                self.notified_streamers.discard(streamer_key)
    
    @check_streams.before_loop
    async def before_check_streams(self):
        await self.bot.wait_until_ready()
    
    def cog_unload(self):
        self.check_streams.cancel()


async def setup(bot):
    await bot.add_cog(Streams(bot))
