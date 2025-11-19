# 🚀 Simplified Binance Futures Testnet Trading Bot

# A Python-based trading bot for Binance USDT-M Futures Testnet, supporting Market, Limit, Stop-Limit, and TWAP orders with full logging and automatic notional validation.

✨ Features

🚀 Market Orders

📌 Limit Orders

🛑 Stop-Limit Orders

📊 TWAP (Time Weighted Average Price) Strategy

🔧 Auto-adjusts quantity to satisfy minimum notional (≥100 USDT)

🧩 Clean OOP architecture (BasicBot class)

📄 Logging to basicbot.log

🧪 Error handling and CLI input validation

🎁 Bonus: Simple CLI UI Menu for human-friendly interaction

## 🗂 Project Structure

```text
project/
│── basic_bot.py
│── .env                # NOT committed
│── .env.example
│── basicbot.log        # auto-generated
│── README.md
│── venv/               # optional

```
⚙️ Installation

Install required packages using pip:
```
pip install python-binance python-dotenv
```
⚙️ Setup
Create Virtual Environment

Linux/macOS
```
python3 -m venv venv
source venv/bin/activate
```

Windows
```
python -m venv venv
venv\Scripts\activate
```
Create .env File
```
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

⚠️ Do NOT add quotes
⚠️ Do NOT commit .env to GitHub

Generate Testnet API Keys

Visit:
https://testnet.binancefuture.com/en/futures
 → Profile → API Management
Enable:

✔ Trade

✔ Futures

▶️ Usage (Command Line)
Market Order
```
python basic_bot.py market --symbol BTCUSDT --side BUY --qty 0.002
```
Limit Order
```
python basic_bot.py limit --symbol ETHUSDT --side BUY --qty 0.04 --price 3000
```
Stop-Limit Order
```
python basic_bot.py stoplimit --symbol BTCUSDT --side SELL --qty 0.002 --stop 65000 --price 64900
```
TWAP (Split Order Execution)
```
python basic_bot.py twap --symbol BTCUSDT --side BUY --total_qty 0.01 --slices 5 --interval 10
```
🎁 Bonus: Simple CLI Menu UI

Run:
```
python ui.py
```

You will see:
```
=== Trading Bot UI ===
1. Market Order
2. Limit Order
3. Stop-Limit Order
4. TWAP Order
5. Exit
Choose an option:
```
Example Input for Market Order
```
1
Symbol: BTCUSDT
Side (BUY/SELL): BUY
Quantity: 0.002
```

Output:
```
Placing MARKET order...
{'symbol': 'BTCUSDT', 'orderId': 1234567, 'status': 'FILLED', ...}
```
📜 Logging

All actions are stored in:
```
basicbot.log
```

Includes:
- timestamps
- API requests
- API responses
- errors / exceptions