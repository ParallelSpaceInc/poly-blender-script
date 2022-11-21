#!/bin/bash
if [ "$#" = 1 ]
then
	blender -b -P "$1"
else
	echo 2gltf2.sh [SCRIPT.py]
fi
