#! python3

"""
docker-manifest.py
Merck, Fall 2018

Create manifest files for multi-arch images from docker-compose service definitions.

Platform Dependencies:  Docker
Pip Dependencies:  pyyaml

docker-compose.yml services name keys should be formatted "{service}-{arch}", and arch should be
included in a "DOCKER_ARCH" build arg.
---
services:
  my_service-amd64:
    build:
      args:
        DOCKER_ARCH: amd64
---

This will register as a service definition with basename "my_service" and architecture "amd64".
Architectures may be any one of amd64, arm32v7, or arm64v8.

Acceptable architecture definitions are listed here:
https://raw.githubusercontent.com/docker-library/official-images/a7ad3081aa5f51584653073424217e461b72670a/bashbrew/go/vendor/src/github.com/docker-library/go-dockerlibrary/architecture/oci-platform.go

A good reference for docker manifest files:
https://lobradov.github.io/Building-docker-multiarch-images/#building-a-multi-arch-manifest

All images should be present on the manifesting system or a partial master manifest will be created with missing references.

TODO: could have this just read the compose file and try to do all services if possible, or take a list of services from the command line
"""

import yaml, logging, os, shutil
from subprocess import call
from argparse import ArgumentParser


def docker_rename_image(old, new):
    cmd = ['docker', 'tag', old, new]
    logging.debug(cmd)
    call(cmd)


def docker_push_image(image):
    cmd = ['docker', 'push', image]
    logging.debug(cmd)
    if not opts.dryrun:
        call(cmd)


def docker_push_manifest(manifest):
    cmd = ['docker', 'manifest', 'push', manifest]
    logging.debug(cmd)
    if not opts.dryrun:
        call(cmd)

def docker_manifest_create(manifest, aliases):
    fp = os.path.expandvars( "$HOME/.docker/manifests/docker.io_{domain}_{service}-{tag}".format(
        domain=opts.domain,
        service=opts.service,
        tag=opts.tag
    ))
    if os.path.exists(fp):
        logging.debug("Removing existing manifests at {}".format(fp))
        shutil.rmtree(fp)
    cmd = ['docker', 'manifest', 'create', manifest, *aliases]
    logging.debug(cmd)
    call(cmd)


def docker_manifest_annotate(manifest, item):
    cmd = ['docker', 'manifest', 'annotate',
           manifest, item['image'],
           '--arch', item['arch'],
           '--os', item['os'] ]
    if item.get('variant'):
        cmd = cmd + ['--variant', item["variant"]]
    logging.debug(cmd)
    call(cmd)


def parse_args():

    p = ArgumentParser(description = "%(prog)s creates Docker manifests for multi-architecture images from docker-compose service definitions")
    p.add_argument("-f", "--file", default="docker-compose.yml",
                   help="docker-compose file with service definitions (default: %(default)s)")
    p.add_argument("-d", "--domain",
                   help="docker domain name")
    p.add_argument("-t", "--tag", default="latest",
                   help="docker image tag (default: %(default)s)")
    p.add_argument('--dryrun', action="store_true",
                   help="Retag images and create manifest, but do not push")
    p.add_argument("service", help="service base name")

    opts = p.parse_args()
    return opts


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    opts = parse_args()

    with open(opts.file) as f:
        data = yaml.safe_load(f)
        services = data.get('services')

    aliases = []
    annotations = {}

    for k, v in services.items():

        arch = v.get('build', {}).get('args', {}).get("DOCKER_ARCH", "amd64")
        logging.debug("Found {} for {}".format(arch, k))

        if k == "{}-{}".format(opts.service, arch):

            # Retag and include this one in the manifest
            current_name = v.get('image')
            new_name = "{domain}/{service}:{tag}-{arch}".format(
                domain=opts.domain,
                service=opts.service,
                tag=opts.tag,
                arch=arch)

            docker_rename_image( current_name, new_name )
            docker_push_image( new_name )

            aliases.append( new_name )

            def get_arch_str(arch):
                if arch == "amd64" or arch == "x86_64":
                    return "amd64", None
                elif arch == "arm32v7" or arch == "arm7hf":
                    return "arm", "v7"
                elif arch == "arm64v8" or arch == "aarch64":
                    return "arm64", "v8"
                else:
                    raise ValueError

            annotations[k] = {
                'image':   new_name,
                'arch':    get_arch_str(arch)[0],
                'variant': get_arch_str(arch)[1],
                'os':      'linux'
            }

    manifest = "{domain}/{service}:{tag}".format(
        domain=opts.domain,
        service=opts.service,
        tag=opts.tag
    )

    docker_manifest_create(manifest, aliases)

    for annotation in annotations.values():
        docker_manifest_annotate(manifest, annotation)

    if not opts.dryrun:
        docker_push_manifest(manifest)
