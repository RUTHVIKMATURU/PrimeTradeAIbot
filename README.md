Simplified Binance Futures Testnet Trading Bot
Junior Python Developer – Crypto Trading Bot Assignment






🧩 Overview

This project implements a simplified crypto trading bot for the Binance USDT-M Futures Testnet.
The bot supports Market, Limit, Stop-Limit, and TWAP strategies, handles minimum-notional rules automatically, and logs all API communication.

✨ Features
🟢 Core Requirements

Connects to Binance Futures Testnet

Uses python-binance library

Supports Market, Limit, Stop-Limit, and TWAP orders

CLI interface using argparse

Logs all actions to basicbot.log

Error handling and validation

🔵 Bonus Features

Auto-adjusts quantity to meet minimum notional (100 USDT)

TWAP execution strategy

Clean OOP structure (BasicBot)

🗂 Project Structure
project/
│── basic_bot.py
│── .env                 # NOT committed
│── .env.example
│── basicbot.log         # auto-generated
│── README.md
│── venv/                # optional

⚙️ Setup Instructions
1️⃣ Create Virtual Environment
Linux/macOS
python3 -m venv venv
source venv/bin/activate

Windows
python -m venv venv
venv\Scripts\activate

2️⃣ Install Dependencies
pip install python-binance python-dotenv

3️⃣ Create .env File (in project root)
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret


⚠️ Do NOT add quotes
⚠️ Do NOT commit .env to GitHub

4️⃣ Create Testnet API Keys

Go to:
https://testnet.binancefuture.com/en/futures
 → Profile → API Management

Enable:

✔ Futures

✔ Trade

▶️ Usage (CLI Examples)
📌 Market Order
python basic_bot.py market --symbol BTCUSDT --side BUY --qty 0.002

📌 Limit Order
python basic_bot.py limit --symbol ETHUSDT --side BUY --qty 0.04 --price 3000

📌 Stop-Limit Order
python basic_bot.py stoplimit --symbol BTCUSDT --side SELL --qty 0.002 --stop 65000 --price 64900

📌 TWAP (Split execution)
python basic_bot.py twap --symbol BTCUSDT --side BUY --total_qty 0.01 --slices 5 --interval 10

📜 Logging

All actions are logged to:

basicbot.log


The log includes:

timestamps

API requests

API responses

exceptions

Attach this file in your submission.

🔒 Security & Best Practices

Always use Testnet API keys

Never commit .env to GitHub

Bot auto-adjusts quantity to avoid:

“Notional must be ≥ 100 USDT” errors
