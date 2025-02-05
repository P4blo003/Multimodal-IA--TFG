#!/bin/bash

ARGS=1

if [ $# -ne $ARGS ]
then
    echo "Bad Command"
    echo "Uso: ./install-model.sh <model_name>"
else
    python3 install.py $1
fi