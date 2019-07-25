# Bus Bot Data Manager

Data manager for Telegram bots based on serving Stops/Bus information for a public transportation system. Written mainly to use with the [VigoBus-TelegramBot](https://github.com/David-Lor/VigoBus-TelegramBot).

The data manager store all the persistent data required by the bot, starting with the Saved Stops that bot users can store.

The communication between the bot backend and this data manager is through a REST API, serving GET, POST and DELETE endpoint methods. The API is powered by [FastAPI](https://github.com/tiangolo/fastapi).

## Requirements

- Python >= 3.6
- Requirements listed on [requirements.txt](requirements.txt)
