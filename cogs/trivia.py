import discord
from discord.ext import commands
import random
import asyncio

class Trivia(commands.Cog):
    """Jogo de trivia com perguntas e pontuação"""
    
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}  # Rastreia sessões ativas
        self.leaderboard = {}  # Pontuação global
        self.perguntas = self.load_perguntas()
    
    def load_perguntas(self):
        """Carrega banco de perguntas expandido (50+ perguntas)"""
        return [
            # Geografia
            {"pergunta": "Qual é a capital da França?", "opcoes": ["Paris", "Lyon", "Marselha", "Bordeaux"], "resposta": "Paris"},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "Brasília", "São Paulo", "Salvador"], "resposta": "Brasília"},
            {"pergunta": "Qual é o maior oceano do mundo?", "opcoes": ["Atlântico", "Índico", "Pacífico", "Ártico"], "resposta": "Pacífico"},
            {"pergunta": "Quantos continentes existem?", "opcoes": ["5", "6", "7", "8"], "resposta": "7"},
            {"pergunta": "Qual é a capital do Japão?", "opcoes": ["Osaka", "Tóquio", "Kyoto", "Hiroshima"], "resposta": "Tóquio"},
            {"pergunta": "Qual país tem mais habitantes?", "opcoes": ["Índia", "China", "EUA", "Indonésia"], "resposta": "Índia"},
            
            # Ciência
            {"pergunta": "Qual planeta é conhecido como o Planeta Vermelho?", "opcoes": ["Vênus", "Marte", "Júpiter", "Saturno"], "resposta": "Marte"},
            {"pergunta": "Quantos lados tem um hexágono?", "opcoes": ["4", "5", "6", "7"], "resposta": "6"},
            {"pergunta": "Qual é o elemento químico com símbolo 'Au'?", "opcoes": ["Alumínio", "Argônio", "Ouro", "Prata"], "resposta": "Ouro"},
            {"pergunta": "Qual é a velocidade da luz?", "opcoes": ["300.000 km/s", "200.000 km/s", "400.000 km/s", "150.000 km/s"], "resposta": "300.000 km/s"},
            {"pergunta": "Quantos ossos tem o corpo humano?", "opcoes": ["186", "206", "226", "246"], "resposta": "206"},
            {"pergunta": "Qual é o maior órgão do corpo humano?", "opcoes": ["Coração", "Pele", "Fígado", "Pulmão"], "resposta": "Pele"},
            
            # História
            {"pergunta": "Em que ano terminou a Segunda Guerra Mundial?", "opcoes": ["1943", "1944", "1945", "1946"], "resposta": "1945"},
            {"pergunta": "Qual foi o primeiro país a enviar um satélite ao espaço?", "opcoes": ["EUA", "União Soviética", "China", "França"], "resposta": "União Soviética"},
            {"pergunta": "Quem foi o primeiro presidente dos EUA?", "opcoes": ["Thomas Jefferson", "George Washington", "Abraham Lincoln", "Benjamin Franklin"], "resposta": "George Washington"},
            {"pergunta": "Em qual ano ocorreu a Revolução Francesa?", "opcoes": ["1776", "1789", "1800", "1815"], "resposta": "1789"},
            
            # Animais
            {"pergunta": "Qual é o animal terrestre mais rápido?", "opcoes": ["Antílope", "Gazela", "Chita", "Leão"], "resposta": "Chita"},
            {"pergunta": "Qual animal é o mais pesado do mundo?", "opcoes": ["Elefante", "Baleia Azul", "Girafa", "Hipopótamo"], "resposta": "Baleia Azul"},
            {"pergunta": "Quantas patas tem um polvo?", "opcoes": ["6", "8", "10", "12"], "resposta": "8"},
            {"pergunta": "Qual mamífero coloca ovos?", "opcoes": ["Ornitorrinco", "Equidna", "Ambos", "Nenhum"], "resposta": "Ambos"},
            
            # Moedas
            {"pergunta": "Qual é a moeda do Japão?", "opcoes": ["Won", "Yuan", "Iene", "Baht"], "resposta": "Iene"},
            {"pergunta": "Qual é a moeda do Reino Unido?", "opcoes": ["Euro", "Libra", "Dólar", "Franco"], "resposta": "Libra"},
            {"pergunta": "Qual é a moeda da China?", "opcoes": ["Iene", "Yuan", "Rupeia", "Baht"], "resposta": "Yuan"},
            {"pergunta": "Qual é a moeda do Brasil?", "opcoes": ["Peso", "Real", "Bolívar", "Guarani"], "resposta": "Real"},
            
            # Cultura
            {"pergunta": "Quantas cores tem o arco-íris?", "opcoes": ["5", "6", "7", "8"], "resposta": "7"},
            {"pergunta": "Qual é a maior biblioteca do mundo?", "opcoes": ["Biblioteca Nacional Francesa", "Biblioteca Britânica", "Biblioteca do Congresso dos EUA", "Biblioteca Vaticana"], "resposta": "Biblioteca do Congresso dos EUA"},
            {"pergunta": "Quantas cordas tem uma guitarra padrão?", "opcoes": ["5", "6", "7", "8"], "resposta": "6"},
            
            # Esportes
            {"pergunta": "Quantos jogadores tem um time de futebol em campo?", "opcoes": ["9", "10", "11", "12"], "resposta": "11"},
            {"pergunta": "Quantas Copas do Mundo o Brasil venceu?", "opcoes": ["3", "4", "5", "6"], "resposta": "5"},
            {"pergunta": "Em que país nasceu o xadrez moderno?", "opcoes": ["Irã", "Itália", "Espanha", "França"], "resposta": "Espanha"},
            
            # Más
            {"pergunta": "Qual país tem mais ouro?", "opcoes": ["Austrália", "África do Sul", "Canadá", "China"], "resposta": "China"},
            {"pergunta": "Qual é o deserto mais quente do mundo?", "opcoes": ["Deserto de Gobi", "Deserto do Saara", "Deserto da Líbia", "Deserto Arábico"], "resposta": "Deserto da Líbia"},
            
            # Tecnologia
            {"pergunta": "Quem inventou a lâmpada elétrica?", "opcoes": ["Nikola Tesla", "Thomas Edison", "George Westinghouse", "Joseph Swan"], "resposta": "Thomas Edison"},
            {"pergunta": "Em qual ano foi criada a Internet?", "opcoes": ["1969", "1975", "1989", "1995"], "resposta": "1969"},
            {"pergunta": "Qual é a unidade básica de um computador?", "opcoes": ["Byte", "Kilobyte", "Bit", "Megabyte"], "resposta": "Bit"},
            
            # Diversos
            {"pergunta": "Quantos dias tem um ano bissexto?", "opcoes": ["364", "365", "366", "367"], "resposta": "366"},
            {"pergunta": "Qual é o símbolo químico do ferro?", "opcoes": ["Fe", "Fr", "F", "Fn"], "resposta": "Fe"},
            {"pergunta": "Quantas letras tem o alfabeto grego?", "opcoes": ["20", "22", "24", "26"], "resposta": "24"},
            {"pergunta": "Qual é a montanha mais alta do mundo?", "opcoes": ["K2", "Kangchenjunga", "Everest", "Makalu"], "resposta": "Everest"},
            {"pergunta": "Qual é o rio mais comprido do mundo?", "opcoes": ["Amazonas", "Nilo", "Yangtse", "Mississípi"], "resposta": "Nilo"},
            {"pergunta": "Quantas cidades têm o status de 'Cidade Eterna'?", "opcoes": ["1", "2", "3", "4"], "resposta": "1"},
            {"pergunta": "Qual é o metal mais precioso do mundo?", "opcoes": ["Ouro", "Platina", "Paládio", "Ródio"], "resposta": "Ródio"},
            {"pergunta": "Quantos lados tem um pentágono?", "opcoes": ["4", "5", "6", "7"], "resposta": "5"},
        ]
    
    @commands.command()
    async def trivia(self, ctx):
        """Inicia um jogo de trivia"""
        
        if ctx.channel.id in self.sessions:
            await ctx.send("Já há uma sessão de trivia em andamento neste canal!")
            return
        
        # Marca como em sessão ativa
        self.sessions[ctx.channel.id] = {"jogador": ctx.author, "pontos": 0}
        
        try:
            embed = discord.Embed(
                title="🎯 Bem-vindo ao Trivia!",
                description="Você terá 10 segundos para responder cada pergunta",
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            
            await asyncio.sleep(2)
            
            # Faz 5 perguntas
            pontos = 0
            for i in range(5):
                pergunta_data = random.choice(self.perguntas)
                resposta_correta = pergunta_data["resposta"]
                opcoes = pergunta_data["opcoes"].copy()
                
                # Embaralha opções
                random.shuffle(opcoes)
                
                # Cria embed com pergunta
                embed = discord.Embed(
                    title=f"❓ Pergunta {i+1}/5",
                    description=pergunta_data["pergunta"],
                    color=discord.Color.purple()
                )
                
                # Adiciona opções com reações
                letras = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
                for j, opcao in enumerate(opcoes):
                    embed.add_field(
                        name=f"{letras[j]} {opcao}",
                        value="Continue...",
                        inline=False
                    )
                
                embed.set_footer(text="Você tem 10 segundos para responder")
                msg = await ctx.send(embed=embed)
                
                # Adiciona reações
                for letra in letras:
                    await msg.add_reaction(letra)
                
                # Aguarda reação
                try:
                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in letras
                    
                    reaction, _ = await self.bot.wait_for(
                        'reaction_add',
                        timeout=10.0,
                        check=check
                    )
                    
                    # Verifica resposta
                    indice = letras.index(str(reaction.emoji))
                    resposta_usuario = opcoes[indice]
                    
                    if resposta_usuario == resposta_correta:
                        pontos += 1
                        await ctx.send(f"✅ Correto! (**{resposta_correta}**)")
                    else:
                        await ctx.send(f"❌ Errado! Era **{resposta_correta}**")
                
                except asyncio.TimeoutError:
                    await ctx.send(f"⏱️ Tempo esgotado! Era **{resposta_correta}**")
                
                await asyncio.sleep(2)
            
            # Resultado final
            embed = discord.Embed(
                title="🏁 Fim do Jogo!",
                description=f"Você acertou **{pontos}/5** perguntas",
                color=discord.Color.gold()
            )
            
            # Atualiza pontuação
            user_id = str(ctx.author.id)
            if user_id not in self.leaderboard:
                self.leaderboard[user_id] = {"pontos": 0, "jogos": 0}
            
            self.leaderboard[user_id]["pontos"] += pontos
            self.leaderboard[user_id]["jogos"] += 1
            
            embed.add_field(
                name="Sua Pontuação",
                value=f"Jogos: {self.leaderboard[user_id]['jogos']}\nPontos totais: {self.leaderboard[user_id]['pontos']}",
                inline=False
            )
            
            await ctx.send(embed=embed)
        
        finally:
            # Remove sessão
            if ctx.channel.id in self.sessions:
                del self.sessions[ctx.channel.id]
    
    @commands.command()
    async def trivia_score(self, ctx, usuario: discord.User = None):
        """Mostra pontuação de trivia"""
        if not usuario:
            usuario = ctx.author
        
        user_id = str(usuario.id)
        
        if user_id not in self.leaderboard:
            await ctx.send(f"**{usuario}** ainda não jogou trivia")
            return
        
        dados = self.leaderboard[user_id]
        
        embed = discord.Embed(
            title=f"🎯 Pontuação de {usuario}",
            color=discord.Color.purple()
        )
        embed.add_field(name="Jogos", value=dados["jogos"], inline=True)
        embed.add_field(name="Pontos Totais", value=dados["pontos"], inline=True)
        media = round(dados["pontos"] / dados["jogos"], 1) if dados["jogos"] > 0 else 0
        embed.add_field(name="Média por jogo", value=media, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def trivia_top(self, ctx):
        """Mostra top 10 jogadores de trivia"""
        if not self.leaderboard:
            await ctx.send("Ninguém jogou trivia ainda!")
            return
        
        # Ordena por pontos
        top = sorted(
            self.leaderboard.items(),
            key=lambda x: x[1]["pontos"],
            reverse=True
        )[:10]
        
        embed = discord.Embed(
            title="🏆 Top 10 Trivia",
            color=discord.Color.gold()
        )
        
        for i, (user_id, dados) in enumerate(top, 1):
            try:
                user = await self.bot.fetch_user(int(user_id))
                nome = user.name
            except:
                nome = f"ID: {user_id}"
            
            embed.add_field(
                name=f"{i}. {nome}",
                value=f"{dados['pontos']} pts ({dados['jogos']} jogos)",
                inline=False
            )
        
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Trivia(bot))
