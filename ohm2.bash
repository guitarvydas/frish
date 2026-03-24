#!/bin/bash
set -eE
export SHELLOPTS
shopt -s nullglob
echo '*** 3'
node nanodsl.3.mjs test.ohm2 >/dev/null
# echo '*** 4'
# node nanodsl.4.mjs test.ohm2 >/dev/null
# echo '*** 5'
# node nanodsl.5.mjs test.ohm2 >/dev/null

