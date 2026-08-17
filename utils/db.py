import os

from ascript.android.system import R

from .auto import Point, Rect, getResolution, toast

# 手动路径, 与自更新环境隔离, 避免重复运行导致的缓存被覆盖
# RootDir = R.sd("/AScript/inotia4/")
# 自动路径, 工程在安卓机上所在的位置, 每次运行都会被刷新
RootDir = R.sd("/airscript/model/inotia4/res")

# 默认设备分辨率 (用于坐标采集的基准设备)
DEFAULT_HEIGHT = 1200
DEFAULT_WIDTH = 2608

# 全局坐标缓存: v 存储 point, r 存储 rect
v = {}  # {name: Point}
r = {}  # {name: Rect}

# 当前设备的缩放比例
_scale_x = 1.0
_scale_y = 1.0


def init_db():
    """初始化数据库: 加载所有坐标并根据当前设备分辨率进行缩放"""
    global _scale_x, _scale_y

    # 获取当前设备分辨率
    width, height = getResolution()

    # 计算缩放比例
    _scale_x = width / DEFAULT_WIDTH
    _scale_y = height / DEFAULT_HEIGHT

    print(f"[DB] 默认分辨率: {DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
    print(f"[DB] 当前分辨率: {width}x{height}")
    print(f"[DB] 缩放比例: x={_scale_x:.4f}, y={_scale_y:.4f}")

    # 加载所有 point 文件
    point_dir = os.path.join(RootDir, "point")
    if os.path.exists(point_dir):
        for name in os.listdir(point_dir):
            filepath = os.path.join(point_dir, name)
            if os.path.isfile(filepath):
                try:
                    with open(filepath, "r") as f:
                        p = Point.from_str(f.read())
                        v[name] = _scale_point(p)
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
                        r[name] = _scale_rect(rect)
                except Exception as e:
                    print(f"[DB] 加载 rect '{name}' 失败: {e}")

    print(f"[DB] 已加载 {len(v)} 个 point, {len(r)} 个 rect")


def _scale_point(p: Point) -> Point:
    """缩放 Point 坐标"""
    return Point(round(p.x * _scale_x), round(p.y * _scale_y))


def _scale_rect(rect: Rect) -> Rect:
    """缩放 Rect 坐标"""
    return Rect(
        round(rect.x1 * _scale_x),
        round(rect.y1 * _scale_y),
        round(rect.x2 * _scale_x),
        round(rect.y2 * _scale_y)
    )


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
