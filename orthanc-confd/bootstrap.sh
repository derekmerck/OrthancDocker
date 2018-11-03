#! /bin/bash

echo "Creating Orthanc config file"
confd -confdir /etc/confd/orthanc -onetime -backend env

if [ "${ORTHANC_PG_ENABLED:-false}" = "true" ]; then
    echo "Checking Postgres db connection"
    python /usr/local/bin/check_postgres.py \
      -H ${ORTHANC_PG_HOST:-localhost} \
      -p ${ORTHANC_PG_PORT:-5432} \
      -u ${ORTHANC_PG_USER:-orthanc} \
      -w ${ORTHANC_PG_PASSWORD:-'passw0rd!'} \
      -d ${ORTHANC_PG_DATABASE:-orthanc}
fi

if [ "${ORTHANC_ROUTE_ENABLED:-false}" = "true" ]; then
    echo "Setting up Orthanc routing script"
    mkdir -p /var/lib/orthanc/scripts
    confd -confdir /etc/confd/routing -onetime -backend env
fi

echo "Starting Orthanc"

if [ -z "$ORTHANC_VERBOSE" ]; then
    exec Orthanc /etc/orthanc/orthanc.json
else
    exec Orthanc /etc/orthanc/orthanc.json --verbose
fi

