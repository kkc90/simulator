FROM jrottenberg/ffmpeg:4.1-ubuntu AS builder

ENV RESOURCES_DIR=/resources

RUN apt-get update && \
	apt-get install -y wget

RUN mkdir -p $RESOURCES_DIR

RUN wget -q https://media.xiph.org/video/derf/webm/FourPeople_1280x720_60.webm -O /FourPeople_1280x720_60.webm && \
	ffmpeg -i /FourPeople_1280x720_60.webm -filter:v fps=fps=30 -q:v 5 $RESOURCES_DIR/FourPeople.mjpeg

RUN wget -q https://media.xiph.org/video/derf/webm/Johnny_1280x720_60.webm -O /Johnny_1280x720_60.webm && \
	ffmpeg -i /Johnny_1280x720_60.webm -filter:v fps=fps=30 -q:v 5 $RESOURCES_DIR/Johnny.mjpeg

RUN wget -q https://media.xiph.org/video/derf/webm/KristenAndSara_1280x720_60.webm -O /KristenAndSara_1280x720_60.webm && \
	ffmpeg -i /KristenAndSara_1280x720_60.webm -filter:v fps=fps=30 -q:v 5 $RESOURCES_DIR/KristenAndSara.mjpeg

RUN wget -q https://github.com/jitsi/jitsi-meet-torture/raw/master/resources/fakeAudioStream.wav -O $RESOURCES_DIR/fakeAudioStream.wav


# Main container
FROM selenium/standalone-chrome:4.5

USER root

ENV START_XVFB=false
# 100 is more than enough for a single server
ENV NODE_MAX_SESSION=100
ENV NODE_MAX_INSTANCES=100
ENV RESOURCES_DIR=/resources

RUN mkdir -p /usr/share/man/man1 && \
	apt-get update && \
	apt-get install -y vim git bc && \
	apt-get clean

RUN echo "set encoding=utf-8" >> /etc/vim/vimrc

RUN mkdir -p $RESOURCES_DIR
COPY --from=builder $RESOURCES_DIR/* $RESOURCES_DIR/

RUN apt-get update && \
	apt-get install -y iproute2 python3 coreutils && \
	apt-get clean

RUN curl -sSL https://raw.githubusercontent.com/thombashi/tcconfig/master/scripts/installer.sh | sudo bash

COPY rootfs/ /
RUN chmod 755 /start.sh

ENTRYPOINT ["/start.sh"]


