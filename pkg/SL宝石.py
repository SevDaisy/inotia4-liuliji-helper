

from ..utils.auto import ocrFind, ocrGet, ocrPaddle_V5, pClick, pin, toast
from ..utils.db import loadPoint, loadRect
from ..utils.model import *


# saveIndex: 第几个存档
# target: 融合到几级宝石：[中级|高级|顶级|混沌]
def SL宝石(saveIndex=1, target=GemLevel.顶级):
    min = 100
    short = 200
    long = 700
    v = {}
    r = {}
    r["属性文本"] = loadRect("融合器-宝石属性文本")
    r["评级文本"] = loadRect("融合器-宝石评级文本")
    for item in [
        # 退出重进
            "菜单", "上一级", "主菜单页", "主菜单选项", "返回主菜单-是", "开始游戏", "跳过登录-否", f"存档{saveIndex}",
        # 去融合
            "平A","融合器-道具合成", "融合器-宝石强化", "宝石配方选择", "宝石配方中级", "宝石配方高级", "宝石配方顶级", "宝石配方混沌",
            "宝石材料位1", "宝石材料位2", "宝石材料位3", "宝石材料添加", "融合器-确认融合", "融合器-确认融合-是", "融合器-融合成功-确认",
        # 辅助按键
            "背包页1", "背包页2", "背包页3", "背包页4", "背包页5",
            "背包格00", "背包格01", "背包格02", "背包格03",
            "背包格10", "背包格11", "背包格12", "背包格13",
            "背包格20", "背包格21", "背包格22", "背包格23",
            "背包格30", "背包格31", "背包格32", "背包格33",
        # 保存
            "马上存档", "马上存档-确认"
    ]:
        v[item] = loadPoint(item)
    for k, p in v.items():
        # print(f"{k}: {"Not found" if p is None else str(p)}")
        if p is None:
            toast("有坐标没取到，程序退出")
            return

    # 规定到什么水平的宝石可以留.
    # 我现在比较穷, 顶级宝石基本就留了.
    gf = GemFilter([
        Entry.from_str("暴击: 6%"),  # 顶7混8.5
        Entry.from_str("命中: 6%"),  # 顶7混8.5
        Entry.from_str("暴击伤害增加: 10.5%"),  # 顶12混13.5
        Entry.from_str("魔法抵抗: 3%"),  # 顶3.4混4
        Entry.from_str("MP恢复: 4"),  # 顶4混5
    ])

    def 重新登录():
        pClick(v["主菜单页"], before=long, msg="打开主菜单页")
        pClick(v["主菜单选项"], before=short, msg="点击主菜单选项")
        pClick(v["返回主菜单-是"], before=short, msg="点击返回主菜单-是")
        pClick(v["开始游戏"], before=long, msg="点击开始游戏")
        pClick(v["跳过登录-否"], before=short, msg="点击跳过登录-否")
        pClick(
            v[f"存档{saveIndex}"],
            before=long, after=long,
            msg=f"点击存档{saveIndex}"
        )

    def 确认并保存():
        pClick(v["上一级"], before=short, msg="退出宝石强化界面")
        pClick(v["上一级"], before=short, msg="退出融合器界面")
        pClick(v["马上存档"], before=short, msg="存个档")
        pClick(v["马上存档-确认"], before=short)

    def 进入宝石强化界面():
        pClick(v["平A"], before=short, msg="打开融合器")
        if ocrFind("宝石") is None:
            pClick(v["融合器-道具合成"], before=min)
        pClick(v["融合器-宝石强化"], before=short, msg="打开宝石强化界面")

    def 选择宝石配方(target: GemLevel):
        pClick(v["宝石配方选择"], before=short)
        pClick(v[f"宝石配方{target.name}"], before=short)

    def 添加宝石原料并合成(gems: list):
        delayX = min
        for i in range(3):
            p, r, c = gems[i].location()
            toast(f"idx={gems[i].index} p={p}, r={r}, c={c}", duration=2000)
            pClick(v[f"背包页{p}"], before=delayX)
            pClick(v[f"宝石材料位{i+1}"], before=delayX)
            pClick(v[f"背包格{r}{c}"], before=delayX)
            pClick(v["宝石材料添加"], before=delayX)

        pClick(v["融合器-确认融合"], before=delayX)
        pClick(v["融合器-确认融合-是"], before=delayX)
        pClick(v["融合器-融合成功-确认"], before=delayX)

    res = ocrFind('宝石')
    if  res is None:
        进入宝石强化界面()

    # 整理背包, 录入当前已有宝石
    gList = []
    i = 0
    cnt = 0
    for page in range(0, 4):
        pClick(v[f"背包页{page+1}"], before=short)
        for row in range(4):
            for col in range(4):
                i += 1
                pClick(v[f"背包格{row}{col}"], before=min, after=min)
                img评级 = pin(rect=r["评级文本"])
                img属性 = pin(rect=r["属性文本"])
                txt = ocrGet(img=img评级)
                level = None
                if txt is not None and txt[0].endswith("宝石"):
                    level = GemLevel.from_str(txt[0][:-2])
                if level is None:
                    continue
                txt = ocrPaddle_V5(img=img属性)
                if txt is None:
                    toast("异常! 识别不到宝石属性文本")
                    continue
                data = Entry.from_str(txt[0])
                if data.kind == EntryKind.错误:
                    toast(f"异常文本: {repr(txt)} like {txt}")
                    txt = ocrGet(r["属性文本"])
                    data = Entry.from_str(txt[0])
                if data.kind != EntryKind.错误:
                    cnt += 1
                    gList.append(Gem(i-1, level, data))
                    toast(f"第 {cnt} 颗, {gList[cnt-1]}")
    pClick(v["背包页1"], before=short)

    # 遍历宝石列表, 已经达标的宝石, 不再作为合成原料
    gLibrary = [{} for _ in range(6)]  # gLibrary[GemLevel(1~5)] = {idx: gem}
    record = [False] * 80  # 标记这个位置是否为原料
    filtered = gf.apply(gList)
    for g in filtered:
        if g.kind < target:
            record[g.index] = True
            gLibrary[g.kind.value][g.index] = g

    print(gLibrary)

    # 遍历低级宝石, 合成为中级。每3个低级宝石合成为1个中级宝石. gs[0] 是留空的，不可用。 1~5 分别是低级中级高级顶级混沌。
    lv = 1
    while lv < target.value:
        选择宝石配方(GemLevel(lv+1))

        gems = list(gLibrary[lv].values())
        # 每次取 3 个，不足 3 个时退出
        for i in range(0, len(gems) - 2, 3):
            添加宝石原料并合成(gems[i:i+3])
        lv += 1
