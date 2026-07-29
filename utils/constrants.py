
import sys
import time

import cv2
from ascript.android import action, screen, system
from ascript.android.action import Touch, click, gesture, slide
from ascript.android.node import Selector
from ascript.android.screen import FindColors, FindImages, Ocr, capture
from ascript.android.system import Device, R
from ascript.android.ui import Dialog

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

    @classmethod
    def from_str(cls, s: str):
        s = s.strip('()').replace(" ", "")
        x_str, y_str = s.split(',')
        return cls(int(x_str.strip()), int(y_str.strip()))

    def __lt__(self, other):
        if self.y != other.y:
            return self.y < other.y
        return self.x < other.x


class Rect:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return f"({self.x1},{self.y1},{self.x2},{self.y2})"

    def __repr__(self):
        return f"({self.x1},{self.y1},{self.x2},{self.y2})"

    @classmethod
    def from_str(cls, s: str):
        s = s.strip('()').replace(" ", "")
        x1_str, y1_str, x2_str, y2_str = s.split(',')
        return cls(int(x1_str.strip()), int(y1_str.strip()), int(x2_str.strip()), int(y2_str.strip()))

    def center(self):
        return Point(int((self.x1 + self.x2) / 2), int((self.y1 + self.y2) / 2))

    def asList(self):
        return [self.x1, self.y1, self.x2, self.y2]


def with_delay(func):
    """装饰器：在执行核心操作前后插入延迟"""
    def wrapper(*args, before=0, after=0, msg="", ** kwargs):
        if msg == "":
            print(f"{func.__name__}({str(args)},{str(kwargs)})")
        else:
            toast(msg, duration=1000)
        if before > 0:
            # print(f"执行前等待 {before} 毫秒")
            time.sleep(before*MilliSeconds)
        # result = ""
        result = func(*args, **kwargs)
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
    print(msg)


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
    res = Ocr.mlkitocr_v2(pattern=txt, image=img)
    return None if res is None else Point(res[cx], res[cy])


@with_delay
def imgFind(part, full=None):
    if full is None:
        full = pin()
    res = FindImages.find_template(R.img(f"{part}.png"))
    return None if res is None else Point(res[cx], res[cy])


@with_delay
def imgFindAll(part, full=None):
    if full is None:
        full = pin()
    res = FindImages.find_all_template(R.img(f"{part}.png"))
    return None if res is None else [Point(item[cx], item[cy]) for item in res]


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


def test():
    img = screen.capture_cv()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    res = FindImages.find_all_template(
        R.img("高级宝石灰.png"),
        rect=[1390, 246, 2193, 1007],
        confidence=0.8, image=img)

    if res is None:
        print("未找到")
        return
    px = []
    for i, item in enumerate(res):
        # print(f"{i}: {Point(item[cx], item[cy])}")
        px.append(Point(item[cx], item[cy]))

    px.sort()
    i = 0
    for p in px:
        pClick(p, 500, msg=f"{i}: {p}")
        i += 1
    pass
