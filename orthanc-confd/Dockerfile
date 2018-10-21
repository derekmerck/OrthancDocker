# X-Arch Orthanc Plugins w Confd Image
# Derek Merck, Fall 2018

ARG DOCKER_ARCH="amd64"

FROM orthanc-plugins-$DOCKER_ARCH
LABEL description="X-Arch Orthanc, free cross-platform DICOM server (plugins, confd)"

ARG CONFD_PKG="https://github.com/kelseyhightower/confd/releases/download/v0.16.0/confd-0.16.0-linux-amd64"

RUN curl -L $CONFD_PKG -o /usr/local/bin/confd && chmod +x /usr/local/bin/confd

RUN mkdir -p /etc/confd/{conf.d,templates}
COPY orthanc.json.tmpl /etc/confd/templates/
COPY conf.toml /etc/confd/conf.d/

COPY bootstrap.sh /usr/bin/local/bootstrap.sh
RUN chmod +x /usr/bin/local/bootstrap.sh

CMD /usr/bin/local/bootstrap.sh

HEALTHCHECK --interval=5s --timeout=2s --start-period=10s CMD bash -c "printf 'GET / HTTP/1.1\n\n' > /dev/tcp/127.0.0.1/8042"
