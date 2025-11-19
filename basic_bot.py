from dotenv import load_dotenv
load_dotenv()

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import argparse, os, time, logging, sys, math
from datetime import datetime

# === Logging setup ===
logger = logging.getLogger("basicbot")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("basicbot.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        """Initialize Binance Futures Testnet client"""
        self.client = Client(api_key, api_secret)

        # ⭐ FORCE futures testnet URL (python-binance does NOT switch automatically)
        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

        logger.info("Initialized BasicBot (testnet=%s)", testnet)

    # ----------------------------------------------------------------------
    # Internal Helpers
    # ----------------------------------------------------------------------
    def _log_and_raise(self, stage, exc):
        logger.exception("%s - Exception: %s", stage, exc)
        raise

    def _get_symbol_info(self, symbol):
        """Fetch exchangeInfo for a symbol and return dict of filters."""
        try:
            info = self.client.futures_exchange_info()
            for s in info.get("symbols", []):
                if s["symbol"] == symbol:
                    return s
            raise ValueError(f"Symbol {symbol} not found in exchange info")
        except Exception as e:
            self._log_and_raise("_get_symbol_info", e)

    def _adjust_qty_to_min_notional(self, symbol, qty, price=None):
        """
        Ensure price * qty >= minNotional.
        Auto-corrects the quantity if needed.
        """
        try:
            s = self._get_symbol_info(symbol)

            # Extract minNotional & stepSize
            min_notional = 100.0
            step_size = None

            for f in s.get("filters", []):
                if f["filterType"] == "MIN_NOTIONAL":
                    min_notional = float(f["notional"])
                if f["filterType"] == "LOT_SIZE":
                    step_size = float(f["stepSize"])

            # Fetch mark price if no limit price provided
            used_price = price
            if used_price is None:
                mp = self.client.futures_mark_price(symbol=symbol)
                used_price = float(mp["markPrice"])

            notional = float(qty) * used_price

            if notional >= min_notional:
                return float(qty), used_price

            # Compute minimum qty
            required_qty = min_notional / used_price

            # Round up with step size
            if step_size:
                steps = math.ceil(required_qty / step_size)
                adjusted_qty = steps * step_size
            else:
                adjusted_qty = required_qty

            logger.info(
                "Notional too small (%.4f < %.4f). Adjusting qty %.6f -> %.6f",
                notional, min_notional, float(qty), adjusted_qty,
            )
            return float(adjusted_qty), used_price

        except Exception as e:
            self._log_and_raise("_adjust_qty_to_min_notional", e)

    # ----------------------------------------------------------------------
    # ORDER TYPES
    # ----------------------------------------------------------------------
    def place_market_order(self, symbol, side, quantity, reduce_only=False):
        """Place Market Order"""
        try:
            qty, _ = self._adjust_qty_to_min_notional(symbol, quantity)

            logger.info("Placing MARKET order: %s %s %s", symbol, side, qty)
            resp = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty,
                reduceOnly=reduce_only
            )
            logger.info("MARKET order response: %s", resp)
            return resp

        except (BinanceAPIException, BinanceOrderException) as e:
            self._log_and_raise("place_market_order", e)

    def place_limit_order(self, symbol, side, quantity, price, time_in_force="GTC", reduce_only=False):
        """Place Limit Order"""
        try:
            qty, _ = self._adjust_qty_to_min_notional(symbol, quantity, price)

            logger.info("Placing LIMIT order: %s %s %s @ %s", symbol, side, qty, price)
            resp = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce=time_in_force,
                quantity=qty,
                price=str(price),
                reduceOnly=reduce_only
            )
            logger.info("LIMIT order response: %s", resp)
            return resp

        except (BinanceAPIException, BinanceOrderException) as e:
            self._log_and_raise("place_limit_order", e)

    def place_stop_limit(self, symbol, side, quantity, stopPrice, price, time_in_force="GTC"):
        """STOP-LIMIT order"""
        try:
            qty, _ = self._adjust_qty_to_min_notional(symbol, quantity, price)

            logger.info("Placing STOP-LIMIT: %s %s %s stop=%s price=%s",
                        symbol, side, qty, stopPrice, price)

            resp = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="STOP",
                timeInForce=time_in_force,
                quantity=qty,
                price=str(price),
                stopPrice=str(stopPrice)
            )
            logger.info("STOP-LIMIT response: %s", resp)
            return resp

        except (BinanceAPIException, BinanceOrderException) as e:
            self._log_and_raise("place_stop_limit", e)

    def get_order_status(self, symbol, orderId=None, origClientOrderId=None):
        """Fetch order status"""
        try:
            params = {"symbol": symbol}
            if orderId:
                params["orderId"] = orderId
            if origClientOrderId:
                params["origClientOrderId"] = origClientOrderId

            resp = self.client.futures_get_order(**params)
            logger.info("Order status: %s", resp)
            return resp

        except Exception as e:
            self._log_and_raise("get_order_status", e)

    def twap_market(self, symbol, side, total_qty, slices=5, interval_seconds=10):
        """Simple TWAP: slices market orders over time"""
        try:
            piece = total_qty / slices
            executed = []

            logger.info("Starting TWAP: %s %s total=%s slices=%d interval=%ds",
                        symbol, side, total_qty, slices, interval_seconds)

            for i in range(slices):
                qty = round(piece, 8)
                resp = self.place_market_order(symbol, side, qty)
                executed.append(resp)

                if i < slices - 1:
                    time.sleep(interval_seconds)

            logger.info("TWAP complete.")
            return executed

        except Exception as e:
            self._log_and_raise("twap_market", e)


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")

    p.add_argument("--api-key", default=os.getenv("BINANCE_API_KEY"))
    p.add_argument("--api-secret", default=os.getenv("BINANCE_API_SECRET"))

    sub = p.add_subparsers(dest="cmd", required=True)

    # Market
    m = sub.add_parser("market")
    m.add_argument("--symbol", required=True)
    m.add_argument("--side", choices=["BUY", "SELL"], required=True)
    m.add_argument("--qty", type=float, required=True)

    # Limit
    l = sub.add_parser("limit")
    l.add_argument("--symbol", required=True)
    l.add_argument("--side", choices=["BUY", "SELL"], required=True)
    l.add_argument("--qty", type=float, required=True)
    l.add_argument("--price", type=float, required=True)

    # Stop-Limit
    s = sub.add_parser("stoplimit")
    s.add_argument("--symbol", required=True)
    s.add_argument("--side", choices=["BUY", "SELL"], required=True)
    s.add_argument("--qty", type=float, required=True)
    s.add_argument("--stop", type=float, required=True)
    s.add_argument("--price", type=float, required=True)

    # TWAP
    t = sub.add_parser("twap")
    t.add_argument("--symbol", required=True)
    t.add_argument("--side", choices=["BUY", "SELL"], required=True)
    t.add_argument("--total_qty", type=float, required=True)
    t.add_argument("--slices", type=int, default=5)
    t.add_argument("--interval", type=int, default=10)

    return p.parse_args()


def main():
    args = parse_args()

    if not args.api_key or not args.api_secret:
        logger.error("API credentials NOT provided. Check .env file.")
        return

    bot = BasicBot(args.api_key, args.api_secret, testnet=True)

    try:
        if args.cmd == "market":
            print(bot.place_market_order(args.symbol, args.side, args.qty))

        elif args.cmd == "limit":
            print(bot.place_limit_order(args.symbol, args.side, args.qty, args.price))

        elif args.cmd == "stoplimit":
            print(bot.place_stop_limit(args.symbol, args.side, args.qty, args.stop, args.price))

        elif args.cmd == "twap":
            print(bot.twap_market(args.symbol, args.side, args.total_qty, args.slices, args.interval))

    except Exception as e:
        logger.error("Execution error: %s", e)


if __name__ == "__main__":
    main()
