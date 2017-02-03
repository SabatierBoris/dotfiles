#!/usr/bin/env bash

PWD=$(pwd)

function link {
	local currentDir=$1
	local targetDir=$2
	local prefix=$3
	for file in `ls ${currentDir} | grep -v $(basename $0) | grep -v README.md`; do
		local target=${targetDir}/${prefix}${file}
		local current=${currentDir}/${file}
		if [ -e ${target} ]; then
			if ! [ -h ${target} ] && [ "$(readlink ${target})" != "${current}" ]; then
				if [ -d ${current} ]; then
					link ${current} ${target} ""
				else
					echo "Can't link ${target} debause it's already exists"
				fi
			fi
		else
			ln -s ${current} ${target}
		fi
	done
}

link $(pwd) ${HOME} "."
