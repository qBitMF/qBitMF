#!/usr/bin/env python
# Take each interface and process out interface state.


from configparser import ConfigParser
import glob
import os
from subprocess import run, DEVNULL, STDOUT

# The name of the network namespace (netns).
WG_NETNS = "wg"


def process_config(hop_id, iface, config_file):
    """Process one single config file"""
    global WG_NETNS

    print(f"Configuring interface '{iface}'")

    # Read the input config file
    conf = ConfigParser()
    conf.read(config_file)


    # HACK: Assumes the first address is the IPv4 one
    addr = conf["Interface"]["Address"].split(",")[0]

    # Filter config file into interface-state
    # This removes lines that are incompatible with wg (as opposed to wg-quick)
    out_conf = ConfigParser()
    out_conf["Interface"] = {
        "PrivateKey": conf["Interface"]["PrivateKey"],
    }
    out_conf["Peer"] = {
        "PublicKey": conf["Peer"]["PublicKey"],
        "AllowedIPs": conf["Peer"]["AllowedIPs"],
        "Endpoint": conf["Peer"]["Endpoint"],
    }
    if conf["Peer"].get("PresharedKey", False):
        out_conf["Peer"]["PresharedKey"] = conf["Peer"]["PresharedKey"]

    with open(f"/interface-state/{iface}.conf", "w") as out_conf_file:
        out_conf.write(out_conf_file)

    # Create interface, move it into netns, then configure it
    run(["ip", "link", "add", "dev", iface, "type", "wireguard"])
    run(["wg", "setconf", iface, f"/interface-state/{iface}.conf"])
    run(["ip", "link", "set", iface, "netns", WG_NETNS])
    run(["ip", "-n", "wg", "addr", "add", addr, "dev", iface])
    run(["ip", "-n", "wg", "link", "set", "up", "dev", iface])
    run(["ip", "-n", "wg", "nexthop", "add", "id", str(hop_id), "dev", iface])


def main():
    # Create the wg netns
    run(f"ip netns delete {WG_NETNS}", shell=True, stdout=DEVNULL, stderr=STDOUT)
    run(f"ip netns add {WG_NETNS}", shell=True)

    # Enable localhost in netns (needed for socat to access the WebUI)
    run(f"ip -n {WG_NETNS} link set lo up", shell=True)

    # Process each WireGuard config file
    # Each interface gets configured as a routable "nexthop", which
    # gets assigned a "hop ID" starting at 1.
    wg_ids = []
    config_files = glob.glob("/interfaces/*.conf")
    for (hop_id, config_file) in enumerate(config_files):
        hop_id += 1
        config_fname = os.path.basename(config_file)
        iface = os.path.splitext(config_fname)[0]

        process_config(hop_id, iface, config_file)
        wg_ids.append(str(hop_id))

    # Create the nexthop group containing all interfaces
    wg_group = "/".join(wg_ids)
    run(
        [
            "ip",
            "-n",
            WG_NETNS,
            "nexthop",
            "add",
            "id",
            "9999",
            "group",
            wg_group,
            "type",
            "resilient",
            "buckets",
            "128",
        ]
    )

    # Make the default route use this nexthop group
    run(f"ip -n {WG_NETNS} route add default nhid 9999", shell=True)


if __name__ == "__main__":
    main()
