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
# Add servers to the config.toml
nano config.toml
```

```bash
# Create service file
sudo tee /etc/systemd/system/ping.service > /dev/null <<EOF
[Unit]
Description=Ping Bot Service
After=network.target

[Service]
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
