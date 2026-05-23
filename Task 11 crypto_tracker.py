# Live Cryptocurrency Price Tracker
# Uses CoinGecko free API - no key needed
# Bonus: price history, CSV save, trend indicator, threshold alert

import requests
import time
import os
import csv
from datetime import datetime

# store price history for trend graph (bonus)
price_log = {}

# coins user is tracking
tracked_coins = []

# alert thresholds set by user
alert_targets = {}

# base url for coingecko free api
api_base = "https://api.coingecko.com/api/v3"

# how many seconds between auto refresh
refresh_wait = 30

def clear_screen():
    # clear terminal for clean display
    os.system("cls" if os.name == "nt" else "clear")

def fetch_prices(coin_list):
    # fetch current price and 24h change for all tracked coins
    coins_joined = ",".join(coin_list)
    url = f"{api_base}/simple/price?ids={coins_joined}&vs_currencies=usd&include_24hr_change=true"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print("  [!] No internet connection.")
        return None
    except requests.exceptions.Timeout:
        print("  [!] Request timed out.")
        return None
    except requests.exceptions.HTTPError as err:
        print(f"  [!] API error: {err}")
        return None

def log_price(coin, price):
    # save price with timestamp to history (bonus feature)
    if coin not in price_log:
        price_log[coin] = []
    timestamp = datetime.now().strftime("%H:%M:%S")
    price_log[coin].append((timestamp, price))
    # keep only last 10 readings
    price_log[coin] = price_log[coin][-10:]

def get_trend_arrow(coin):
    # show up/down trend based on last 2 price readings
    history = price_log.get(coin, [])
    if len(history) < 2:
        return "  --"
    last_price = history[-1][1]
    prev_price = history[-2][1]
    if last_price > prev_price:
        return "  UP"
    elif last_price < prev_price:
        return "  DOWN"
    return "  FLAT"

def check_alerts(coin, current_price):
    # check if price crossed user set threshold (bonus alert feature)
    if coin in alert_targets:
        target = alert_targets[coin]
        if current_price >= target:
            print(f"\n  *** ALERT: {coin.upper()} hit your target ${target:.2f}! Current: ${current_price:.2f} ***")

def display_prices(data):
    # print prices in a clean table format
    print("\n" + "=" * 55)
    print(f"  {'COIN':<18} {'PRICE (USD)':>12} {'24H %':>8} {'TREND':>8}")
    print("=" * 55)
    for coin in tracked_coins:
        if coin in data:
            coin_data = data[coin]
            price = coin_data.get("usd", 0)
            change = coin_data.get("usd_24h_change", 0)
            # log price for trend history
            log_price(coin, price)
            # check if alert should fire
            check_alerts(coin, price)
            trend = get_trend_arrow(coin)
            change_display = f"{change:+.2f}%" if change else "N/A"
            print(f"  {coin.upper():<18} ${price:>12,.4f} {change_display:>8} {trend:>8}")
        else:
            print(f"  {coin.upper():<18} {'Not Found':>12}")
    print("=" * 55)
    print(f"  Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def save_to_csv():
    # save full price history to csv file (bonus feature)
    if not price_log:
        print("  No data to save yet.")
        return
    filename = f"crypto_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Coin", "Time", "Price (USD)"])
        for coin, records in price_log.items():
            for time_stamp, price in records:
                writer.writerow([coin.upper(), time_stamp, price])
    print(f"  Saved to {filename}")

def set_alert():
    # let user set a price alert for a coin
    if not tracked_coins:
        print("  No coins tracked yet. Add some first.")
        return
    print(f"  Tracked coins: {', '.join(tracked_coins)}")
    coin_name = input("  Enter coin name to set alert: ").strip().lower()
    if coin_name not in tracked_coins:
        print("  Coin not in your list.")
        return
    try:
        target_price = float(input(f"  Alert when {coin_name} reaches $: "))
        alert_targets[coin_name] = target_price
        print(f"  Alert set for {coin_name.upper()} at ${target_price:.2f}")
    except ValueError:
        print("  Invalid price entered.")

def add_coin():
# add a new coin to tracking list
    coin_name = input("  Enter coin id (e.g. bitcoin, ethereum, dogecoin): ").strip().lower()
    if coin_name in tracked_coins:
        print("  Already tracking this coin.")
        return
 # quick check if coin exists
    test = fetch_prices([coin_name])
    if test and coin_name in test:
        tracked_coins.append(coin_name)
        print(f"  Added {coin_name.upper()} to your tracker.")
    else:
        print("  Coin not found. Check spelling or try the full CoinGecko ID.")

def view_prices():
# fetch and display prices for all tracked coins
    if not tracked_coins:
        print("  No coins in list. Please add some first.")
        return
    data = fetch_prices(tracked_coins)
    if data:
        display_prices(data)

def auto_refresh():
# keep refreshing prices every N seconds until user stops
    if not tracked_coins:
        print("  Add coins first.")
        return
    print(f"  Auto-refreshing every {refresh_wait}s. Press Ctrl+C to stop.\n")
    try:
        while True:
            clear_screen()
            print("  [Auto Refresh Mode]")
            view_prices()
            time.sleep(refresh_wait)
    except KeyboardInterrupt:
        print("\n  Stopped auto-refresh.")

def show_menu():
    # display main menu options
    print("\n  ===  CRYPTO PRICE TRACKER  ===")
    print("  1. View Prices")
    print("  2. Add Cryptocurrency")
    print("  3. Auto Refresh Prices")
    print("  4. Set Price Alert")
    print("  5. Save History to CSV")
    print("  6. Exit")
    print("  ==============================")

def main():
    # program starts here
    print("  Welcome to Live Crypto Tracker!")
    # add some default coins to start with
    tracked_coins.extend(["bitcoin", "ethereum", "dogecoin"])
    print(f"  Default coins loaded: {', '.join(tracked_coins)}")

    while True:
        show_menu()
        user_choice = input("  Choose option (1-6): ").strip()

        if user_choice == "1":
            view_prices()
        elif user_choice == "2":
            add_coin()
        elif user_choice == "3":
            auto_refresh()
        elif user_choice == "4":
            set_alert()
        elif user_choice == "5":
            save_to_csv()
        elif user_choice == "6":
            print("  Goodbye! Happy trading!")
            break
        else:
            print("  Invalid choice. Enter 1 to 6.")

# run only when executed directly
if __name__ == "__main__":
    main()