from basic_bot import BasicBot
import os

def main_menu():
    print("\n=== Trading Bot UI ===")
    print("1. Market Order")
    print("2. Limit Order")
    print("3. Stop-Limit Order")
    print("4. TWAP Order")
    print("5. Exit")
    return input("Choose an option: ")

def main():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    bot = BasicBot(api_key, api_secret)

    while True:
        choice = main_menu()

        if choice == "1":
            symbol = input("Symbol: ")
            side = input("Side (BUY/SELL): ").upper()
            qty = float(input("Quantity: "))
            print(bot.place_market_order(symbol, side, qty))

        elif choice == "2":
            symbol = input("Symbol: ")
            side = input("Side (BUY/SELL): ").upper()
            qty = float(input("Quantity: "))
            price = float(input("Price: "))
            print(bot.place_limit_order(symbol, side, qty, price))

        elif choice == "3":
            symbol = input("Symbol: ")
            side = input("Side (BUY/SELL): ").upper()
            qty = float(input("Quantity: "))
            stop = float(input("Stop Price: "))
            price = float(input("Limit Price: "))
            print(bot.place_stop_limit(symbol, side, qty, stop, price))

        elif choice == "4":
            symbol = input("Symbol: ")
            side = input("Side (BUY/SELL): ").upper()
            total = float(input("Total Quantity: "))
            slices = int(input("Slices: "))
            interval = int(input("Interval Seconds: "))
            print(bot.twap_market(symbol, side, total, slices, interval))

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
