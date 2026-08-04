from .utils.model import GemLevel, GemFilter, Entry
from .pkg.SL强化 import SL强化
from .pkg.SL宝石 import SL宝石
from .pkg.SL孔位 import SL孔位


print("main OK")


# 规定到什么水平的宝石可以留.

# 0621
# 暴击 9% | 暴伤 16.5%
# 0801
# 暴击 8.6% | 暴伤 13.6% | 暴伤抵抗 25.1%
gf = GemFilter([
    Entry.from_str("HP吸收: 8%"),  # 混 4.3~8.6
    Entry.from_str("暴击率: 8%"),  # 混 4.3~8.6
    Entry.from_str("暴击伤害增加率: 15%"),  # 混 6.8~13.6
    Entry.from_str("暴击伤害抵抗率: 23%"),  # 混 12~25.1
    Entry.from_str("魔法抵抗率: 4%"),  # 混 4.2
    Entry.from_str("回避率: 4%"),  # 混 4.5
    # Entry.from_str("MP增加: 88"),  #
])

# SL宝石(gf, saveIndex=1, 背包上界=3, target=GemLevel.顶级, mode="Only Prepare")
# SL宝石(gf, saveIndex=1, 背包上界=1, target=GemLevel.顶级, mode="FULL")

SL宝石(gf, saveIndex=1, 背包上界=3, target=GemLevel.混沌, mode="FULL")
# SL宝石(gf, saveIndex=1, 背包上界=1, target=GemLevel.混沌, mode="FULL")

# SL强化(saveIndex=1, packIndex=1, maxSuccess=12)
# SL强化(saveIndex=1, packIndex=1, mode="混沌普通")
# SL强化(saveIndex=1, packIndex=1, mode="混沌关键")

# SL孔位(saveIndex=1, packIndex=1, posID="00", is可强化装备=True)
