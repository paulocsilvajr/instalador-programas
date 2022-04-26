#!/usr/bin/env bash
# fonte: https://stackoverflow.com/questions/6980090/how-to-read-from-a-file-or-standard-input-in-bash

LOGFILE="completo.log"

function log() {
    BASELOG=$(dirname $0)
    DATACOMPLETA=$(date "+%Y%m%d %H%M%S")

    while read line
    do
        echo "$DATACOMPLETA [$1] $line" | tee -a ${BASELOG}/${LOGFILE}
    done < "${2:-/dev/stdin}"
}

