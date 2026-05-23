# Project 11: Live Cryptocurrency Price Tracker

A Python-based CLI application that fetches and displays real-time cryptocurrency prices using the CoinGecko public API. This project demonstrates clean data integration, exception handling, and automated data monitoring.

## 🚀 Features
- **Real-Time Tracking:** Live USD prices and 24-hour percentage changes.
- **Auto-Refresh Mode:** Automatically updates prices at set intervals (30s).
- **Error Handling:** Gracefully manages network drops, API timeouts, and invalid inputs.
- **Bonus Features:** Visual trend arrows (▲/▼), custom price threshold alerts, and history logging to CSV.

## 🛠️ Setup & Usage

1. **Install Dependencies:**
   ```bash
   pip install requests

2. **Run the Application:**

Bash
python crypto_tracker.py

3.📊 Sample Output
=======================================================
  COIN               PRICE (USD)    24H %        TREND
=======================================================
  BITCOIN            $67,420.5000   +1.45%       UP ▲
  ETHEREUM           $3,510.2500    -0.85%     DOWN ▼
=======================================================

4.**Demo video**:
You can see working in :
Crypto tracker demo video.mp4
