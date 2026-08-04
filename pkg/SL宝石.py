from ..utils.auto import imgFind, ocrFind, ocrGet, ocrPaddle_V5, pClick, pin, toast
from ..utils.db import loadPoint, loadRect
from ..utils.model import *


def firstEmpty(isEmpty: list) -> int:
    notFound = -1
    for i in range(0, len(isEmpty)):
        if int(isEmpty[i]) == 1:
            return i
    return notFound


class GemOcrError(Exception):
    """非宝石异常: 截图区域不是宝石或OCR识别失败"""
    pass


class GemParseError(Exception):
    """宝石解析异常: 宝石属性格式无法解析"""

    def __init__(self, level, data, msg=None):
        self.level = level
        self.data = data
        self.msg = msg or f"GemParseError: level={level}, data={data}"
        super().__init__(self.msg)

    def __str__(self):
        return self.msg


def parseGem(r评级, r属性):
    img评级 = pin(rect=r评级)
    img属性 = pin(rect=r属性)

    # 读取宝石评级
    txt = ocrGet(img=img评级)
    level = None
    if txt and len(txt) > 0 and txt[0].endswith("宝石"):
        level = GemLevel.from_str(txt[0][:-2])
    if level is None:
        raise GemOcrError("识别不到宝石评级")

    # 读取宝石属性
    txt = ocrPaddle_V5(img=img属性)
    if not txt or len(txt) == 0:
        raise GemOcrError("识别不到宝石属性")
    data = Entry.from_str(txt[0])
    if data.kind == EntryKind.错误:
        # 使用备用 OCR
        txt_alt = ocrGet(r属性)
        if txt_alt and len(txt_alt) > 0:
            data = Entry.from_str(txt_alt[0])
        else:
            # 或者直接视为解析失败
            data = Entry.from_str("")
    if data.kind == EntryKind.错误:
        raise GemParseError(level=level, data=data, msg="解析宝石属性出错")

    if data.value == 0:
        toast(f"异常: {txt}")
    return level, data


def SL宝石(gf: GemFilter, saveIndex=1, 背包上界=5, target=GemLevel.顶级, mode="Only Prepare"):
    """
    gf: 必需参数 指定保留什么品质及以上的宝石
    saveIndex: 游戏的第几个存档位
    背包上界: 合法值 1~5, 默认是5. 我一般都用 4, 因为第五个背包肯定是被杂物堆满的, 省得程序去扫描了.
    target: 目标是几级宝石 [高级|*顶级|混沌]
    mode:
        - Only Prepare: 只合成到比 target 级别低一级的宝石就停下并保存
        - 否则: 反复存档读档直到所有 target 的原材料都已经被合成为满足 gf 要求的好宝石
    """
    if target < GemLevel.高级:
        # 有人会想要 SL 刷出满值的中级宝石吗? 会有吗? 真有这样的需要, 请自行修改代码
        toast("目标至少得是高级宝石")
        return

    min = 100
    short = 200
    long = 700
    v = {}
    r = {}
    r["属性文本"] = loadRect("融合器-宝石属性文本")
    r["评级文本"] = loadRect("融合器-宝石评级文本")
    r["添加按钮"] = loadRect("融合器-添加按钮")
    r["道具合成"] = loadRect("融合器-道具合成")
    for item in [
        # 退出重进
            "菜单", "上一级", "主菜单页", "主菜单选项", "返回主菜单-是", "开始游戏", "跳过登录-否", f"存档{saveIndex}",
        # 去融合
            "平A", "融合器-道具合成", "融合器-宝石强化", "宝石配方选择", "宝石配方中级", "宝石配方高级", "宝石配方顶级", "宝石配方混沌",
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
        if p is None:
            toast(f"坐标 {k} 没取到，程序退出")
            return

    def 退出并重新登录():
        pClick(v["上一级"], before=short)
        pClick(v["上一级"], before=short)
        pClick(v["菜单"], before=short)
        pClick(v["主菜单页"], before=long)
        pClick(v["主菜单选项"], before=short)
        pClick(v["返回主菜单-是"], before=short)
        pClick(v["开始游戏"], before=long)
        pClick(v["跳过登录-否"], before=short)
        pClick(
            v[f"存档{saveIndex}"],
            before=long, after=long,
            msg=f"点击存档{saveIndex}"
        )

    def 退出并保存():
        pClick(v["上一级"], before=short)
        pClick(v["上一级"], before=short)
        pClick(v["马上存档"], before=short)
        pClick(v["马上存档-确认"], before=short)

    def 进入宝石强化界面():
        pClick(v["平A"], before=short, after=short)
        if ocrGet(img=pin(r['道具合成'])):
            pClick(v["融合器-道具合成"], before=min)
        pClick(v["融合器-宝石强化"], before=short)

    def 选择宝石配方(target: GemLevel):
        print(f"选择配方: 宝石配方{target.name}")
        pClick(v["背包页1"], before=min)  # 点一下背包, 不然宝石信息框会挡住换配方的按钮
        pClick(v["宝石配方选择"], before=min)
        pClick(v[f"宝石配方{target.name}"], before=min)

    def 添加宝石原料并合成(gems: list):
        delayX = min
        for i in range(3):
            p, r, c = pkgLocation(gems[i].index)
            # toast(f"idx={gems[i].index} p={p}, r={r}, c={c}", duration=2000)
            pClick(v[f"背包页{p}"], before=delayX)
            pClick(v[f"宝石材料位{i+1}"], before=delayX)
            pClick(v[f"背包格{r}{c}"], before=delayX)
            pClick(v["宝石材料添加"], before=delayX)

        pClick(v["融合器-确认融合"], before=delayX)
        pClick(v["融合器-确认融合-是"], before=delayX)
        pClick(v["融合器-融合成功-确认"], before=delayX)

    if ocrFind('宝石') is None:
        进入宝石强化界面()

    # 整理背包, 录入当前已有宝石
    gList = [{} for _ in range(6)]  # gLibrary[GemLevel(1~5)] = {idx: gem}
    i = 0
    cnt = 0
    isEmpty = [int(False)] * (背包上界 * 16)  # 记录当前位置是否是空位, 0不是空位, 1是空位
    for page in range(1, 背包上界+1):
        pClick(v[f"背包页{page}"], before=short)
        for row in range(4):
            for col in range(4):
                i += 1
                pClick(v[f"背包格{row}{col}"], before=min, after=min)

                # 空格子跳过
                img按钮 = pin(rect=r['添加按钮'])
                foundBtn = imgFind("宝石材料添加", img按钮)
                # toast(f"{i-1}: ({row},{col}) {'空' if notFound is None else '非空'}")
                if foundBtn is None:
                    isEmpty[i-1] = int(True)
                    continue

                # 解析屏幕中的宝石信息
                try:
                    level, data = parseGem(r["评级文本"], r["属性文本"])
                except GemOcrError:
                    continue
                except GemParseError as e:
                    print(str(e))
                    continue

                # 一切正常, 正常处理
                cnt += 1
                g = Gem(i-1, level, data)
                isGood = gf.check(g)
                toast(f"第 {cnt} 颗, {g} {'成品' if isGood else '材料'}")
                if not isGood:
                    gList[g.level.value][g.index] = g
    pClick(v["背包页1"], before=short)

    # 原材料区数量统计
    for i in range(0, 6):
        print(f"{GemLevel(i).name}: {len((list(gList[i].values())))}")

    # 遍历低级宝石, 合成为中级。每3个低级宝石合成为1个中级宝石. gs[0] 是留空的，不可用。 1~5 分别是低级中级高级顶级混沌。
    # lv 作为材料的宝石的等级
    for lv in range(1, target.value-1):
        if firstEmpty(isEmpty) == -1:
            toast("背包满的，无法合成")
            return

        gems = list(gList[lv].values())

        if len(gems) <= 2:
            # 材料不到 3 个, 跳过这个等级
            continue

        选择宝石配方(GemLevel(lv+1))
        # 每次取 3 个，不足 3 个时退出
        for i in range(0, len(gems) - 2, 3):
            _new = firstEmpty(isEmpty)
            # page, row, col = pkgLocation(_new)
            # toast(f"_new:{_new}, p:{page}, r:{row}, c:{col}")
            # toast("".join(str(int(item)) for item in isEmpty))
            once = gems[i:i+3]
            添加宝石原料并合成(once)
            for item in once:
                isEmpty[item.index] = int(True)
                del gList[item.level.value][item.index]
            isEmpty[_new] = int(False)
            # 查看合成结果
            page, row, col = pkgLocation(_new)
            pClick(v[f"背包页{page}"], before=min)
            pClick(v[f"背包格{row}{col}"], before=min, after=min)

            # 解析屏幕中的宝石信息
            try:
                level, data = parseGem(r["评级文本"], r["属性文本"])
            except GemOcrError:
                continue
            except GemParseError as e:
                print(str(e))
                continue
            # 新宝石加入原料库
            g = Gem(_new, level, data)
            isGood = gf.check(g)
            toast(f"得到 {g} {'成品' if isGood else '材料'}")
            if not isGood:
                gList[g.level.value][g.index] = g

    if mode == "Only Prepare":
        return
    elif firstEmpty(isEmpty) == -1:
        toast("背包满的，无法合成")
        return
    # ===============================================================================
    # ================================ 开始 SL 刷宝石 ================================
    # ===============================================================================
    # 保存一下
    退出并保存()
    loopTimes = 0
    gems = list(gList[target.value-1].values())  # 原材料列表
    if len(gems) <= 2:
        toast("低品质原材料数量不足, 程序退出")
        return
    for i in range(0, len(gems)-2, 3):
        once = gems[i:i+3]
        _new = firstEmpty(isEmpty)
        page, row, col = pkgLocation(_new)

        while True:
            进入宝石强化界面()
            选择宝石配方(target)
            添加宝石原料并合成(once)
            loopTimes += 1
            # 查看合成结果
            pClick(v[f"背包页{page}"], before=min)
            pClick(v[f"背包格{row}{col}"], before=min, after=min)
            # 解析屏幕中的宝石信息
            try:
                level, data = parseGem(r["评级文本"], r["属性文本"])
            except GemOcrError:
                continue
            except GemParseError as e:
                print(str(e))
                continue
            # 合成产物品质检查
            g = Gem(_new, level, data)
            isGood = gf.check(g)
            toast(f"第 {loopTimes} 次: {g} {'出货!!!' if isGood else ''}")
            # 出货了就保存, 退出死循环
            if isGood:
                for item in once:
                    isEmpty[item.index] = int(True)
                    del gList[item.level.value][item.index]
                isEmpty[_new] = int(False)
                退出并保存()
                break
            # 不然就 SL重来
            退出并重新登录()
