#!/bin/bash

source venv/bin/activate
echo $1
echo $2
venv/bin/python run.py $1 $2