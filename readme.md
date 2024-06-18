```
systemctl status earthquake.service
```


```
[Unit]
Description=Earthquake Data Fetching Service
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/python3 /root/python/earthquake/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

```

```
systemctl enable earthquake.service
systemctl start earthquake.service
systemctl stop earthquake.service
systemctl status earthquake.service
```

```
systemctl restart earthquake.service
```
