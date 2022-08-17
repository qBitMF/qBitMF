#!/bin/bash

# Everything here runs unprivileged as the PUID/PGID user

# Configure qBittorrent defaults, if not done already
if [ ! -f /config/qBittorrent/config/qBittorrent.conf ]
then
    mkdir -p /config/qBittorrent/config
    cp /qBittorrent.conf.default /config/qBittorrent/config/qBittorrent.conf
    chown abc:abc /config/qBittorrent/config/qBittorrent.conf
fi

# Run qBittorrent and daemonize
qbittorrent-nox --profile=/config --webui-port=18080 -d
