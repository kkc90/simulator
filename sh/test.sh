#!/bin/bash
DEVICE=$(route | grep '^default' | grep -o '[^ ]*$')
ip link add ifb0 type ifb
ip link set dev ifb0 up
# tc qdisc add dev $DEVICE ingress
# tc filter add dev $DEVICE  parent ffff: protocol ip u32 match u32 0 0 flowid 1:1 action mirred egress redirect dev ifb0
# tc qdisc add dev ifb0 root netem delay 50ms rate 1mbit

tc qdisc add dev enp3s0 handle ffff: ingress
tc filter add dev enp3s0  parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev ifb0
tc qdisc add dev ifb0 parent 2: classid 2:1 htb rate 1.5mbit