# Getting wireguard configuration files


First login to your Windscribe Pro Account. Generating configs is not available for free or Build-a-Plan Accounts.

Now head to https://windscribe.com/getconfig/wireguard and select your desired Location and Port. Leave the third Option at "New Key Pair" if this is the first config you are generating.

![example of how to generate windscribe config](/doc/img/windscribe-guide-1.png)
  
<br />

## Generating more configuration files

Windscribe accounts are limited to 5 key-pairs. I recommend using the same key-pair for all your qBitMF connections.

To generate more configs, again enter your Location and Port, but select the existing key-pair you generated the first time. In case you want to use the same key-pair with the same Server multiple times, I recommend using different Ports, as using the same Port twice can lead to weird behavior.

![example of how to generate windscribe config](/doc/img/windscribe-guide-2.png)

Now head back to [the README](../../README.md#configuring-docker-and-docker-compose) to continue setup.
