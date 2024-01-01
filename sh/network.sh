#!/bin/bash
set -x

ARGS="$@"

RESOURCES_DIR=.
RUN_MODE=train
TEST_DIR=mixed
RANDOM_TRACE=true

sleep 2

# start bw simulator in background
if [ "$RUN_MODE" == "train" ]; then
    python3 bw_sim_loop.py enp3s0 > bw_sim.log 2>&1 &
elif [ "$RUN_MODE" == "test" ]; then
    python3 bw_sim_test.py enp3s0 "$TEST_DIR" > bw_sim.log 2>&1 &
else
    echo "RUN_MODE not set, exit ..."
    exit
fi
