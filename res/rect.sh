#!/usr/bin/bash

source "$(dirname $0)/common.sh"

act=${1:-read}

data="""
融合器-背包范围: (1390,246,2193,1007)
融合器-宝石评级文本: (675,273,880,325)
融合器-宝石属性文本: (678,342,1100,384)
"""

work "rect" "$act"
