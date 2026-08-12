from .utils.model import GemLevel, GemFilter, Entry
from .pkg.SL强化 import SL强化
from .pkg.SL宝石 import SL宝石
from .pkg.SL孔位 import SL孔位


print("main OK")

gf0621 = GemFilter([
    Entry.from_str("暴击伤害增加率: 16.5%"),

])
gf0804 = GemFilter([
    Entry.from_str("暴击率: 8.6%"),
    Entry.from_str("回避率: 4.5%"),
])


def _example():
    gf = GemFilter([
        Entry.from_str("暴击率: 6%"),
        Entry.from_str("暴击伤害增加率: 10.5%"),
        Entry.from_str("回避率: 4%"),
        Entry.from_str("MP增加: 70"),
        Entry.from_str("MP恢复: 4"),
        # Entry.from_str("HP吸收: 8%"),
        # Entry.from_str("魔法抵抗率: 4%"),
        # Entry.from_str("暴击伤害抵抗率: 22%"),
    ])
    SL宝石(gf, saveIndex=1, 背包上界=3, target=GemLevel.顶级, mode="Only Prepare")
    SL宝石(gf, saveIndex=1, 背包上界=1, target=GemLevel.顶级, mode="FULL")

    SL宝石(gf, saveIndex=1, 背包上界=1, target=GemLevel.混沌, mode="FULL")

    SL强化(saveIndex=1, packIndex=1, maxSuccess=12)
    SL强化(saveIndex=1, packIndex=1, mode="混沌普通")
    SL强化(saveIndex=1, packIndex=1, mode="混沌关键")

    SL孔位(saveIndex=1, packIndex=1, posID="00", is可强化装备=True)


def _0621刷暴伤():
    gf = GemFilter([
        # Entry.from_str("HP吸收: 8%"),  # 混 4.3~8.6
        Entry.from_str("暴击率: 8.5%"),  # 混 4.3~8.6
        Entry.from_str("暴击伤害增加率: 16%"),  # 混 6.8~13.6
        # Entry.from_str("暴击伤害抵抗率: 22%"),  # 混 12~25.1
        # Entry.from_str("魔法抵抗率: 4%"),  # 混 4.2
        # Entry.from_str("回避率: 4%"),  # 混 4.5
        # Entry.from_str("MP增加: 88"),  #
    ])
    SL宝石(gf, saveIndex=1, 背包上界=4, target=GemLevel.混沌, mode="FULL")


def _0804魔导():
    gf = GemFilter([
        # Entry.from_str("HP吸收: 8%"),  # 混 4.3~8.6
        Entry.from_str("暴击率: 8%"),  # 混 4.3~8.6
        # Entry.from_str("暴击伤害增加率: 15%"),  # 混 6.8~13.6
        Entry.from_str("暴击伤害抵抗率: 22%"),  # 混 12~25.1
        # Entry.from_str("魔法抵抗率: 4%"),  # 混 4.2
        # Entry.from_str("回避率: 4%"),  # 混 4.5
        # Entry.from_str("MP增加: 88"),  #
    ])
    # SL宝石(gf, saveIndex=1, 背包上界=2, target=GemLevel.混沌, mode="FULL")
    SL孔位(saveIndex=1, packIndex=1, posID="00", is可强化装备=True)


def _0804刺客():
    # 新档 顶级宝石就可以留 低1 中3 高9 顶27
    gf = GemFilter([
        Entry.from_str("暴击率: 9%"),
        Entry.from_str("暴击伤害增加率: 16.5%"),
        Entry.from_str("回避率: 4.5%"),
        # Entry.from_str("MP恢复: 5"),
        # Entry.from_str("暴击抵抗率: 13%"),  # 后期找机会单出一个
        # Entry.from_str("HP吸收: 8%"),
        # Entry.from_str("魔法抵抗率: 4%"),
    ])

    SL孔位(saveIndex=2, packIndex=1, posID=f"00", is可强化装备=False)
    # SL孔位(saveIndex=2, packIndex=1, posID=f"00", is可强化装备=True)
    # SL孔位(saveIndex=2, packIndex=1, posID=f"01", is可强化装备=True)
    # SL强化(saveIndex=2, packIndex=1, maxSuccess=13)
    # SL强化(saveIndex=2, packIndex=1, mode="21")
    # SL宝石(gf, saveIndex=2, 背包上界=1, target=GemLevel.混沌, mode="Only Prepare")
    # SL宝石(gf, saveIndex=2, 背包上界=2, target=GemLevel.混沌, mode="FULL")
    # SL宝石(gf, saveIndex=2, mode="bug")


def 新档狂战():
    # 新档 顶级宝石就可以留 低1 中3 高9 顶27
    gf = GemFilter([
        Entry.from_str("暴击率: 9%"),
        Entry.from_str("暴击伤害增加率: 16.5%"),
        Entry.from_str("回避率: 4.5%"),
        # Entry.from_str("MP恢复: 5"),
        # Entry.from_str("暴击抵抗率: 13%"),  # 后期找机会单出一个
        # Entry.from_str("HP吸收: 8%"),
        # Entry.from_str("魔法抵抗率: 4%"),
    ])

    SL孔位(saveIndex=3, packIndex=1, posID=f"00", is可强化装备=False)
    # SL孔位(saveIndex=3, packIndex=1, posID=f"00", is可强化装备=True)
    # SL孔位(saveIndex=3, packIndex=1, posID=f"01", is可强化装备=True)
    # SL强化(saveIndex=3, packIndex=1, maxSuccess=13)
    # SL强化(saveIndex=3, packIndex=1, mode="21")
    # SL宝石(gf, saveIndex=3, 背包上界=1, target=GemLevel.混沌, mode="Only Prepare")
    # SL宝石(gf, saveIndex=3, 背包上界=2, target=GemLevel.混沌, mode="FULL")
    # SL宝石(gf, saveIndex=3, mode="bug")


新档狂战()

# _0621刷暴伤()
# _0804魔导()
