import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def user(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"Informações de {member.name}", color=discord.Color.green())
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Nome de Usuário", value=f"@{member.name}", inline=False)
        embed.add_field(name="Display Name", value=member.display_name, inline=True)
        embed.add_field(name="Bot", value="Sim" if member.bot else "Não", inline=True)
        embed.add_field(name="Conta Criada em", value=member.created_at.strftime("%d/%m/%Y às %H:%M"), inline=False)
        embed.add_field(name="Entrou no Servidor em", value=member.joined_at.strftime("%d/%m/%Y às %H:%M"), inline=False)
        embed.add_field(name="Status", value=str(member.status).title(), inline=True)
        embed.add_field(name="Atividade", value=member.activity.name if member.activity else "Nenhuma", inline=True)
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        embed.add_field(name="Cargos", value=", ".join(roles) if roles else "Nenhum cargo", inline=False)
        embed.add_field(name="Cor do Perfil", value=str(member.color), inline=True)
        embed.add_field(name="Permissão de Admin", value="Sim" if member.guild_permissions.administrator else "Não", inline=True)
        embed.set_footer(text=f"Solicitado por {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def servidor(self, ctx: commands.Context):
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
    
    @commands.command()
    async def avatar(self, ctx: commands.Context, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"Avatar de {member.name}", color=discord.Color.blue())
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
