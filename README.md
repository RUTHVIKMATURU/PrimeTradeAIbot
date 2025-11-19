<!-- README.md for Simplified Binance Futures Testnet Trading Bot -->

# 🚀 Simplified Binance Futures Testnet Trading Bot  
### *Junior Python Developer – Crypto Trading Bot Assignment*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Binance API](https://img.shields.io/badge/Binance-Futures%20API-gold?logo=binance)
![Status](https://img.shields.io/badge/Project-Completed-brightgreen)

---

## 🧩 Overview

This project implements a simplified **crypto trading bot** for the **Binance USDT-M Futures Testnet**.  
It supports Market, Limit, Stop-Limit, and TWAP orders, handles Binance futures constraints (minimum notional & step sizes), and logs all activity.

---

## ✨ Features

### 🟢 Core Requirements
- ✅ Connects to **Binance Futures Testnet** (`testnet.binancefuture.com/fapi`)  
- ✅ Uses `python-binance` library  
- ✅ Supports **Market**, **Limit**, **Stop-Limit**, and **TWAP** orders  
- ✅ CLI input via `argparse`  
- ✅ Logging to `basicbot.log`  
- ✅ Error handling and validation

### 🔵 Bonus
- ⭐ Auto-adjusts quantity to meet **minimum notional (≥100 USDT)**  
- ⭐ TWAP (time-sliced market orders)  
- ⭐ Clean OOP structure (`BasicBot` class)  

---

## 🗂 Project Structure

project/
│── basic_bot.py
│── .env # (NOT committed)
│── .env.example
│── README.md
│── basicbot.log # generated automatically after running
│── venv/ # optional

yaml
Copy code

---

## ⚙️ Setup Instructions

1. **Create & activate virtual environment**

Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
Windows


venv\Scripts\activate
Install dependencies


pip install python-binance python-dotenv
Create .env (in project root)


BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
⚠️ Do not add quotes, do not commit .env to GitHub.

Create Testnet API keys at:
https://testnet.binancefuture.com/en/futures → Profile → API Management (Futures Testnet)

Enable: Trade / Futures

▶️ Usage (CLI Examples)
Market Order

python basic_bot.py market --symbol BTCUSDT --side BUY --qty 0.002

Limit Order

python basic_bot.py limit --symbol ETHUSDT --side BUY --qty 0.04 --price 3000

Stop-Limit Order

python basic_bot.py stoplimit --symbol BTCUSDT --side SELL --qty 0.002 --stop 65000 --price 64900

TWAP (split into slices)

python basic_bot.py twap --symbol BTCUSDT --side BUY --total_qty 0.01 --slices 5 --interval 10

📜 Logging
All actions are logged to basicbot.log with timestamps, API responses, and stack traces for errors. This file is created automatically in the project folder when you run the bot.

🔒 Security & Best Practices
Use Testnet API keys for development and never use mainnet keys in this project.

Never commit .env (use .gitignore).

Validate quantities & prices — the bot auto-adjusts quantity to meet minimum notional requirements.
