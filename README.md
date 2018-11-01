# X-Arch Orthanc for Docker

Derek Merck  
<derek_merck@brown.edu>  
Rhode Island Hospital and Brown University  
Providence, RI  

Build multi-architecture [Orthanc](https://www.orthanc-server.com) DICOM-node Docker images.

source: <https://github.com/derekmerck/docker-orthanc-xarch>


## Overview

Orthanc is developed and maintained by Sébastien Jodogne. Full documentation is available in the [Orthanc Book](http://book.orthanc-server.com/users/docker.html).  

This repo is a fork of Jodogne's [OrthancDocker](https://github.com/jodogne/OrthancDocker) project.  The `xarch` branch creates cross-architecture Docker images for the most recent default/mainline release version of Orthanc.  These images are manifested per modern Docker.io guidelines so that an appropriately architected image can be will automatically selected for a given tag depending on the pulling architecture.

This repo also creates a "self-configuring" orthanc image, `orthanc-confd`, motivated by the [OsimisDocker](https://osimis.atlassian.net/wiki/spaces/OKB/pages/26738689/How+to+use+osimis+orthanc+Docker+images) environment-variable-based configurator.  

- Based on the cross-architecture `orthanc-plugins` image
- Uses [confd][] to generate an appropriate `orthanc.json` configuration file from environment variables at startup
- Creates a postgres database for itself if needed
- Provides simple route forwarding to other Orthanc peers and DICOM modalities
- Includes a modern Docker container "healthcheck" attribute that regularly checks connectivity on 8042

Futher movitivated by the OsirisDocker project, this repo also creates an "osimis-webviewer" orthanc image, `orthanc-wbv`.
 
- Based on `orthanc-confd`
- Includes the very useful webviewer plugin from the Osimis Orthanc project
- _ONLY_ built for `amd64` architectures, because the binary is copied directly from the Osimis webviewer image

[confd]: https://github.com/kelseyhightower/confd


## Use It

Images can be pulled from:

```bash
$ docker run derekmerck/orthanc          # (latest-amd64, latest-arm32v7, latest-arm64v8)
$ docker run derekmerck/orthanc-plugins  # (latest-amd64, latest-arm32v7, latest-arm64v8)
$ docker run derekmerck/orthanc-confd    # (latest-amd64, latest-arm64v8)
$ docker run derekmerck/orthanc-wbv      # (latest-amd64)
```

Images for specific architectures images can be directly pulled from the same namespace using the format `derekmerck/orthanc:${TAG}-${ARCH}`, where `$ARCH` is one of `amd64`, `arm32v7`, or `arm64v8`.  Explicit architecture specification is sometimes helpful when an indirect build service shadows the production architecture.


## Build It

These images are based on the cross-platform `resin/${ARCH}-debian:stretch` image.  [Resin.io][] base images include the [QEMU][] cross-compiler to facilitate building Docker images for low-power single-board computers while using more powerful Intel-architecture compute servers.

[Resin.io]: http://resin.io
[QEMU]: https://www.qemu.org

This supports builds for `amd64`, `armhf`/`arm32v7`, and `aarch64`/`arm64v8` architectures.  Most low-power single board computers such as the [Raspberry Pi][] and [Beagleboard][] are `armhf`/`arm32v7` devices.  The [Pine64][] and [NVIDIA Jetson][] are `aarch64`/`arm64v8` devices.  Desktop computers/vms, [UP boards][], and the [Intel NUC][] are `amd64` devices.  

[UP boards]: http://www.up-board.org/upcore/
[Intel NUC]: https://www.intel.com/content/www/us/en/products/boards-kits/nuc.html
[Raspberry Pi]: https://www.raspberrypi.org
[Beagleboard]: http://beagleboard.org
[Pine64]: https://www.pine64.org
[NVIDIA Jetson]: https://developer.nvidia.com/embedded/buy/jetson-tx2

`docker-compose.yml` contains build recipes for each architecture for both a vanilla `orthanc` image and an `orthanc-plugins` image.  `orthanc-plugins` is based on `orthanc`, but since we cannot define build dependencies in a compose file (strangely, `depends_on` only works with `run` or `up`), the vanilla `orthanc` image must be explicitly built before the `orthanc-plugins` image.

To build all images:

1. Register the Docker QEMU cross-compilers
2. Call `docker-compose` to build the vanilla `orthanc` images
3. Call `docker-compose` to build the `orthanc-plugin` images
4. Call `docker-compose` to build the `orthanc-confd` images
5. Call `docker-compose` to build the `orthanc-wbv-amd64` image
6. Get [docker-manifest][] from Github
7. Put Docker into "experimental mode" for manifest creation
8. Call `docker-manifest.py` with an appropriate domain to manifest and push the images

[docker-manifest]: https://github.com/derekmerck/docker-manifest

```bash
$ docker run --rm --privileged multiarch/qemu-user-static:register --reset
$ docker-compose build orthanc-amd64 orthanc-arm32v7 orthanc-arm64v8
$ docker-compose bulid orthanc-plugins-amd64 orthanc-plugins-arm32v7 orthanc-plugins-arm64v8
$ docker-compose bulid orthanc-confd-amd64 orthanc-confd-arm64v8
$ docker-compose bulid orthanc-wbv-amd64
$ pip install git+https://github.com/derekmerck/docker-manifest
$ mkdir -p $HOME/.docker && echo '{"experimental":"enabled"}' > "$HOME/.docker/config.json"
$ python3 -m docker-manifest -d $DOCKER_USERNAME orthanc
$ python3 -m docker-manifest -d $DOCKER_USERNAME orthanc-plugins
$ python3 -m docker-manifest -d $DOCKER_USERNAME orthanc-confd
$ python3 -m docker-manifest -d $DOCKER_USERNAME orthanc-wbv
```

A [Travis][] automation pipeline for git-push-triggered image regeneration and tagging is demonstrated in the `.travis.yml` script.  However, these cross-compiling jobs exceed Travis' 50-minute timeout window, so builds are currently done by hand using cloud infrastructure.

[Travis]: http://travis-ci.org


## Run Orthanc on ARM

If you need access to an ARM device for development, [Packet.net][] rents bare-metal 96-core 128GB `aarch64` [Cavium ThunderX] servers for $0.50/hour.  Packet's affiliated [Works On Arm][] program provided compute time for developing and testing these cross-platform images.

[Cavium ThunderX]: https://www.cavium.com/product-thunderx-arm-processors.html
[Packet.net]: https://packet.net
[Works On Arm]: https://www.worksonarm.com

Setup your ARM device with Docker and pull the image tag. You can confirm that the appropriate image has been pulled by starting a container with the command `arch`.  

```bash
$ docker pull derekmerck/orthanc
Using default tag: latest
latest: Pulling from derekmerck/orthanc
Digest: sha256:1975e3a92cf9099284fc3bb2d05d3cf081d49babfd765f96f745cf8a23668ff6
Status: Downloaded newer image for derekmerck/orthanc:latest
$ docker run derekmerck/orthanc arch
aarch64
```

You can also confirm the image architecture without running a container by inspecting the value of `.Config.Labels.architecture`.  (This is a creator-defined label that is _different_ than the normal `.Architecture` key -- which appears to _always_ report as `amd64`.)

```bash
$ docker inspect derekmerck/orthanc --format "{{ .Config.Labels.architecture }}"
arm64v8
```


## Why Bother?

On-board embedded AI is the future of medical imaging!  Orthanc provides a vital, robust bridge between modality-generated DICOM and modern data indexing and analysis algorithms.

This image is also drop-in compatible with the [derekmerck.orthanc-docker](https://github.com/derekmerck/ansible-orthanc-docker) [Ansible][] role, facilitating quick configuration of complex DICOM infrastructures on ARM data center equipment.

[Ansible]: https://www.ansible.com


## Confd/wbv Options

```bash
$ docker run -e ORTHANC_PASSWORD=my_password -e ORTHANC_AET=MY_ORTHANC derekmerck/orthanc-confd 
```

Following is a list of common options and their defaults that can be configured through environment variables.

```yaml
ORTHANC_VERBOSE=false

ORTHANC_NAME=Orthanc
ORTHANC_AET=ORTHANC
ORTHANC_MAX_SIZE=0    # Max storage size in MB
ORTHANC_MAX_PATIENTS=0
ORTHANC_STORE_DICOM=true

ORTHANC_REMOTE_ENABLED=true
ORTHANC_AUTH_ENABLED=true
ORTHANC_USER=orthanc
ORTHANC_PASSWORD=passw0rd!

ORTHANC_USER_[0-3]=""  # Additional users in "user,password" format
ORTHANC_MOD_[0-3]=""   # Known DICOM modalities in "name,aet,host,port" format
ORTHANC_PEER_[0-3]=""  # Known Orthanc peers in "name,url,user,password" format
```

_NOTE: avoid using `,` or escaped characters like quotes in passwords as they interfere with the simple string splitting used for parsing here._

The postgres plugin can be similarly configured using `ORTHANC_PG` variables

```bash
ORTHANC_PG_ENABLED=false
ORTHANC_PG_STORE_DICOM=false
ORTHANC_PG_HOST=localhost
ORTHANC_PG_PORT=5432
ORTHANC_PG_USER=postgres
ORTHANC_PG_PASSWORD=passw0rd!
ORTHANC_PG_DATABASE=orthanc
```

Simple routing to known peers or modalities can be configured using `ORTHANC_ROUTE` variables.

```bash
ORTHANC_ROUTE_ENABLED=false
ORTHANC_ROUTE_AND_STORE=false  # Do not delete image after forwarding 
ORTHANC_ROUTE_TO_PEERS=name1,name1,name2,...  # Names from ORTHANC_PEER_N descriptions
ORTHANC_ROUTE_TO_MODS=name0,name1,name2,...   # Names from ORTHANC_MOD_N descriptions
```

The webviewer plugin for the `orthanc-wbv` image is configured using using `ORTHANC_WBV` variables.

```bash
ORTHANC_WBV_ENABLED=false
ORTHANC_WBV_DOWNLOAD_ENABLED=false
ORTHANC_WBV_STORE_ANNOTATIONS=false
```

There is a good summary of this "confd onetime" configuration method here <http://www.mricho.com/confd-and-docker-separating-config-and-code-for-containers/>


## Changes

- Major: Rebased images from `_/ubuntu:14` to `resin/$ARCH-debian:stretch`
- Major: Refactored into multi-stage build
- Major: `orthanc-postgresql` code-base updated to use `orthanc-databases` repo
- Major: Wrapped Orthanc invocation with `confd`
- Major: Added `psychopg2` script to check for Postgres database and create if necessary
- Major: Added simple `lua`-scripted auto-forwarding
- Major: Added Osimis webviewer (for `amd64` _ONLY_)

- Minor: Set locale using a [Debian-friendly method](https://unix.stackexchange.com/questions/246846/cant-generate-en-us-utf-8-locale)
- Minor: Specified `libssl1.0-dev` in `orthanc` image
- Minor: Added [GDCM][] CLI tools to `orthanc` image
- Minor: Refactored `command` to leave `entrypoint` available for init process
- Minor: Redirected `deb.debian.org` sources to `cdn-fastly.deb.debian.org` to mitigate `apt` source errors

[GDCM]: http://gdcm.sourceforge.net/wiki/index.php/Main_Page


## Notes

Grab the latest `orthanc.json` file to update the template:

```bash
$ docker run -d --name orthanc derekmerck/orthanc
$ docker cp orthanc:/etc/orthanc/orthanc.json .
```

## License

Standard Orthanc [GNU Affero General Public License](http://www.gnu.org/licenses/) applies.
