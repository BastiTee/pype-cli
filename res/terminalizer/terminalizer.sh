#!/bin/bash
cwd="$( cd "$( dirname "$0" )"; pwd )"
cd $cwd

if [ "$1" == "record" ]; then
    cnt_name="terminalizer-pype-cli"
    echo "You are here: $cwd"
    docker build -t $cnt_name .
    docker kill $cnt_name-container ||true
    docker rm $cnt_name-container ||true
    docker create --name $cnt_name-container -t -i $cnt_name \
    record --config /config.yml record
    docker cp $cwd/config.yml $cnt_name-container:config.yml
    docker cp $cwd/docker-entrypoint.sh $cnt_name-container:/usr/local/bin/docker-entrypoint.sh
    docker start -i --attach $cnt_name-container
    docker cp $cnt_name-container:record.yml $cwd/record.yml
fi

# For rendering we need a display host therefore no docker here
if [ "$1" == "render" ]; then
    bin=node_modules/terminalizer/bin/app.js
    [ ! -f $bin ] && npm install terminalizer
    [ ! -d ~/.terminalizer ] && $bin init
    [ "$1" == "render" ] && $bin render record.yml --output pype-cli.gif --quality 100
fi
