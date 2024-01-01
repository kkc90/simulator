#!/bin/bash
set -x

ARGS="$@"

# VIDEO_SRC="${VIDEO_SRC:-FourPeople.mjpeg}"
# DEFAULT_DELAY="${DEFAULT_DELAY:-50}"

# start selenium grid in background
./opt/bin/entry_point.sh &
sleep 2

# start bw simulator in background
if [ "$RUN_MODE" == "train" ]; then
    python3 bw_sim_loop.py eth0 > bw_sim.log 2>&1 &
elif [ "$RUN_MODE" == "train_2" ]; then
    python3 bw_sim_loop_2.py eth0 > bw_sim.log 2>&1 &
elif [ "$RUN_MODE" == "test" ]; then
    # python3 bw_sim_test.py eth0 "$TEST_DIR" "$DEFAULT_DELAY" > bw_sim.log 2>&1 &
    python3 bw_sim_test.py eth0 "$TEST_DIR" > bw_sim.log 2>&1 &
elif [ "$RUN_MODE" == "stable_2" ]; then
    python3 bw_sim_test_2.py eth0 > bw_sim.log 2>&1 &
else
    echo "RUN_MODE not set, exit ..."
    exit
fi

CNT=0
DURATION=172800s #DURATION=1800s
# join meeting for DURATION, then exit and join new meeting
while true :
do
    (( CNT++ ))
    echo "current meeting room is ${URL}, count is ${CNT}" > ./meeting_room.txt
    timeout $DURATION google-chrome --headless --disable-gpu --no-sandbox --ignore-certificate-errors --window-size=1920,1080 \
        --use-fake-ui-for-media-stream --use-fake-device-for-media-stream \
        --disable-plugins --mute-audio --disable-infobars \
        --autoplay-policy=no-user-gesture-required \
        --use-file-for-fake-video-capture=$RESOURCES_DIR/$VIDEO_SRC \
        ----use-file-for-fake-audio-capture=$RESOURCES_DIR/fakeAudioStream.wav \
        --remote-debugging-port=9222 ${URL}

done
