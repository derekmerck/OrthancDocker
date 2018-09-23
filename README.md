# Orthanc for Docker
[Docker Hub](https://www.docker.com/) repository to build [Orthanc](http://www.orthanc-server.com/) and its official plugins. Orthanc is a lightweight, RESTful Vendor Neutral Archive for medical imaging.

Full documentation is available in the [Orthanc Book](http://book.orthanc-server.com/users/docker.html).

Orthanc is developed and maintained by Sebastien Jodogne.


# X-Arch Orthanc for Docker

Derek Merck  
<derek_merck@brown.edu>  
Rhode Island Hospital and Brown University  
Providence, RI  

Build multi-arch [Orthanc](https://www.orthanc-server.com) DICOM-node Docker images.

## Overview

This image is based on the `resin/$ARCH-debian:stretch` image.  [Resin.io][] base images include the [QEMU][] cross-compiler to facilitate building images for low-power single-board computers using more powerful Intel-architecture desktops and servers.

[Resin.io]: http://resin.io
[QEMU]: https://www.qemu.org

This branch supports builds for `amd64`, `armhf`/`arm32v7`, and `aarch64`/`arm64v8` architectures.  

Most low-power single board computers such as the Raspberry Pi and Beagleboard are `armhf`/`arm32v7` devices.

`docker-compose.yml` contains build descriptions for all relevant architectures.

## Build

We cannot use `depends_on` for build dependencies in `docker-compose`, so the vanilla `orthanc` image must explicitly built before the `orthanc-plugins` image.

```bash
$ docker-compose build orthanc-amd64 orthanc-plugins-amd64
```

To bulid the entire suite: first register the cross-compilers, then call `docker-compose twice`, first with  the vanilla `orthanc` images, and then with the `orthanc-plugin` images.  Finally, call `manifest-it.py` to manifest and push the final images (you will need to update the compose and manifest files to point at your own Docker domain).

```bash
$ docker run --rm --privileged multiarch/qemu-user-static:register --reset
$ docker-compose build orthanc-amd64 orthanc-arm32v7 orthanc-arm64v8
$ docker-compose bulid orthanc-plugins-amd64 orthanc-plugins-arm32v7 orthanc-plugins-arm64v8
$ python3 manifest-it.py xarch-orthanc.manifest.yml
```

An automation pipeline for image generation is provided in the `.travis.yml` script.

## Pull

Images are _theoretically_ manifested per Docker.io guidelines so that an appropriately architected image be will automatically selected for a given tag depending on the pulling architecture.

```bash
$ docker run derekmerck/orthanc
$ docker run derekmerck/orthanc-plugins
```

Specifically architected images can be directly pulled using the format `derekmerck/orthanc{-plugins}{-arch}{:tag}`, where `arch` is one of `amd64`, `arm32v7`, or `arm64v8`.  Such explicit architecture specification is necessary, for example, on Resin hosts because of their indirect build service.

## Run Orthanc on ARM

[Packet.net][] rents bare-metal 96-core `aarch64` [Cavium ThunderX] servers for $0.50/hour.  Packet's affiliated [Works On Arm][] program provided build-time for some of this development.

[Cavium ThunderX]: https://www.cavium.com/product-thunderx-arm-processors.html
[Packet.net]: https://packet.net
[WorksOnArm]: https://www.worksonarm.com


## Changes

- Rebase images on `resin/$ARCH-debian:stretch`
- Specify `libssl1.0-dev`
- Add [GDCM][] CLI tools
- `orthanc-postgresql` code-base updated to `orthanc-databases`

[GDCM]: http://gdcm.sourceforge.net/wiki/index.php/Main_Page


## License

Standard Orthanc usage license applies.
