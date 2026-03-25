#!/bin/sh

cleanup() {
    mv @hold-makec @makec
    [ -f out.x ] && cat out.x
}
trap cleanup EXIT

cp @makec @hold-makec
cp @dev-makec @makec
./@make
