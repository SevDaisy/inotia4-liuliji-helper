#!/usr/bin/env bash

base=$(realpath $(dirname $0))
port=${1:-8080}

echo """
adb disconnect
adb connect 192.168.31.10:$port

# adb shell rm -rvf /sdcard/AScript/inotia4/point
adb push .\auto\point.zip /sdcard/AScript/inotia4
adb shell ls -la /sdcard/AScript/inotia4/point
"""

### adb push 推不上去。DeepSeek 说是 Windows ADB 有 bug，无法处理大小为 512B 整数倍的文件。笑死。