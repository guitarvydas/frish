#!/bin/sh

cleanup() {
    mv @hold-makec @makec
    if [ -f out.✗ ]; then
        cat out.✗
    else
        echo "*** No Errors ***"
    fi
}

trap cleanup EXIT

cp @makec @hold-makec
cp @dev-makec @makec
~/.local/bin/@make
