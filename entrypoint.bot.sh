#!/bin/bash
LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
PYTHONPATH=/lib/

echo Waiting else we have e r r o r 111
sleep 12

#pip freeze
ls -al
python3 -m bot

exec "$@"
