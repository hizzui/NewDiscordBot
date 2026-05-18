# NDB Bot - Discord Automation Platform

<img width="736" height="414" alt="NDB Bot Banner" src="https://github.com/user-attachments/assets/6ce3a2a0-39e4-4222-95b0-37da2225ebec" />

A feature-rich, modular Discord bot with over 40 advanced commands built to handle server moderation, virtual economy, interactive games, trivia datasets, and dynamic livestream tracking.

## 🚀 Core Modules & Features

- **Moderation:** Complete toolkit for server safety (`kick`, `ban`, `unban`, `mute`, `unmute`, `warn`, `warnings`, `unwarn`).
- **Economy:** Fully functional virtual currency engine (`balance`, `pay`, `slots`, `payday`, `leaderboard`).
- **Fun & Games:** Quick interaction utilities (`dado` (dice), `moeda` (coin flip), `vote`, `calc`).
- **Trivia Engine:** Interactive game module with a pool of 50+ built-in questions (`trivia`, `trivia_score`, `trivia_top`).
- **Custom Commands:** Allows server admins to handle dynamic message hooks (`customcom create`, `customcom delete`, `customcom list`, `customcom show`).
- **Livestream Tracking:** Real-time stream monitoring utilizing async hooks for the Twitch API (`stream add`, `stream remove`, `stream list`, `stream check`).
- **Channel Cleanup:** High-speed bulk message deletion utilities (`purge`, `clean`, `cleanup`, `clear`).
- **Information:** Rich embedded server and profile data diagnostics (`user`, `servidor`, `avatar`, `ajuda`).

---

## 💻 Quick Start

### Prerequisites
- Python 3.10+
- A Discord Bot Token (via Discord Developer Portal)

### Installation
```bash
# Clone the repository and navigate to the root directory
git clone [https://github.com/rycarvalho/ndb-bot.git](https://github.com/rycarvalho/ndb-bot.git)
cd ndb-bot

# Install the required dependencies
pip install -r requirements.txt

# Set up your environment file
cp .env.example .env
