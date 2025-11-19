Simplified Binance Futures Testnet Trading Bot
Junior Python Developer – Crypto Trading Bot Assignment






🧩 Overview

This project implements a simplified crypto trading bot for the Binance USDT-M Futures Testnet, fulfilling all requirements of the hiring assignment.

The bot supports placing Market, Limit, Stop-Limit, and TWAP orders while handling Binance futures constraints like minimum notional value and symbol precision.

✨ Features
🟢 Core Requirements
Requirement	Status	Notes
Binance Testnet Support	✅	Uses testnet.binancefuture.com/fapi
API Key + Secret	✅	Loaded from .env
python-binance Library	✅	Main client wrapper
Market Orders	✅	Auto-adjusts qty
Limit Orders	✅	Auto-adjusts qty
Input via CLI	✅	argparse
Logging to file	✅	basicbot.log
Error Handling	✅	Exception-safe
🔵 Bonus Features

⭐ Stop-Limit Orders

⭐ TWAP Strategy (Time Weighted Average Price)

⭐ Auto-adjust quantity to satisfy min-notional (100 USDT)

⭐ Reusable class-based code structure (BasicBot)

⭐ Clean & professional CLI interface

🛠️ Project Structure
project/
│── basic_bot.py
│── .env                # (not shared)
│── .env.example
│── README.md
│── basicbot.log        # generated automatically
│── venv/               # optional

⚙️ Setup Instructions
🔧 1. Clone or Download the project
git clone <your-repo-url>
cd project

🐍 2. Create & activate virtual environment

Linux/macOS:

python3 -m venv venv
source venv/bin/activate


Windows:

venv\Scripts\activate

📦 3. Install dependencies
pip install python-binance python-dotenv

🔐 4. Create .env file

Use the template:

BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret


⚠️ Do NOT add quotes
⚠️ Do NOT upload .env to GitHub

📡 How to Use the Bot (CLI Commands)
▶️ Market Order
python basic_bot.py market --symbol BTCUSDT --side BUY --qty 0.002

▶️ Limit Order
python basic_bot.py limit --symbol ETHUSDT --side BUY --qty 0.04 --price 3000

▶️ Stop-Limit Order
python basic_bot.py stoplimit --symbol BTCUSDT --side SELL --qty 0.002 --stop 65000 --price 64900

▶️ TWAP Strategy Order
python basic_bot.py twap --symbol BTCUSDT --side BUY --total_qty 0.01 --slices 5 --interval 10

📜 Logging

All API actions are logged to:

basicbot.log


The log includes:

Timestamps

Request types

Full API responses

Error stack traces

📌 You MUST attach this log in your job application email.

🔒 Security Notice

Never upload .env to GitHub

This bot only operates on Testnet

Auto-adjust qty protects from

“Notional must be ≥ 100 USDT”

Invalid step sizes