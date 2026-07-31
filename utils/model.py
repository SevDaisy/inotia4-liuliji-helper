from enum import Enum
from xml.etree.ElementTree import tostring


class EntryKind(Enum):
    @classmethod
    def from_str(cls, s: str):
        for member in cls:
            if member.value in s:
                return member
        return cls.错误

    力量 = "力量"
    敏捷 = "敏捷"
    体力 = "体力"
    智力 = "智力"
    精力 = "精力"
    暴击 = "暴击"
    命中 = "命中"
    暴伤抵抗 = "暴击伤害抵抗"
    魔抗 = "魔法抵抗"
    闪避 = "回避"
    盾牌格挡 = "盾牌格挡"
    武器格挡 = "武器格挡"
    MP增加 = "MP增加"
    MP回复 = "MP回复"
    暴击抵抗 = "暴击抵抗"
    暴伤增加 = "暴击伤害增加"
    吸血 = "HP吸收"
    火 = "火"
    风 = "风"
    寒气 = "寒气"
    神圣 = "神圣"
    黑暗 = "黑暗"
    毒 = "毒"
    重力摆 = "重力摆"
    冰霜 = "冰霜"
    治愈气息 = "治愈气息"
    狂战士 = "狂战士"
    瞬间回复 = "瞬间回复"
    魔力专家 = "魔力专家"
    减少敌意 = "减少敌意"
    眩晕抗性 = "眩晕抗性"
    睡眠抗性 = "睡眠抗性"
    失明抗性 = "失明抗性"
    恐惧抗性 = "恐惧抗性"
    减速抗性 = "减速抗性"
    沉默抗性 = "沉默抗性"
    错误 = "错误"


class Entry:
    def __init__(self, kind: EntryKind, value: float):
        self.kind = kind
        self.value = value

    def isKind(self, kind: str):
        return self.kind == EntryKind.from_str(kind)

    def isGE(self, value: float):
        return self.value >= value

    @classmethod
    def ParseNumber(cls, s: str):
        """尝试将字符串解析为整数或浮点数，支持百分数"""
        s = s.strip()
        try:
            # 先尝试直接转换为整数
            return int(s)
        except ValueError:
            try:
                # 整数不行，再试试浮点数
                return float(s)
            except ValueError:
                # 如果都不行，检查是不是百分数
                if s.endswith('%'):
                    # 去掉 '%'，转为浮点数后除以 100
                    return float(s[:-1]) / 100
                # 如果都不是，可以返回 None 或者抛出异常，看你的需求
                return float(0)

    def __str__(self):
        formatted = f"{self.value:.0f}"
        if self.value < 1:
            formatted = f"{self.value * 100:.1f}%"
            # formatted = formatted.rstrip('0').rstrip('.')  # 去除多余的0和小数点
        return f"{self.kind.name}:{formatted}"

    def __repr__(self):
        return self.__str__(self)


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

    @classmethod
    def Data(cls, s: str):
        # print(f"Gem.Data: '{s}'")
        tmp = s.split(":")
        if len(tmp) < 2:
            return Entry(EntryKind.错误, 0)
        kind = EntryKind.from_str(tmp[0])
        value = Entry.ParseNumber(tmp[1])
        return Entry(kind, value)

    def __str__(self):
        return f"{self.kind.name}宝石 {self.data}"

    def __repr__(self):
        return self.__str__(self)
