#!/bin/bash

DIR="/opt/remote_desktop"
VNC="$DIR/noVNC_0.6"
LAUNCHER="$DIR/start"
STOP="$DIR/stop"
SERVER="$DIR/remote_desktop"
SERVICE="/etc/systemd/system/remote_desktop.service"


if [[ $(id -u) != 0 ]]
then
    echo "Please log in as root user to run this utility."
    exit 1
fi

if [[ "$DIR" == "/" ]] || [[ -z "$DIR" ]]
then
    echo "Please check variable DIR."
    exit 1
fi



# . . . . . Main . . . . . #

echo -e "\e[33m[ Installing Dependencies ]\e[0m"

apt install -y tightvncserver websockify net-tools


echo -e "\n\e[33m[ Installing VNC ]\e[0m"

[[ -d "$DIR" ]] && rm -r "$DIR"

mkdir -p "$DIR"
wget  -q --show-progress -O "$VNC" "https://github.com/wildfoundry/specialprojects-public/raw/remote-desktop/noVNC-stable-v0.6.zip"
unzip -q "$VNC" -d "$DIR"
rm    "$VNC"

VNC="$DIR/noVNC-stable-v0.6"


echo """#!/bin/bash

if [[ \$(id -u) != 0 ]]
then
        echo "Please log in as root user to run this utility."
        exit 1
fi

if netstat -pant | grep -q :80
then
        echo Dataplicity wormhole port 80 is currently busy running another service. Please deactivate it and try again.
        exit 1
fi

$VNC/utils/launch.sh --vnc 127.0.0.1:5901 --listen 80
""" > "$SERVER" && chmod +x "$SERVER"


echo """[Unit]
Description=Remote Desktop

[Service]
Type=idle
ExecStart=$SERVER

[Install]
WantedBy=multi-user.target
""" > "$SERVICE"
systemctl enable remote_desktop
systemctl start  remote_desktop


echo """#!/bin/bash

vncserver -kill :1
""" > "$STOP" && chmod +x "$STOP"


echo """#!/bin/bash

vncserver -kill :1 2>/dev/null

vncserver :1 -geometry 1920x1080 -depth 24 -dpi 96 
""" > "$LAUNCHER" && chmod +x "$LAUNCHER"


echo -e "\n\e[33mTo launch remote desktop access please run command: \e[0m"
echo "$LAUNCHER"

