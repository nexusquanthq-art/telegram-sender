# Telegram Sender

GUI tool for sending messages, photos, videos, and documents to Telegram.

## Features

- Send text messages to Telegram
- Send photos (JPG, PNG, GIF, WebP)
- Send videos (MP4, MOV, AVI, MKV)
- Send documents (PDF, ZIP, TXT, etc.)
- Clean GUI with two windows
- Threaded sending (no UI freeze)
- Auto file type detection

## Setup

### 1. Create a Telegram Bot

1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow the instructions
5. Copy the bot token it gives you

### 2. Get Your Chat ID

1. Search for `@userinfobot` on Telegram
2. Start a chat with it
3. It will show your chat ID
4. Copy the ID

### 3. Add Your Credentials

You have two options:

**Option A: Environment Variables**

# Windows
set TG_BOT_TOKEN=your_token_here
set TG_CHAT_ID=your_chat_id_here

# Linux/Mac
export TG_BOT_TOKEN=your_token_here
export TG_CHAT_ID=your_chat_id_here

Option B: Edit the Code Directly

Open telegram.py and change these lines:


BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "YOUR_BOT_TOKEN")
CHAT_ID   = os.getenv("TG_CHAT_ID",   "YOUR_CHAT_ID")

Replace YOUR_BOT_TOKEN and YOUR_CHAT_ID with your real values.
Installation


pip install requests

How To Run


python telegram.py

Two windows open:

    Message Window - Send text messages

    Media Window - Send files with optional captions

How To Use
Sending Text

    Type your message

    Click "Send"

    Check status at the bottom

Sending Files

    Click "Browse..." and select a file

    (Optional) Add a caption

    Click "Send"

Supported File Types

    Images: JPG, JPEG, PNG, GIF, WebP

    Videos: MP4, MOV, AVI, MKV

    Documents: PDF, ZIP, TXT, and more

Requirements

    Python

    requests library

License

All Rights Reserved - See LICENSE file
Author

Nexus

    Telegram: @Nexushqh
