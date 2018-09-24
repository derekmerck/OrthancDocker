# X-Arch Orthanc for Docker

Derek Merck  
<derek_merck@brown.edu>  
Rhode Island Hospital and Brown University  
Providence, RI  

Build multi-architecture [Orthanc](https://www.orthanc-server.com) DICOM-node Docker images.


## Overview

Orthanc is developed and maintained by Sebastien Jodogne. Full documentation is available in the [Orthanc Book](http://book.orthanc-server.com/users/docker.html).

This image is based on the `resin/$ARCH-debian:stretch` image.  [Resin.io][] base images include the [QEMU][] cross-compiler to facilitate building images for low-power single-board computers using more powerful Intel-architecture desktops and servers.

[Resin.io]: http://resin.io
[QEMU]: https://www.qemu.org

This branch supports builds for `amd64`, `armhf`/`arm32v7`, and `aarch64`/`arm64v8` architectures.  Most low-power single board computers such as the Raspberry Pi and Beagleboard are `armhf`/`arm32v7` devices.  The NVIDIA Jetson is an `aarch64`/`arm64v8` device.


## Build

`docker-compose.yml` contains build recipes for all relevant architectures.  We cannot use `depends_on` for build dependencies in `docker-compose`, so the vanilla `orthanc` image must explicitly built before the `orthanc-plugins` image that is based on it.

```bash
$ docker-compose build orthanc-amd64 orthanc-plugins-amd64
```

To build all images:

1. Register the Docker QEMU cross-compilers
2. Call `docker-compose` to build the vanilla `orthanc` images
3. Call `docker-compose` to build the `orthanc-plugin` images
4. Put Docker into experimental mode for manifest creation, if it is not already
5. Finally, call `manifest-it.py` to manifest and push the image sets (you will need to edit the compose and manifest files to point at your own Docker domain).

```bash
$ docker run --rm --privileged multiarch/qemu-user-static:register --reset
$ docker-compose build orthanc-amd64 orthanc-arm32v7 orthanc-arm64v8
$ docker-compose bulid orthanc-plugins-amd64 orthanc-plugins-arm32v7 orthanc-plugins-arm64v8
$ mkdir -p $HOME/.docker && echo '{"experimental":"enabled"}' > "$HOME/.docker/config.json"
$ python3 manifest-it.py xarch-orthanc.manifest.yml
```

An automation pipeline for image generation and tagging is demonstrated in the `.travis.yml` script.


## Pull

Images are _theoretically_ manifested per modern Docker.io guidelines so that an appropriately architected image be will automatically selected for a given tag depending on the pulling architecture.

```bash
$ docker run derekmerck/orthanc
$ docker run derekmerck/orthanc-plugins
```

Specifically architected images can be directly pulled using the format `derekmerck/orthanc{-plugins}{-arch}{:tag}`, where `arch` is one of `amd64`, `arm32v7`, or `arm64v8`.  Such explicit architecture specification is necessary on Resin hosts because their indirect build service shadows the production architecture.


## Run Orthanc on ARM

[Packet.net][] rents bare-metal 96-core `aarch64` [Cavium ThunderX] servers for $0.50/hour.  Packet's affiliated [Works On Arm][] program provided build-time for some of this development.

[Cavium ThunderX]: https://www.cavium.com/product-thunderx-arm-processors.html
[Packet.net]: https://packet.net
[Works On Arm]: https://www.worksonarm.com


## Changes

- Rebased from `_/ubuntu:14` to `resin/$ARCH-debian:stretch`
- Refactored into two-stage buiid with `orthanc-plugins` image based on `orthanc` image
- Specified `libssl1.0-dev` in `orthanc` image
- Added [GDCM][] CLI tools to `orthanc` image
- Refactored command to leave entrypoint available
- `orthanc-postgresql` code-base updated to `orthanc-databases` in `orthanc-plugins` image

[GDCM]: http://gdcm.sourceforge.net/wiki/index.php/Main_Page


## License

Standard Orthanc [GNU Affero General Public License](http://www.gnu.org/licenses/) applies.
