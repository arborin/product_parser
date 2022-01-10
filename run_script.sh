#!/bin/bash

export DISPLAY=:0

screen -XS scrap quit

screen -dmS scrap /usr/bin/python3 /home/user/web_scrapping/evisaforms.py > /home/user/log.txt
