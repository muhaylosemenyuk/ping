import os
import subprocess
import time
from telegram import Bot
import toml
import json
import asyncio

def read_config():
    return toml.load("config.toml")

def read_servers():
    config = read_config()
    return config["servers"]["server_list"]

def read_previous_statuses():
    if os.path.exists("status.json"):
        with open("status.json", "r") as status_file:
            return json.load(status_file)
    else:
        return {}

def save_previous_statuses(previous_statuses):
    with open("status.json", "w") as status_file:
        json.dump(previous_statuses, status_file)

async def send_telegram_message(message):
    bot = Bot(token=read_config()["telegram"]["bot_token"])
    await bot.send_message(chat_id=read_config()["telegram"]["chat_id"], text=message)

async def check_server_status(name, ip):
    try:
        subprocess.check_output(['ping', '-c', '3', ip])
        current_status = 'up'
    except subprocess.CalledProcessError:
        current_status = 'down'

    previous_statuses = read_previous_statuses()

    if ip not in previous_statuses:
        previous_statuses[ip] = None

    if current_status != previous_statuses[ip]:
        if current_status == 'up':
            message = f'✅ [ {name} ] ({ip}) >>> Server is {current_status}'
        else:
            message = f'❌ [ {name} ] ({ip}) >>> Server is {current_status}'
        await send_telegram_message(message)
        previous_statuses[ip] = current_status

        save_previous_statuses(previous_statuses)

async def main():
    while True:
        SERVERS_TO_PING = read_servers()
        for server in SERVERS_TO_PING:
            server_name = server["name"]
            server_ip = server["ip"]
            await check_server_status(server_name, server_ip)
            await asyncio.sleep(1)  # Зачекайте 1 секунду перед переходом до наступного серверу
        await asyncio.sleep(60)  # Зачекайте 1 хвилину перед наступною ітерацією циклу

if __name__ == "__main__":
    asyncio.run(main())
