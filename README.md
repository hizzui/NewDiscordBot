# 🤖 NDB Bot - Discord Bot Modular

Um bot Discord modular com **40+ comandos** para moderação, economia, diversão, trivia e monitoramento de streams (Twitch).

## ✨ Funcionalidades

**Moderação:** `!kick` `!ban` `!unban` `!mute` `!unmute` `!warn` `!warnings` `!unwarn`

**Economia:** `!balance` `!pay` `!slots` `!payday` `!leaderboard`

**Diversão:** `!dado` `!moeda` `!vote` `!calc`

**Trivia:** `!trivia` `!trivia_score` `!trivia_top` (50+ perguntas)

**Customizados:** `!customcom create` `!customcom delete` `!customcom list` `!customcom show`

**Streams:** `!stream add/remove/list/check` (Twitch API)

**Limpeza:** `!purge` `!clean` `!cleanup` `!clear`

**Informações:** `!user` `!servidor` `!avatar` `!ajuda`

---

## 🚀 Quick Start

### Pré-requisitos
- Python 3.10+
- Token do Discord Bot

### Instalação
```bash
pip install -r requirements.txt
cp .env.example .env
```

### Configuração
Edite `.env` e adicione:
```
DISCORD_TOKEN=seu_token_aqui
TWITCH_CLIENT_ID=opcional
TWITCH_ACCESS_TOKEN=opcional
```

### Rodar
```bash
python main.py
```

---

## 📁 Estrutura

```
cogs/
 ├── general.py      → Gerais + ajuda
 ├── moderation.py   → Moderação
 ├── economy.py      → Economia
 ├── fun.py          → Diversão
 ├── trivia.py       → Trivia
 ├── streams.py      → Twitch
 ├── customcom.py    → Customizados
 ├── cleanup.py      → Limpeza
 └── info.py         → Informações

config.py           → Configurações
logging_config.py   → Logging
main.py             → Entry point
```

---

## 🔧 Configuração

### Variáveis de Ambiente
```
DISCORD_TOKEN=           (obrigatório)
TWITCH_CLIENT_ID=        (opcional)
TWITCH_ACCESS_TOKEN=     (opcional)
LOG_LEVEL=INFO
COMMAND_PREFIX=!
```

### Dependências
- discord.py 2.3.2
- aiohttp 3.9.1
- python-dotenv
- yt-dlp
- PyNaCl

---

## 📝 Licença

MIT License

