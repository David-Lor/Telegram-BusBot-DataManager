# Bus Bot Data Manager

Data manager for Telegram bots based on serving Stops/Bus information for a public transportation system. Written mainly to use with the [VigoBus-TelegramBot](https://github.com/David-Lor/VigoBus-TelegramBot).

The data manager store all the persistent data the bot works with, mainly the Saved Stops that bot users can store, on MongoDB.

The communication between the bot backend and this data manager is through a REST API, serving GET, POST and DELETE endpoint methods. The API is powered by [FastAPI](https://github.com/tiangolo/fastapi) and fully async.

## Endpoints

- GET `/status`: get API status (healthcheck)
- GET `/stops/{userid}`: get all the Stops saved by the given User
- POST `/stops`: insert or update a Saved Stop (stop data in body request)
- DELETE `/stops/{userid}/{stopid}`: remove the given Stop from the given User

## Changelog

- 0.0.1
    - Initial release
    - Functional GET, POST, DELETE methods connected with MongoDB

## Requirements

- Python >= 3.6
- Requirements listed on [requirements.txt](requirements.txt)
- A MongoDB server
