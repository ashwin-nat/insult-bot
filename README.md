
## ⚙️ Discord Insult Bot Setup Guide

Follow these steps to create your bot on Discord and invite it to your server:

### 1. Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"**
3. Name your bot (e.g., *Insult Bot*) and click **Create**

---

### 2. Generate a Bot Token

1. In your application, go to the **"Bot"** tab (left sidebar)
2. Click **"Add Bot"** → Yes
3. Under **"Token"**, click **"Reset Token"** → Copy it
4. Paste it into your `.env` file:

```

DISCORD_TOKEN="your-token-here"

````

> ⚠️ Never share this token. It gives full control of your bot.

---

### 3. Get Client ID

- Go to the **"OAuth2" → "General"** tab
- Copy the **Client ID** — you’ll need this to invite the bot

---

### 4. Set Bot Permissions

1. Go to the **"OAuth2" → "URL Generator"**
2. Under **Scopes**, check:
   - `bot`

3. Under **Bot Permissions**, select:
   - `Send Messages`
   - `Read Message History`
   - `Use Slash Commands` *(optional, if you use them)*

4. Copy the generated URL and open it in your browser
5. Select your Discord server and authorize the bot

---

### 5. Start the Bot

Once invited to your server, run:

```bash
python main.py
````

Your bot should appear online and respond to messages!
