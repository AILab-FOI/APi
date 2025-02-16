#!/bin/bash

ps -ef | awk '$2 > 200' | while read -r line; do
    pid=$(echo $line | awk '{print $2}')
    echo "Killing process $pid"
    kill -9 $pid
done