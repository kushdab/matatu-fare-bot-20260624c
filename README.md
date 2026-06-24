# Matatu Fare Bot 2026

A crowdsourced Telegram bot designed for Nairobi commuters to track matatu (public transport) fare fluctuations during peak hours. 

## Features
- **Get Fares**: Retrieve average and peak fares for specific routes.
- **Report Fares**: Contribute to the database by reporting what you just paid.
- **Route Listing**: Discover which routes are currently being tracked.
- **Data Persistence**: Stores data locally in `fares.json`.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get a Bot Token from [BotFather](https://t.me/BotFather) on Telegram.

3. Set your environment variable:
   ```bash
   export TELEGRAM_TOKEN='your_token_here'
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Commands
- `/start`: Initialize the bot.
- `/fare <route>`: e.g., `/fare CBD-Westlands`.
- `/report <route> <amount>`: e.g., `/report CBD-Westlands 70`.
- `/routes`: Show all tracked routes.
- `/help`: Show usage info.