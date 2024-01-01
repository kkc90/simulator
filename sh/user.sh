#!/bin/bash
set -x

ARGS="$@"

# VIDEO_SRC="${VIDEO_SRC:-FourPeople.mjpeg}"
VIDEO_SRC=FourPeople.y4m

RESOURCES_DIR=.
URL=https://141.223.124.48/dpnm

# # start selenium grid in background
# ./opt/bin/entry_point.sh &
sleep 2

# CNT=0
DURATION=21600s #1800s #21600s
# join meeting for DURATION, then exit and join new meeting
while true :
do
    # (( CNT++ ))
    echo "current meeting room is ${URL}" > ./meeting_room.txt
    timeout $DURATION google-chrome --disable-gpu --no-sandbox --ignore-certificate-errors --window-size=1920,1080 \
	--incognito \
        --use-fake-ui-for-media-stream --use-fake-device-for-media-stream \
        --disable-plugins --mute-audio --disable-infobars \
        --autoplay-policy=no-user-gesture-required \
        --use-file-for-fake-video-capture=$RESOURCES_DIR/$VIDEO_SRC \
        --remote-debugging-port=9222 ${URL}

done

#timeout $DURATION google-chrome --disable-gpu --no-sandbox --ignore-certificate-errors --window-size=1920,1080 \
#--remote-debugging-port=9222 ${URL}_${CNT}
#echo "current meeting room is ${URL}_${CNT}" > ./meeting_room.txt
#google-chrome --headless
#----use-file-for-fake-audio-capture=$RESOURCES_DIR/fakeAudioStream.wav \
