#!/bin/bash
set -eE
export SHELLOPTS
shopt -s nullglob
test=test.ohm2
echo
echo '*** bracket matching'
export PBPWD=$(pwd)
export PBP="$(pwd)/pbp"
export PYTHONPATH="${PBP}/kernel:${PYTHONPATH}"
export PBPCALLER=$PBPWD
./pbp/t2t bracketmatch <"${test}"
echo
echo '*** 3'
node nanodsl.3.mjs "${test}"
# echo '*** 4'
# node nanodsl.4.mjs test.ohm2 >/dev/null
# echo '*** 5'
# node nanodsl.5.mjs test.ohm2 >/dev/null

