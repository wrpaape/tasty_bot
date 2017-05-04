#!/bin/bash

# GLOBAL VARIABLES
# ==============================================================================
SAMPLES_DIR=/home/reid/visual_semantics/alexa-avs-sample-app/samples
COMPANION_SERVICE_DIR=$SAMPLES_DIR/companionService
JAVA_CLIENT_DIR=$SAMPLES_DIR/javaclient
APP_LOG=$JAVA_CLIENT_DIR/logs/application.log
THIS_DIR=`dirname $BASH_SOURCE`
IMAGES_DIR=$THIS_DIR/images


# HELPER FUNCTIONS
# ==============================================================================
# open images in background
open_images() {
    eog --new-instance $IMAGES_DIR/*.{png,jpg,gif} &
}

# start wireshark in background (may prompt for password)
start_wireshark() {
    sudo wireshark 1>/dev/null 2>/dev/null &
}

# start auth server in background
start_companion_service() {
    cd $COMPANION_SERVICE_DIR \
    && npm start 1>/dev/null &
}

# clear log file, build, then run the java client in background
start_java_client() {
    truncate $APP_LOG --size 0   \
    && cd $JAVA_CLIENT_DIR       \
    && mvn install   1>/dev/null \
    && mvn exec:exec 1>/dev/null &
}

# tail java client log file in foreground
start_monitoring_logs() {
    JSON='^\({\|\s*\("\|}\)\).*'
    THREADS='\(downchannel\)\?requestthread'
    DIRECTIVES='directive'
    ANY='$'
    # MATCH="$JSON\|$THREADS\|$DIRECTIVES\|$ANY"
    MATCH="$JSON\|$THREADS"
    tail --follow $APP_LOG | grep --ignore-case --color $MATCH
}

# ensure background processes killed on exit
cleanup() {
    BG_PIDS=`jobs -pr`
    [ -n "$BG_PIDS" ] && kill $BG_PIDS 2>/dev/null
}


# PROGRAM ENTRY
# ==============================================================================
trap cleanup SIGINT SIGTERM EXIT \
&& open_images                   \
&& start_wireshark               \
&& start_companion_service       \
&& start_java_client             \
&& start_monitoring_logs
