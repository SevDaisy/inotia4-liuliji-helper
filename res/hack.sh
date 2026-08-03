#!/bin/bash

base=$(dirname $(realpath $0))

rm ${base}/../res/point/* ${base}/../res/rect/* 2>/dev/null

${base}/../res/point.sh w
${base}/../res/rect.sh w
