from enum import Enum


class EntryKind(Enum):
    @classmethod
    def from_str(cls, s: str):
        for member in cls:
            if member.value == s:
                return member
        return cls.错误

    def __init__(self, value: str, idx: int):
        self._value_ = value
        self.idx = idx

    def __hash__(self):
        return self.idx

    def __eq__(self, other):
        return self.name == other.name

    力量 = ("力量", 0)
    敏捷 = ("敏捷", 1)
    体力 = ("体力", 2)
    智力 = ("智力", 3)
    精力 = ("精力", 4)
    暴击 = ("暴击率", 5)
    命中 = ("命中率", 6)
    暴伤抵抗 = ("暴击伤害抵抗率", 7)
    魔抗 = ("魔法抵抗率", 8)
    闪避 = ("回避率", 9)
    盾牌格挡 = ("盾牌格挡率", 10)
    武器格挡 = ("武器格挡率", 11)
    MP增加 = ("MP增加", 12)
    MP回复 = ("MP恢复", 13)
    暴击抵抗 = ("暴击抵抗率", 14)
    暴伤增加 = ("暴击伤害增加率", 15)
    吸血 = ("HP吸收", 16)
    火 = ("火", 17)
    风 = ("风", 18)
    寒气 = ("寒气", 19)
    神圣 = ("神圣", 20)
    黑暗 = ("黑暗", 21)
    毒 = ("毒", 22)
    重力摆 = ("重力摆", 23)
    冰霜 = ("冰霜", 24)
    治愈气息 = ("治愈气息", 25)
    狂战士 = ("狂战士", 26)
    瞬间回复 = ("瞬间回复", 27)
    魔力专家 = ("魔力专家", 28)
    减少敌意 = ("减少敌意", 29)
    眩晕抗性 = ("眩晕抗性", 30)
    睡眠抗性 = ("睡眠抗性", 31)
    失明抗性 = ("失明抗性", 32)
    恐惧抗性 = ("恐惧抗性", 33)
    减速抗性 = ("减速抗性", 34)
    沉默抗性 = ("沉默抗性", 35)
    错误 = ("错误", 36)


class Entry:
    def __init__(self, kind: EntryKind, value: float):
        self.kind = kind
        self.value = value

    def isKind(self, kind: str):
        return self.kind == EntryKind.from_str(kind)

    @classmethod
    def ParseNumber(cls, s: str) -> float:
        """尝试将字符串解析为整数、浮点数或百分数，失败时返回 0.0"""

        try:
            return int(s)      # 尝试整数
        except ValueError:
            try:
                return float(s)  # 尝试浮点数
            except ValueError:
                if s.endswith('%'):
                    try:
                        return float(s[:-1]) / 100  # 处理百分数
                    except ValueError:
                        print(f"警告: 无法解析百分数字符串 '{s}'，返回 0.0")
                        return 0.0
                else:
                    print(f"警告: 无法解析数字字符串 '{s}'，返回 0.0")
                    return 0.0

    @classmethod
    def from_str(cls, s: str):
        s=translated(s)
        tmp = s.split(":")
        if len(tmp) < 2:
            return Entry(EntryKind.错误, 0)
        kind = EntryKind.from_str(tmp[0])
        value = Entry.ParseNumber(tmp[1])
        return Entry(kind, value)

    def __str__(self):
        formatted = f"{self.value:.0f}"
        if self.value < 1:
            formatted = f"{self.value * 100:.1f}%"
        return f"{self.kind.name}:{formatted}"

    def __repr__(self):
        return self.__str__()


class GemLevel(Enum):
    错误 = 0
    低级 = 1
    中级 = 2
    高级 = 3
    顶级 = 4
    混沌 = 5

    @classmethod
    def from_str(cls, s: str):
        # print(f"GemLevel.from_str: '{s}'")
        for member in cls:
            if s == member.name:
                return member
        return cls.错误

    def __lt__(self, other):
        return self.value < other.value


class Gem:
    def __init__(self, index: int, level: GemLevel, data: Entry):
        self.index = index  # 在背包中的位置, 理论合法值 0~79
        self.kind = level
        self.data = data

    def isLevel(self, level: int):
        return self.kind == Gem(level)

    def location(self):
        page = int(self.index / 16)
        row = int(int(self.index % 16)/4)
        col = self.index - page * 16 - row * 4
        return page+1, row, col

    def __str__(self):
        return f"{self.kind.name}宝石{self.index} {self.data}"

    def __repr__(self):
        return self.__str__()


class GemFilter:
    def __init__(self, targetEntry: list):
        kindNeed = {}
        valueMin = {}

        for entry in targetEntry:
            kindNeed[entry.kind] = True
            data = entry.value
            stored = valueMin.get(entry.kind, 0)
            valueMin[entry.kind] = data if data > stored else stored

        self.kindNeed = kindNeed
        self.valueMin = valueMin

    def append(self, targetEntry: list):
        kindNeed = self.kindNeed
        valueMin = self.valueMin

        for entry in targetEntry:
            kindNeed[entry.kind] = True
            data = entry.value
            stored = valueMin.get(entry.kind, 0)
            valueMin[entry.kind] = data if data > stored else stored

        self.kindNeed = kindNeed
        self.valueMin = valueMin

    def remove(self, targetKind: list):
        for kind in targetKind:
            self.kindNeed[kind] = False
            self.valueMin[kind] = 0

    def apply(self, gems: list):
        """ 去掉足够优秀的宝石 """
        res = [
            gem for gem in gems
            if not self.kindNeed.get(gem.data.kind, False)
            or gem.data.value >= self.valueMin.get(gem.data.kind, 0)
        ]

        print(res)
        return res

    def check(self, gem: None) -> bool:
        """ true 说明宝石足够好 """
        return self.kindNeed.get(gem.kind, False) and gem.data.value >= self.valueMin.get(gem.kind, 0)


def translated(s: str) -> str:
    trans = {
        ord('増'): '增',
        ord('：'): ':',
        ord('|'): None
    }
    return s.translate(trans)

if __name__ == "__main__":
    def testGemFilter():
        ds = [
            Gem(0, GemLevel.低级, Entry(EntryKind.力量, 100)),
            Gem(1, GemLevel.中级, Entry(EntryKind.暴击, 100)),
            Gem(1, GemLevel.中级, Entry(EntryKind.暴击, 0.01)),
            Gem(1, GemLevel.中级, Entry(EntryKind.暴击, 1.6*0.01)),
            Gem(2, GemLevel.高级, Entry(EntryKind.暴伤增加, 100)),
            Gem(2, GemLevel.高级, Entry(EntryKind.暴伤增加, 0.01)),
            Gem(3, GemLevel.顶级, Entry(EntryKind.闪避, 100)),
            Gem(3, GemLevel.顶级, Entry(EntryKind.闪避, 0.01)),
            Gem(4, GemLevel.低级, Entry(EntryKind.MP回复, 100)),
            Gem(4, GemLevel.低级, Entry(EntryKind.MP回复, 0.01)),
        ]

        f = GemFilter([
            Entry.from_str("暴击率: 6%"),  # 顶7混8.5
            Entry.from_str("命中率: 6%"),  # 顶7混8.5
            Entry.from_str("暴击伤害增加率: 10.5%"),  # 顶12混13.5
            Entry.from_str("魔法抵抗率: 3%"),  # 顶3.4混4
            Entry.from_str("MP恢复: 4"),  # 顶4混5
        ])
        print(f.kindNeed)
        print(f.valueMin)
        f.apply(ds)
        print(f"f.check(ds[0]) -> {f.check(ds[0])}")
        print(f"f.check(ds[1]) -> {f.check(ds[1])}")

    def testEntryParse():
        for s in [
            "敏捷: 2",
            "MP恢复: 3",
            "暴击率: 1.69%",
            "暴击伤害增加率:7.9%",
            "暴击伤害増加率: 7.9%",
            '暴击伤害增加率：7.9%',
        ]:
            e = Entry.from_str(s)
            # if e.kind == EntryKind.错误:
            print(f"{s:<{40}} ---> {e}")

    def testSlice():
        gems = list(range(16))
        print(gems)
        for i in range(0, len(gems)-2, 3):
            print(gems[i:i+3])

    def testLocation():
        g = Gem(0, GemLevel.中级, Entry(EntryKind.力量, 1))
        p, r, c = g.location()
        print(f"p={p}, r={r}, c={c}")

    # testLocation()
    testGemFilter()
    # testEntryParse()
    pass
