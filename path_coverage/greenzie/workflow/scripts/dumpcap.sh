#!/usr/bin/env bash

NOW=$(date +"%T")

dumpcap -w /home/joe/catkin_ws/src/data/dumpcap/data.$NOW -f "host turtlebot"

