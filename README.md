# Absol - Smart OOM Killer

## How to install as a service

## Step 1: Save the script to the official directory

Linux systems expect user executables to be in the `/usr/local/bin/` folder. Let's copy your `absol.py` there and ensure it has execution permissions:

```bash
sudo cp absol.py /usr/local/bin/absol.py
sudo chmod +x /usr/local/bin/absol.py
```

## Step 2: Create the Service file

Now let's create the service configuration for the Linux service manager (systemd).

```bash
sudo vim /etc/systemd/system/absol.service
```

Paste the configuration below inside. Note that we are telling it to run as root (essential for Absol to have permission to kill any process that is freezing the machine) and to restart automatically (`Restart=always`) if the script closes due to an error:

```ini
[Unit]
Description=Absol - Smart OOM Killer (RAM Monitor)
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /usr/local/bin/absol.py
Restart=always
RestartSec=5
User=root

[Install]
WantedBy=multi-user.target
```

*(To save and exit in Vim: press `Esc`, type `:wq`, and press `Enter`).*

## Step 3: Reload the Daemon and Start the Service

Now we need to notify Linux that there is a new service, configure it to start on boot, and start it right now. Run one command at a time:

Update the internal list of services:

```bash
sudo systemctl daemon-reload
```

Enable it to start automatically when you turn on the PC:

```bash
sudo systemctl enable absol.service
```

Start it right now:

```bash
sudo systemctl start absol.service
```

## How to know if it worked? (Debugging)

To confirm if Absol is happily running silently in the shadows, type:

```bash
sudo systemctl status absol.service
```

You should see a green dot with the words `active (running)`.