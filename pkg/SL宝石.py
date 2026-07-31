from ..utils.auto import ocrGet, pClick, pSlide, pin, toast
from ..utils.db import loadPoint, loadRect
from ..utils.model import Gem, GemLevel


# saveIndex: 第几个存档
# target: 融合到几级宝石：[中级|高级|顶级|混沌]
def SL宝石(saveIndex=1, target=GemLevel.混沌):
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
            "平A", "融合器-宝石强化", "宝石配方选择", "宝石配方中级", "宝石配方高级", "宝石配方顶级", "宝石配方混沌",
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
        pClick(v["融合器-宝石强化"], before=short, msg="打开宝石强化界面")

    # 进入宝石强化界面()

    # 整理背包, 录入当前已有宝石
    gList = []
    record = [False] * 80
    i = 0
    cnt = 0
    for page in range(4, 5):
        pClick(v[f"背包页{page+1}"], before=short, msg=f"打开背包页 {page+1}")
        for row in range(4):
            for col in range(4):
                i += 1
                pClick(v[f"背包格{row}{col}"], before=min, after=min)
                img评级 = pin(rect=r["评级文本"])
                img属性 = pin(rect=r["属性文本"])
                txt = ocrGet(img=img评级)
                level = None
                if txt is not None and " ".join(txt).endswith("宝石"):
                    level = GemLevel.from_str(" ".join(txt)[:-2])
                if level is None:
                    continue
                txt = ocrGet(img=img属性)
                if txt is None:
                    toast("异常! 没读到宝石属性")
                    continue
                cnt += 1
                gList.append(Gem(i-1, level, Gem.Data(" ".join(txt))))
                toast(f"第 {cnt} 颗, {gList[cnt-1]}")
