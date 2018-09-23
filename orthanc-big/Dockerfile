# X-Arch Orthanc Vanilla
# Derek Merck, Fall 2018

ARG ORX_ARCH="amd64"
#ARG ORX_ARCH="arm32v7"
#ARG RESIN_ARCH="arm64v8"

FROM derekmerck/orthanc-base-$ORX_ARCH

# MAINTAINER Sebastien Jodogne <s.jodogne@gmail.com>
MAINTAINER Derek Merck <derek_merck@brown.edu>
LABEL Description="X-Arch Orthanc, free DICOM server" Vendor="The Orthanc project"

ADD ./build-orthanc.sh /root/build-orthanc.sh
RUN bash /root/build-orthanc.sh "default"

VOLUME [ "/var/lib/orthanc/db" ]
EXPOSE 4242
EXPOSE 8042

ENTRYPOINT [ "Orthanc" ]
CMD [ "/etc/orthanc/" ]

ENV TZ=America/New_York
# Disable resin.io's systemd init system
ENV INITSYSTEM off
