# X-Arch Orthanc Vanilla Image
# Derek Merck, Fall 2018

ARG RESIN_ARCH="amd64"
#ARG RESIN_ARCH="armv7hf"
#ARG RESIN_ARCH="aarch64"

FROM resin/${RESIN_ARCH}-debian:stretch

ARG DOCKER_ARCH="amd64"
# ARG DOCKER_ARCH="arm32v7"
# ARG DOCKER_ARCH="arm64v8"

LABEL maintainer="Derek Merck"
LABEL email="derek_merck@brown.edu"
LABEL maintainer2="Sebastien Jodogne"
LABEL description="X-Arch Orthanc, free cross-platform DICOM server"
LABEL vendor="The Orthanc project"
LABEL architecture="$DOCKER_ARCH"
LABEL os="linux"

RUN apt -y clean && apt -y update && apt -y upgrade
RUN DEBIAN_FRONTEND=noninteractive apt -y install --no-install-recommends \
    wget \
    nano \
    build-essential \
    unzip \
    cmake \
    git \
    mercurial \
    uuid-dev \
    libcurl4-openssl-dev \
    liblua5.1-0-dev \
    libgtest-dev \
    libpng-dev \
    libsqlite3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libdcmtk2-dev \
    libboost-all-dev \
    libwrap0-dev \
    libcharls-dev \
    libjsoncpp-dev \
    libpugixml-dev \
    libssl1.0-dev \
    libgdcm-tools \
    locales \
  && apt -y clean \
  && rm -rf /var/lib/apt/lists/*

RUN sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen && locale-gen

ADD ./build-dcmtk.sh /root/build-dcmtk.sh
RUN bash /root/build-dcmtk.sh

ADD ./build-orthanc.sh /root/build-orthanc.sh
RUN bash /root/build-orthanc.sh "default"

VOLUME [ "/var/lib/orthanc/db" ]
EXPOSE 4242
EXPOSE 8042

# Leave entrypoint alone for resin-init
CMD [ "Orthanc", "/etc/orthanc/" ]

ENV TZ=America/New_York
# Disable resin.io's systemd init system
ENV INITSYSTEM off
