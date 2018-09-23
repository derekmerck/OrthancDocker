# X-Arch Orthanc Base Image
# Derek Merck, Fall 2018

ARG RESIN_ARCH="amd64"
#ARG RESIN_ARCH="armv7hf"
#ARG RESIN_ARCH="aarch64"

FROM resin/${RESIN_ARCH}-debian:stretch
# MAINTAINER Sebastien Jodogne <s.jodogne@gmail.com>
MAINTAINER Derek Merck <derek_merck@brown.edu>

LABEL Description="Base environment to build X-Arch Orthanc" Vendor="The Orthanc project"

RUN apt-get -y clean && apt-get -y update
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install \
    wget nano build-essential unzip cmake mercurial uuid-dev libcurl4-openssl-dev liblua5.1-0-dev libgtest-dev libpng-dev libsqlite3-dev libjpeg-dev zlib1g-dev libdcmtk2-dev libboost-all-dev libwrap0-dev libcharls-dev libjsoncpp-dev libpugixml-dev libssl1.0-dev libgdcm-tools locales \
  && apt-get clean && rm -rf /var/lib/apt/lists/*
