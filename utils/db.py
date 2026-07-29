import os

from ascript.android.system import R

from .constrants import Point, Rect, imgFind, imgFindAll, toast

# 手动路径, 与自更新环境隔离, 避免重复运行导致的缓存被覆盖
# RootDir = R.sd("/AScript/inotia4/")
# 自动路径, 工程在安卓机上所在的位置, 每次运行都会被刷新
RootDir = R.sd("/airscript/model/inotia4/res")


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


def loadRect(name):
    targetFile = os.path.join(RootDir, "rect", name)
    if os.path.exists(targetFile):
        with open(targetFile, "r") as f:
            return Rect.from_str(f.read())
    else:
        return None
