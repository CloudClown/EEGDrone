#!/bin/bash

rosmake ardrone_autonomy

if [ $? -eq 0 ]; then
    echo "[package] ardrone_autonomy is already installed..."
else
    echo "[download] ardrone_autonomy package......"
    git clone git://github.com/tum-vision/ardrone_autonomy.git
    echo "[build] ardrone_autonomy package.......ARSDroneLib and collatorals"
    cd ardrone_autonomy && ./build_sdk.sh && cd ..
    rosmake ardrone_autonomy
fi

rosmake tum_ardrone

if [ $? -eq 0 ]; then
    echo "[package] tum_ardrone is already installed..."
else
    echo "[download] the tum package......"
    git clone git://github.com/tum-vision/tum_ardrone.git
    echo "[rosmake] the tum package......."
    rosmake tum_ardrone
    rosmake eeg_control
fi

echo "[rosmake] EEGControlMsgs..."
rosmake EEGControlMsgs