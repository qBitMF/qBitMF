#!/bin/bash

# Everything here runs on each container startup.

# Set user's UID and GID
PUID=${PUID:-911}
PGID=${PGID:-911}

groupmod -o -g "$PGID" abc
usermod -o -u "$PUID" abc

chown abc:abc /config
chown abc:abc /downloads

# Process interface files
rm -rf /interface-state
mkdir -p /interface-state

python3 /make-wg-netns.py

# Set DNS to Cloudflare
# By default, docker tries to handle DNS so it can resolve internal hostnames,
# So we need to override it at runtime, rather than through the Dockerfile.

# Also note that we can't use the DNS from WireGuard config files, as those
# might end up being interface-specific. We need a DNS server that can be
# contacted through any interface.
cp /resolv.conf.default /etc/resolv.conf

# Run qBittorrent as an unprivileged netns'd user
ip netns exec wg su -m abc -c /start-unpriv.sh

# Run socat outside the wg netns, to access the qBittorrent WebUI without
# qBittorrent losing its isolation.
exec socat tcp-listen:8080,reuseaddr,fork exec:'ip netns exec wg socat STDIO "tcp-connect\:127.0.0.1\:18080"',nofork
