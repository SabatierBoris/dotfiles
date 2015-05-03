#!/usr/bin/env bash

PWD=$(pwd)

for file in `ls ${PWD} | grep -v $(basename $0)`; do
    echo "Creating symplink to ${file} in ~"
    ln -s ${PWD}/${file} ${HOME}/.${file}
done
