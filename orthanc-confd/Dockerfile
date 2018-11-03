# X-Arch Orthanc Plugins w Confd Image
# Derek Merck, Fall 2018

ARG DOCKER_ARCH="amd64"

FROM orthanc-plugins-$DOCKER_ARCH
LABEL description="X-Arch Orthanc, free cross-platform DICOM server (plugins, confd)"

# Sources are listed as cdn-fastly addresses in most recent Stretch
RUN sed -i "s\deb.debian.org\cdn-fastly.deb.debian.org\g" /etc/apt/sources.list

RUN DEBIAN_FRONTEND=noninteractive apt -y clean && apt -y update
RUN DEBIAN_FRONTEND=noninteractive apt -y install --no-install-recommends \
    python-psycopg2 \
  && apt -y clean \
  && rm -rf /var/lib/apt/lists/*

ARG CONFD_PKG="https://github.com/kelseyhightower/confd/releases/download/v0.16.0/confd-0.16.0-linux-amd64"

RUN curl -L $CONFD_PKG -o /usr/local/bin/confd && chmod +x /usr/local/bin/confd

RUN mkdir -p /etc/confd/{conf.d,templates}
COPY orthanc.json.tmpl /etc/confd/orthanc/templates/
COPY orthanc.json.toml /etc/confd/orthanc/conf.d/
COPY routing.lua.tmpl /etc/confd/routing/templates/
COPY routing.lua.toml /etc/confd/routing/conf.d/

COPY check_postgres.py /usr/local/bin/check_postgres.py
RUN chmod +x /usr/local/bin/check_postgres.py
COPY bootstrap.sh /usr/local/bin/bootstrap.sh
RUN chmod +x /usr/local/bin/bootstrap.sh

CMD /usr/local/bin/bootstrap.sh

HEALTHCHECK --interval=5s --timeout=2s --start-period=10s CMD bash -c "printf 'GET / HTTP/1.1\n\n' > /dev/tcp/127.0.0.1/8042"
