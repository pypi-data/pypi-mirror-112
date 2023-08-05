# Snappi-Trex
Snappi-Trex is a Snappi plugin that allows executing scripts written using 
[Snappi](https://github.com/open-traffic-generator/snappi) with Cisco's [T-Rex Traffic Generator](https://trex-tgn.cisco.com)

## Design
Snappi-Trex converts Snappi Open Traffic Generator API configuration into the equivalent T-Rex STL Client configuration. This allows users to use the T-Rex Traffic Generator and its useful features without having to write complex T-Rex scripts. 

![diagram](docs/res/snappi-trex-design.svg)

The above diagram outlines the overall process of how the Snappi Open Traffic Generator API is able to interface with T-Rex and generatee traffic over its network interfaces. Snappi_trex is essential to convert Snappi scripts into the equivalent T-Rex STL Client instructions.

<br>

Snappi_trex usage follows the standard usage of Snappi with a few modifications outlined in the [Usage](https://github.com/open-traffic-generator/snappi-trex/docs/usage.md) document.


# Quickstart

## Installing and Running T-Rex
T-Rex must be installed and configured in order to use snappi_trex. For a quick tutorial on T-Rex installation, running, and basic usage, check out this [T-Rex Tutorial](https://github.com/open-traffic-generator/snappi-trex/docs/t-rex-tutorial.md)

## Installing Snappi-Trex
First, make sure that Snappi is installed.
```sh
pip3 install snappi
```
Now, install the snappi_trex extension.
```sh
pip3 install snappi_trex
```

## Start Scripting
```
import snappi
import sys, os

# Replace vX.XX with the installed version of T-Rex. 
# Change '/opt/trex' if you installed T-Rex in another location
trex_path = '/opt/trex/vX.XX/automation/trex_control_plane/interactive'
sys.path.insert(0, os.path.abspath(trex_path))


def hello_snappi_trex():
    """
    This script does following:
    - Send 1000 packets back and forth between the two ports at a rate of
      1000 packets per second.
    """
    # create a new API instance where host points to trex server
    api = snappi.api(host='https://localhost', ext='trex')
    
    # and an empty traffic configuration to be pushed to controller later on
    cfg = api.config()

    # add two ports where location points to traffic-engine (aka ports)
    p1, p2 = (
        cfg.ports
        .port(name='p1', location='localhost:5555')
        .port(name='p2', location='localhost:5556')
    )

    # add layer 1 property to configure same speed on both ports
    ly = cfg.layer1.layer1(name='ly')[-1]
    ly.port_names = [p1.name, p2.name]
    ly.speed = ly.SPEED_1_GBPS

    # enable packet capture on both ports
    cp = cfg.captures.capture(name='cp')[-1]
    cp.port_names = [p1.name, p2.name]

    # add two traffic flows
    f1, f2 = cfg.flows.flow(name='flow p1->p2').flow(name='flow p2->p1')
    # and assign source and destination ports for each
    f1.tx_rx.port.tx_name, f1.tx_rx.port.rx_name = p1.name, p2.name
    f2.tx_rx.port.tx_name, f2.tx_rx.port.rx_name = p2.name, p1.name

    # configure packet size, rate and duration for both flows
    f1.size.fixed = 128
    f2.size.fixed = 256
    for f in cfg.flows:
        # send 1000 packets and stop
        f.duration.fixed_packets.packets = 1000
        # send 1000 packets per second
        f.rate.pps = 1000

    # configure packet with Ethernet, IPv4 and UDP headers for both flows
    eth1, ip1, udp1 = f1.packet.ethernet().ipv4().udp()
    eth2, ip2, udp2 = f2.packet.ethernet().ipv4().udp()

    # set source and destination MAC addresses
    eth2.src.value, eth2.dst.value = '00:AA:00:00:00:AA', '00:AA:00:00:04:00'
    eth1.src.increment.start = '10:AA:00:00:04:00'
    eth1.src.increment.step = 2
    eth1.src.increment.count = 1000
    eth2.src.values = ['33:33:33:11:11:11', '22:22:22:22:22:22']
    eth1.dst.decrement.start = '10:AA:00:00:04:00'
    eth1.dst.decrement.step = 4
    eth1.dst.decrement.count = 1000

    # set source and destination IPv4 addresses
    ip2.src.value, ip2.dst.value = '10.0.0.2', '10.0.0.1'

    ip1.src.increment.start = '11.0.0.1'
    ip1.src.increment.step = 2
    ip1.src.increment.count = 1000
    ip1.dst.decrement.start = '12.0.0.0'
    ip1.dst.decrement.step = 4
    ip1.dst.decrement.count = 1000

    # set incrementing port numbers as source UDP ports
    udp1.src_port.value = 5000
    udp2.src_port.decrement.start = 5000
    udp2.src_port.decrement.step = 1
    udp2.src_port.decrement.count = 1000

    # assign list of port numbers as destination UDP ports
    udp1.dst_port.values = [8000, 8004, 8049, 9001]
    udp2.dst_port.decrement.start = 5000
    udp2.dst_port.decrement.step = 1
    udp2.dst_port.decrement.count = 1000


    print('Pushing traffic configuration ...')
    api.set_config(cfg)

    print('Starting transmit on all configured flows ...')
    ts = api.transmit_state()
    ts.state = ts.START
    api.set_transmit_state(ts)


if __name__ == '__main__':
    hello_snappi_trex()

```