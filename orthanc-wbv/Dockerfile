# X-Arch Orthanc Plugins w Confd Image
# Derek Merck, Fall 2018

# amd64 ONLY
ARG DOCKER_ARCH="amd64"

FROM osimis/orthanc-webviewer-plugin:1.1.1 as wvb

FROM orthanc-confd-$DOCKER_ARCH
LABEL description="X-Arch Orthanc, free cross-platform DICOM server (plugins, confd, wvb)"

COPY --from=wvb /usr/share/orthanc/plugins/libOsimisWebViewer.so /usr/share/orthanc/plugins/

COPY *.tmpl /etc/confd/orthanc/templates/
COPY *.toml /etc/confd/orthanc/conf.d/
