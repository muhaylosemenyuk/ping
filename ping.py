import os
import subprocess
import time
from telegram import Bot
import toml
import json
import asyncio

# Reading configuration data from the config.toml file
config = toml.load("config.toml")
TELEGRAM_BOT_TOKEN = config["telegram"]["bot_token"]
CHAT_ID = config["telegram"]["chat_id"]
SERVERS_TO_PING = config["servers"]["server_list"]

STATUS_FILE = "status.json"

# Creating a status file if it does not exist
if not os.path.exists(STATUS_FILE):
    # Create a status file with default values ​​(None)
    default_statuses = {server["ip"]: None for server in SERVERS_TO_PING}
    with open(STATUS_FILE, "w") as status_file:
        json.dump(default_statuses, status_file)

# Reading previous statuses from a file
with open(STATUS_FILE, "r") as status_file:
    previous_statuses = json.load(status_file)

# Function for sending a message in Telegram
async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)
    print(message)

# Function for pinging the server and notification in Telegram
async def check_server_status(name, ip):
    try:
        subprocess.check_output(['ping', '-c', '3', ip])
        current_status = 'up'
    except subprocess.CalledProcessError:
        current_status = 'down'

    # Status change check
    if current_status != previous_statuses[ip]:
        if current_status == 'up':
            message = f'✅ [ {name} ] ({ip}) >>> Server is {current_status}'
        else:
            message = f'❌ [ {name} ] ({ip}) >>> Server is {current_status}'
        await send_telegram_message(message)
        previous_statuses[ip] = current_status

        # Saving the new state to a file
        with open(STATUS_FILE, "w") as status_file:
            json.dump(previous_statuses, status_file)

async def main():
    while True:
        for server in SERVERS_TO_PING:
            server_name = server["name"]
            server_ip = server["ip"]
            await check_server_status(server_name, server_ip)
            await asyncio.sleep(1)  # Зачекайте 1 секунду перед переходом до наступного серверу
        await asyncio.sleep(60)  # Зачекайте 1 хвилину перед наступною ітерацією циклу

if __name__ == "__main__":
    asyncio.run(main())
