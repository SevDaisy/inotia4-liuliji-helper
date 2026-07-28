from ascript.android.system import R

import os

from .constrants import Point, imgFind, toast

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
    "背包菜单", "主菜单",
    # 背包页可见, 左上00, 右上04, 右下33
    "背包分格"
    "背包页1", "背包页2", "背包页3", "背包页4", "背包页5",
    "背包格11", "背包格21"
    # 条件可见
    "强化成功"
]


def Initialize(name):
    if name == "强化成功":
        res = imgFind("确认")
        if res is not None:
            save("强化成功", res, "point")
