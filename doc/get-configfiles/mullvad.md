## Generating WireGuard config files from Mullvad VPN


After logging in, go to https://mullvad.net/en/account/#/wireguard-config and click "Generate key".

Then, select your Country, City, and Server underneath. **DO NOT** pick "All servers", as this may cause qBitMF to connect to the same VPN server multiple times.

> **Note**
> It's recommended to look at the [Mullvad Servers](https://mullvad.net/en/servers/) page to see the speeds of each server.

Then, once you're happy with what you've picked, click `Download file`.

![Mullvad WireGuard configuration file generator screenshot](/doc/img/19eb88e382a9e494ee661b920e378e807596e72cebb23c30860d2fd8ec6cee78.png)  

> **Warning**
> Do not use us30-wireguard. Pick a different server, because us30 is bound to get overloaded if everyone picks it.

Once you've clicked `Download file`, you should have a wireguard config file (in my case, called `mlvd-us30.conf`). It should look something like:

```ini
[Interface]
PrivateKey = (snipped)
Address = 10.64.23.144/32,fc00:bbbb:bbbb:bb01::1:178f/128
DNS = 10.64.0.1

[Peer]
PublicKey = RW+wwTv4BqRNbHPZFcIwl74f9kuRQlFLxnaocpMyKgw=
AllowedIPs = 0.0.0.0/0,::0/0
Endpoint = 174.127.113.8:51820
```

Save this file in a directory somewhere.

Next, it's recommended you configure an incoming port. Go to https://mullvad.net/en/account/#/ports. You will see the WireGuard key you generated under "My devices" with a unique name.

Select the city that you generated the configuration file in (in my case, `Dallas, TX`), and select that device name beside it, then click "Add port".

![Mullvad port forwarding screenshot](/doc/img/70a681d2ac317c2a2e97c990c4bab1c7a1369b27d660fd0b46679880079aeb63.png)  

Once you've added the port, you will see the port show up under your device:

![Mullvad port forwarding screenshot 2](/doc/img/baff7a265e7f889ecf645b3d56da36d65cbfaedaa444d42de4a04aee6d10d89a.png)  

Make a note of this port (in my case, port 59004), and the fact that it's associated with the config file you just downloaded (in my case, `mlvd-us30`).

![Text file containing notes. This screenshot's not needed, but it's fun so why not.](/doc/img/29355e6249f8fa8da5d1471adf57887d4dba742141a53b41f29386895ecad319.png)

Now, repeat these steps for each of the VPN interfaces you want to use. Try to also generate listening ports for the other interfaces too, if possible.
