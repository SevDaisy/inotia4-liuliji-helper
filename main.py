from .utils.model import GemLevel, GemFilter, Entry
from .pkg.SL强化 import SL强化
from .pkg.SL宝石 import SL宝石
from .pkg.SL孔位 import SL孔位


print("main OK")


# 规定到什么水平的宝石可以留.
# 我现在比较穷, 顶级宝石基本就留了.
gf = GemFilter([
    Entry.from_str("暴击率: 8%"),  # 顶7混8.5
    # Entry.from_str("命中率: 6.5%"),  # 顶7混8.5
    Entry.from_str("暴击伤害增加率: 13%"),  # 顶12混13.5
    # Entry.from_str("魔法抵抗率: 3.5%"),  # 顶3.4混4
    # Entry.from_str("回避率: 3%"),  # # 顶3.4混4
    # Entry.from_str("MP恢复: 4"),  # 顶4混5
    # Entry.from_str("智力: 20"),  # 顶20混25
])

# SL宝石(gf, saveIndex=1, 背包上界=3, target=GemLevel.顶级, mode="Only Prepare")
# SL宝石(gf, saveIndex=1, 背包上界=1, target=GemLevel.顶级, mode="FULL")

# SL宝石(gf, saveIndex=1, 背包上界=3, target=GemLevel.混沌, mode="FULL")
# SL宝石(gf, saveIndex=1, 背包上界=3, target=GemLevel.混沌, mode="FULL")

# SL强化(saveIndex=1, packIndex=1, maxSuccess=12)
# SL强化(saveIndex=1, packIndex=1, mode="混沌卷轴")

SL孔位(saveIndex=1, packIndex=1, posID="00", is可强化装备=False)
