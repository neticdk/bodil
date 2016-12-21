#!/bin/bash

set -e

syncit() {
  channel=$1
  version=${2:-current}

  wget --cut-dirs=1 -nH --quiet -A coreos_production_image*,coreos_production_pxe*,version.txt* -m http://${channel}.release.core-os.net/amd64-usr/${version}
}

cd $(dirname $0)

(
  cd bodil/static/images/coreos/stable
  syncit stable
)

(
  cd bodil/static/images/coreos/beta
  syncit beta
)

(
  cd bodil/static/images/coreos/alpha
  syncit alpha
)

