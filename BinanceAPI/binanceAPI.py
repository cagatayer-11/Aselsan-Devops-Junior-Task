import requests
import time
import logging

# Basic configuration for logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]  # Outputs to console
)
binance = "https://api.binance.com"
avg_price = "/api/v3/avgPrice"


def main():
    def get_price():
        response = requests.get(binance + avg_price + "?symbol=BTCUSDT")
        return round(float(response.json()["price"]), 2)

    early_price = get_price()
    print(f"Initial BTCUSDT price {early_price}")
    logging.info(f"Initial BTCUSDT price {early_price}")
    while True:
        time.sleep(300)
        current_price = get_price()
        if current_price > early_price:
            print(f"BTCUSDT price increased to {current_price}")
            logging.info(f"BTCUSDT price increased to {current_price}")

        elif current_price < early_price:
            print(f"BTCUSDT price decreased to {current_price}")
            logging.info(f"BTCUSDT price increased to {current_price}")

        early_price = current_price


if __name__ == '__main__':
    main()
