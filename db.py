from ascript.android.system import R

import os

from .constrants import Point, imgFind, imgFindAll, toast

RootDir = R.sd("/AScript/inotia4/")


def save(name, value, prefix=""):
    targetFile = os.path.join(RootDir, prefix, name)
    with open(targetFile, "w") as f:
        f.write(str(value))
    toast(f"Stored: {targetFile}", duration=3000)


def loadPoint(name):
    targetFile = os.path.join(RootDir, "point", name)
    if os.path.exists(targetFile):
        with open(targetFile, "r") as f:
            return Point.from_str(f.read())
    else:
        return None


DataList = [
    # 游戏内直接可见
    "平A", "菜单",
    # 菜单页可见
    "背包菜单", "主菜单页", "上一级",
    # 背包页可见, 左上00, 右上40, 右下33
    "背包页1", "背包页2", "背包页3", "背包页4", "背包页5",
    "背包格11", "背包格21",
    # 主菜单页可见
    "保存选项", "主菜单选项",
    # 条件可见
    "强化成功", "确认保存", "返回主菜单-是", "返回主菜单-否", "跳过登录-是", "跳过登录-否",
    # 开屏界面 (Ocr.mlkitocr_v2(pattern=r"开始游戏"))
    "开始游戏",
    # 存档选择页 (存档槽 相似度0.4可取三个)
    "存档1", "存档2", "存档3",
]


# 此函数已弃用。转人工处理，详见 init.py
def Initialize(name):
    res = None
    if name == "强化成功":
        res = imgFind("确认")
    elif name in ["平A", "菜单", "背包菜单", "主菜单页", "上一级", "确认保存"]:
        res = imgFind(name)
    if res is not None:
        save(name, res, prefix="point")
        return
    if name == "背包分格":
        # res = imgFindAll("背包页")
        # for i, p in enumerate(res):
        #     save(f"背包页{i+1}", p, prefix="point")
        res = imgFindAll("背包分格")
        res.sort(key=lambda p: (p.x, p.y))

        def avg(a, b):
            return int((a+b)/2)
        s04 = Point(avg(res[0].x, res[4].x), avg(res[0].y, res[4].y))
        s46 = Point(avg(res[4].x, res[6].x), avg(res[4].y, res[6].y))
        save("背包分格21", s04, prefix="point")
        save("背包分格22", s46, prefix="point")
