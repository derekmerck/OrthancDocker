#! python

"""
manifest-it.py
Merck, Summer 2018

Create manifest files for multi-arch images.

Uses simple `manifest.yaml` description format:

---
- image: "domain/master-image-name:tag"

  manifests:
    - image: "domain/amd64-image-name:tag"
      platform:
        architecture: amd64
        os: linux

    - image: "domain/armhf-image-name:tag"
      platform:
        architecture: arm
        variant: v7
        os: linux

    - image: "domain/arm64-image-name:tag"
      platform:
        architecture: arm64
        variant: v8
        os: linux
---

Note that armhf or arm32v7 is arch: arm, variant: v7, which makes sense, but is poorly documented.

Acceptable architecture definitions are listed here:
https://raw.githubusercontent.com/docker-library/official-images/a7ad3081aa5f51584653073424217e461b72670a/bashbrew/go/vendor/src/github.com/docker-library/go-dockerlibrary/architecture/oci-platform.go

All images must be present on the manifesting system or a partial master manifest will be created with missing references.

"""

import yaml, logging
from subprocess import call
from argparse import ArgumentParser

def docker_push(item):
    cmd = ['docker', 'push', item]
    logging.debug(cmd)
    call(cmd)

def docker_manifest_create(prime, aliases):
    cmd = ['docker', 'manifest', 'create', '--amend', prime, *aliases]
    # cmd = ['docker', 'manifest', 'create', prime, *aliases]
    logging.debug(cmd)
    call(cmd)

def docker_manifest_annotate(prime, item):
    cmd = ['docker', 'manifest', 'annotate',
          prime, item['image'],
          '--arch', item['platform']['architecture'],
          '--os', item['platform']['os'] ]
    if item['platform'].get('variant'):
        cmd = cmd + ['--variant', item['platform']["variant"]]
    logging.debug(cmd)
    call(cmd)

def docker_manifest_push(prime):
    cmd = ['docker', 'manifest', 'push', prime]
    logging.debug(cmd)
    call(cmd)

def parse_args():

    p = ArgumentParser("manifest-it.py creates Docker manifests for multi-architecture images")
    p.add_argument("manifest_file", help="File with manifest data and aliases")
    p.add_argument('-d', '--dryrun', action="store_true", help="Retag and manifest but don't push")

    opts = p.parse_args()
    return opts

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    opts = parse_args()

    with open(opts.manifest_file) as f:
        items = yaml.safe_load(f)

    for item in items:

        prime = item["image"]
        aliases = []

        for m in item["manifests"]:
            if not opts.dryrun:
                docker_push(m["image"])
            aliases.append(m["image"])

        docker_manifest_create(prime, aliases)

        for m in item["manifests"]:
            docker_manifest_annotate(prime, m)

        if not opts.dryrun:
            docker_manifest_push(prime)
