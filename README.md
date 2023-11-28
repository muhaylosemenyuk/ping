# Install

```bash
# Update system and install python
sudo apt update
sudo apt install python3 python3-pip git python-telegram-bot
pip install toml
```

```bash
# Clone repository
git clone https://github.com/muhaylosemenyuk/ping.git
cd ~/ping
```

```bash
# Add servers and telegram data to the config.toml
nano config.toml
```
![image](https://github.com/muhaylosemenyuk/ping/assets/79005788/d587c877-b9f5-429a-9387-cd340333b71c)

Enter your TELEGRAM_API_KEY

[How to get Telegram bot API token](https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token)

Enter your MONITORING_CHAT_ID

[How to get a group chat id?](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)


```bash
# Create service file
sudo tee /etc/systemd/system/ping.service > /dev/null <<EOF
[Unit]
Description=Ping Bot Service
After=network.target

[Service]
User=root
ExecStart=/usr/bin/python3 /root/ping/ping.py
WorkingDirectory=/root/ping/
Restart=always
RestartSec=5

[Install]
WantedBy=default.target

EOF
```

```bash
systemctl daemon-reload
systemctl enable ping
systemctl restart ping
```

```bash
# Check logs
journalctl -u ping -f -o cat
```
