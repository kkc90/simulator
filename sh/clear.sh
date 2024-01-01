#!/bin/sh
DEVICE=$(route | grep '^default' | grep -o '[^ ]*$')
tc qdisc del dev $DEVICE ingress
tc qdisc del dev ifb0 root
kill -9 `ps -ef | grep 'bw_sim' | awk '{print $2}'`
