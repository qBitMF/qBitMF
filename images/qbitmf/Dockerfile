FROM ubuntu:jammy

# Install prereqs
RUN apt update \
    && apt upgrade -y \
    && apt install -y --no-install-recommends \
    curl ca-certificates wireguard iproute2 \
    iptables vim iputils-ping mtr dnsutils tcpdump \
    socat build-essential pkg-config qtbase5-dev \
    qttools5-dev libqt5svg5-dev libboost-dev \
    libboost-tools-dev libboost-system-dev \
    libssl-dev libgcrypt-dev ninja-build cmake \
    zlib1g-dev libgeoip-dev libboost-chrono-dev \
    libboost-random-dev qttools5-dev-tools tmux vnstat \
    && apt-get clean \
    && apt --purge autoremove -y

# Build libtorrent
ADD deps/libtorrent-multiface /libtorrent-multiface
WORKDIR /libtorrent-multiface
RUN cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr . \
    && make -j$(nproc) \
    && make install

# Build qbittorrent
ADD deps/qbittorrent-multiface /qbittorrent-multiface
WORKDIR /qbittorrent-multiface
CMD ./configure --disable-gui \
    && make -j$(nproc) \
    && make install

# Add the abc user
RUN useradd --no-create-home --home-dir /config --shell /bin/bash abc

ENV HOME="/config" \
XDG_CONFIG_HOME="/config" \
XDG_DATA_HOME="/config"

WORKDIR /

# Add default config files
ADD qBittorrent.conf.default /qBittorrent.conf.default
ADD resolv.conf.default /resolv.conf.default

# Add scripts
ADD start.sh /start.sh
ADD start-unpriv.sh /start-unpriv.sh
ADD make-wg-netns.py /make-wg-netns.py

# Add a convenience script for accessing bash within the wg netns
# Accessible via "docker-compose execute qbitmf wgbash"
ADD wgbash.sh /usr/bin/wgbash

CMD ["/bin/bash", "/start.sh"]
