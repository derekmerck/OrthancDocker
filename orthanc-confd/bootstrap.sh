#! /bin/bash

echo "Creating config file"
confd -onetime -backend env

echo "Starting Orthanc"
exec Orthanc /etc/orthanc/orthanc.json