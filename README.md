# NDB Bot - Discord Bot

<img width="736" height="414" alt="image" src="https://github.com/user-attachments/assets/6ce3a2a0-39e4-4222-95b0-37da2225ebec" />


Um bot Discord modular com 40+ comandos para moderação, economia, diversão, trivia e monitoramento de streams.

## Funcionalidades

**Moderacao:** kick, ban, unban, mute, unmute, warn, warnings, unwarn

**Economia:** balance, pay, slots, payday, leaderboard

**Diversao:** dado, moeda, vote, calc

**Trivia:** trivia, trivia_score, trivia_top (50+ perguntas)

**Customizados:** customcom create, customcom delete, customcom list, customcom show

**Streams:** stream add, stream remove, stream list, stream check (Twitch API)

**Limpeza:** purge, clean, cleanup, clear

**Informacoes:** user, servidor, avatar, ajuda

## Quick Start

### Requisitos
- Python 3.10+
- Discord Token

### Instalacao
```bash
pip install -r requirements.txt
cp .env.example .env
```

### Configuracao
Edite .env:
```
DISCORD_TOKEN=seu_token
```

### Rodar
```bash
python main.py
```

## Dependencias

- discord.py 2.3.2
- aiohttp 3.9.1
- python-dotenv
- yt-dlp
- PyNaCl


