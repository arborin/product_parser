#!/bin/bash

export DISPLAY=:0

screen -XS extscrap quit

screen -dmS extscrap /usr/bin/python3 /home/user/web_scrapping/exteriores.py > /home/user/log.txt
