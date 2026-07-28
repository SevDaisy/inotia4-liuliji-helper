# from esp32 import BleDevice
from ascript.android import screen
from ascript.android.action import click, slide, Touch, gesture
# 导入控件检索相关
from ascript.android.node import Selector
# 导入图色相关
from ascript.android.screen import capture, FindColors, FindImages, Ocr
# 导入系统相关
from ascript.android import system
# 环境设备相关
from ascript.android.system import R, Device
# 模拟动作相关
from ascript.android import action
# 对话框
from ascript.android.ui import Dialog


import time
import sys

# 全局变量声明
cx = 'center_x'
cy = 'center_y'
MilliSeconds = 0.001


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"


def with_delay(func):
    """装饰器：在执行核心操作前后插入延迟"""
    def wrapper(*args, before=0, after=0, msg="", ** kwargs):
        if before > 0:
            # print(f"执行前等待 {before} 毫秒")
            time.sleep(before*MilliSeconds)
        # result = ""
        result = func(*args, **kwargs)
        msg = f"->{str(args)} {str(kwargs)}" if msg == "" else msg
        Dialog.toast(msg, dur=1000)
        print(msg)
        if after > 0:
            # print(f"执行前等待 {after} 毫秒")
            time.sleep(after*MilliSeconds)
        return result
    return wrapper


def pin(debug=False):
    now = screen.capture()
    screen.bitmap_to_file(R.sd("1.png"), now)
    if debug:
        print(now)
    return now


def toast(msg, duration=1000):
    Dialog.toast(msg, duration)


def exit(code=0):
    sys.exit(code)


@with_delay
def ocrFind(txt: str, img=None, debug=False):
    """
    在屏幕上查找文字，返回第一个匹配结果。
    :param txt: 指定查找文本, img: 传入源图, None=自动截屏
    :return: dict {text, rect, center_x, center_y, confidence} 或 None
    """

    if img is None:
        img = pin()
    res = Ocr.find(text=txt, image=img)
    return None if res is None else Point(res[cx], res[cy])


@with_delay
def imgFind(part, full=None):
    if full is None:
        full = pin()
    res = FindImages.find_template(R.img(f"{part}.png"))
    return None if res is None else Point(res[cx], res[cy])


@with_delay
def doClick(x, y, dur=20):
    return action.click(x, y, dur)


@with_delay
def doSlide(x1, y1, x2, y2, dur=300):
    return action.slide(x1, y1, x2, y2, dur)


@with_delay
def pClick(p: Point, dur=20):
    return action.click(p.x, p.y, dur)


@with_delay
def pSlide(start: Point, end: Point, dur=300):
    return action.slide(start.x, start.y, end.x, end.y, dur)
