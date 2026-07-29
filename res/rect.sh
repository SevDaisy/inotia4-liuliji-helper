#!/usr/bin/bash

source "$(dirname $0)/common.sh"

act=${1:-read}

data="""
背包范围: (1390,246,2193,1007)
融合器-宝石属性文本: (659,336,1355,423)
融合器-宝石种类文本: (669,264,878,338)
"""

work "rect" "$act"
