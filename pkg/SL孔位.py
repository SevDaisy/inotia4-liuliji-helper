from xml.etree.ElementTree import tostring

from ..utils.auto import imgFind, ocrFind, ocrGet, ocrPaddle_V5, pClick, pin, toast
from ..utils.db import loadPoint, loadRect
from ..utils.model import *


def SL孔位(saveIndex=1, packIndex=1, posID="00", is可强化装备=True):
    """
    saveIndex: 游戏的第几个存档位
    """

    min = 100
    short = 200
    long = 700
    v = {}
    r = {}
    r["孔位数量"] = loadRect("融合器-强化孔位数量" if is可强化装备 else "融合器-饰品孔位数量")
    r["添加按钮"] = loadRect("融合器-添加按钮")
    for item in [
        # 退出重进
            "菜单", "上一级", "主菜单页", "主菜单选项", "返回主菜单-是", "开始游戏", "跳过登录-否", f"存档{saveIndex}",
        # 去融合
            "平A", "融合器-道具合成", "融合器-宝石孔生成", "宝石材料添加", "融合器-确认融合", "融合器-确认融合-是", "融合器-融合成功-确认",
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
        pClick(v[f"存档{saveIndex}"], before=long, after=long)

    def 退出并保存():
        pClick(v["上一级"], before=short)
        pClick(v["上一级"], before=short)
        pClick(v["马上存档"], before=short)
        pClick(v["马上存档-确认"], before=short)

    def 进入宝石孔生成界面():
        pClick(v["平A"], before=short)
        if ocrFind("宝石") is None:
            pClick(v["融合器-道具合成"], before=min)
        pClick(v["融合器-宝石孔生成"], before=short)

    cnt = 0
    while True:
        cnt += 1
        进入宝石孔生成界面()

        # 打孔
        for x in [
            f"背包页{packIndex}",
            "背包格00",
            "宝石材料添加",
            "融合器-确认融合",
            "融合器-确认融合-是",
            "融合器-融合成功-确认",
            f"背包格{posID}",
        ]:
            pClick(v[x], before=short, after=short)

        # 检查结果
        txt = ocrPaddle_V5(img=pin(r["孔位数量"]))
        res = 0
        if txt and len(txt) > 0:
            try:
                res = int(txt[0][-1])
                toast(f"第{cnt}次, 孔位: {res}")
            except ValueError:
                toast(f"异常文本: {txt[0]}")
        else:
            toast("异常: 无法识别孔位数量")
        if res == 4:
            退出并保存()
            break

        # SL重来
        退出并重新登录()
