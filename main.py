# from .pkg.SL强化 import SL强化

# SL强化(saveIndex=1, packIndex=1)


from .pkg.SL宝石 import SL宝石
from .utils.model import GemLevel, GemFilter, Entry

# print("main OK")

# 规定到什么水平的宝石可以留.
# 我现在比较穷, 顶级宝石基本就留了.
gf = GemFilter([
    Entry.from_str("暴击率: 6%"),  # 顶7混8.5
    Entry.from_str("命中率: 6%"),  # 顶7混8.5
    Entry.from_str("暴击伤害增加率: 10%"),  # 顶12混13.5
    Entry.from_str("魔法抵抗率: 3.5%"),  # 顶3.4混4
    Entry.from_str("MP恢复: 4"),  # 顶4混5
])

# SL宝石(gf, saveIndex=1, target=GemLevel.顶级, mode="Only Prepare")
# SL宝石(gf, saveIndex=1, 背包上界=1, target=GemLevel.顶级, mode="FULL")
SL宝石(gf, saveIndex=1, 背包上界=1, target=GemLevel.混沌, mode="FULL")
