import os

from ascript.android.system import R

from .auto import Point, Rect, getResolution, toast

# 手动路径, 与自更新环境隔离, 避免重复运行导致的缓存被覆盖
# RootDir = R.sd("/AScript/inotia4/")
# 自动路径, 工程在安卓机上所在的位置, 每次运行都会被刷新
RootDir = R.sd("/airscript/model/inotia4/res")

# 全局坐标缓存: v 存储 point, r 存储 rect
v = {}  # {name: Point}
r = {}  # {name: Rect}


def init_db():
    """初始化数据库: 加载所有坐标"""

    # 获取当前设备分辨率
    width, height = getResolution()

    print(f"[DB] 当前分辨率: {width}x{height}")

    # 加载所有 point 文件
    point_dir = os.path.join(RootDir, "point")
    if os.path.exists(point_dir):
        for name in os.listdir(point_dir):
            filepath = os.path.join(point_dir, name)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "r") as f:
                        p = Point.from_str(f.read())
                        v[name] = p
                except Exception as e:
                    print(f"[DB] 加载 point '{name}' 失败: {e}")

    # 加载所有 rect 文件
    rect_dir = os.path.join(RootDir, "rect")
    if os.path.exists(rect_dir):
        for name in os.listdir(rect_dir):
            filepath = os.path.join(rect_dir, name)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "r") as f:
                        rect = Rect.from_str(f.read())
                        r[name] = rect
                except Exception as e:
                    print(f"[DB] 加载 rect '{name}' 失败: {e}")

    print(f"[DB] 已加载 {len(v)} 个 point, {len(r)} 个 rect")


def save(name, value, prefix=""):
    targetFile = os.path.join(RootDir, prefix, name)
    with open(targetFile, "w") as f:
        f.write(str(value))
    toast(f"Stored: {targetFile}", duration=3000)


def loadPoint(name):
    """从缓存中获取 Point, 不存在则返回 None"""
    return v.get(name)


def loadRect(name):
    """从缓存中获取 Rect, 不存在则返回 None"""
    return r.get(name)
