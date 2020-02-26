#!/usr/bin/env bash

################################################################
# Author    Version     Date          Comments
# Xiaolei   v0.1       2017-10-30     Add nvidia and cuda libs
################################################################

# Helper functions
die() {
  echo $@
  exit 1
}

## pre-load nvidia and cuda libs via copy
#cp -a /opt/nvidia/* /usr/lib/x86_64-linux-gnu/
#cp -a /opt/tools/* /usr/bin/
#ldconfig
## DON'T mofify above commands

#mkdir /usr/share/fonts/
#cp /var/tf-k8s/msyh.ttf /usr/share/fonts/

jupyter notebook --allow-root "$@"
