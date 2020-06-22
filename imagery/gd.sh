#!/bin/bash

#run a shell script in a container

export GDAL_CONTAINER=osgeo/gdal:ubuntu-small-latest

COMPRESS=webp

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)

function gd_docker() {
    docker run -v $PWD:$PWD --user $USER_ID:$GROUP_ID -i $GDAL_CONTAINER $PWD/$@ $PWD
}

function gd_docker_shell() {
    docker run -v $PWD:$PWD -it $GDAL_CONTAINER $PWD/$@ $PWD
}

gd_docker $@
