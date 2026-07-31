#!/usr/bin/bash

source "$(dirname $0)/common.sh"

act=${1:-read}

data="""
背包范围: (1390,246,2193,1007)
融合器-宝石属性文本: (670,330,1282,395)
融合器-宝石评级文本: (669,264,1267,338)
"""

work "rect" "$act"
