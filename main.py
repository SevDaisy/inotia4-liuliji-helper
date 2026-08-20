from .utils.auto import Point, drawCross, drawRegion, pClick
from .utils.db import v, r
from .utils.model import GemLevel, GemFilter, Entry
from .pkg.SL强化 import SL强化
from .pkg.SL宝石 import SL宝石
from .pkg.SL孔位 import SL孔位


print("main OK")

gf = GemFilter([
    Entry.from_str("暴击率: 8.6%"),
    # 注意 一行代码的开头如果是 # 井字符, 那么这行代码就是不会有任何作用的, 是不生效的。
    # Entry.from_str("暴击伤害增加率: 16.5%"),
    # Entry.from_str("回避率: 4.5%"),
    # Entry.from_str("MP恢复: 6"),
    # Entry.from_str("魔法抵抗率: 4%"),
])


SL宝石(gf, mode="bug")
