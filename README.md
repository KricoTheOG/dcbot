# Discord BTC Shop Bot

This bot allows users to buy virtual items using Bitcoin (BTC) via NOWPayments.

## Setup

1. Replace API keys in `config.json`
2. Run the Flask webhook server: `python webhook.py`
3. Start the bot: `python bot.py`
4. Commands:
   - `!shop` — view items
   - `!buy <item_id>` — get BTC payment link
   - `!inventory` — see owned items

Make sure the webhook is accessible by NOWPayments (use `ngrok` for local testing).