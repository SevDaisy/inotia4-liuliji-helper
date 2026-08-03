import sys
import time

import cv2
from ascript.android import action, screen
from ascript.android.screen import FindImages, Ocr
from ascript.android.system import Device, R
from ascript.android.ui import Dialog
import PaddleOcrV5

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
    """装饰器：在执行核心操作前后插入延迟, 并支持日志和弹窗"""
    def wrapper(*args, before=0, after=0, msg="", ** kwargs):
        if msg == "":
            print("\t"*8 + f"{func.__name__}({str(args)},{str(kwargs)})")
        else:
            toast(msg, duration=1000)
        if before > 0:
            time.sleep(before*MilliSeconds)
        result = func(*args, **kwargs)
        if after > 0:
            time.sleep(after*MilliSeconds)
        return result
    return wrapper


def pin(rect=None):
    now = None
    if rect is None:
        now = screen.capture()
    else:
        now = screen.capture(rect.x1, rect.y1, rect.x2, rect.y2)
    return now


def pinGray(rect=None):
    now = None
    if rect is None:
        now = screen.capture_cv()
    else:
        now = screen.capture_cv(rect.x1, rect.y1, rect.x2, rect.y2)
    return cv2.cvtColor(now, cv2.COLOR_BGR2GRAY)


def toast(msg, duration=1000):
    Dialog.toast(msg, duration)
    print(msg)


def exit(code=0):
    sys.exit(code)


@with_delay
def ocrGet(rect=None, img=None):
    res = None
    if img is None:
        img = pin()
    if rect is None:
        res = Ocr.mlkitocr_v2(image=img)
    else:
        res = Ocr.mlkitocr_v2(image=img, rect=rect.asList())
    return None if res is None else [x.text for x in res]


@with_delay
def ocrPaddle_V5(rect=None, img=None):
    if img is None:
        img = pin()
    if rect is None:
        res = PaddleOcrV5.detect(image=img)
    else:
        res = PaddleOcrV5.detect(image=img, rect=rect.asList())
        print(res)
    return None if res is None else [x['text'] for x in res]


@with_delay
def ocrFind(pattern: str, img=None):
    """ 模式匹配，返回匹配到的中心位置 """
    if img is None:
        img = pin()
    res = Ocr.mlkitocr_v2(pattern=pattern, image=img)
    res = None if res is None else [
        Point(item.center_x, item.center_y) for item in res].sort()
    return res


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
    return None if res is None else [Point(item[cx], item[cy]) for item in res].sort()


@with_delay
def imgFindGray(part, rect, full=None):
    if full is None:
        full = pinGray()
    res = FindImages.find_all_template(
        R.img(f"{part}.png"),
        rect=rect,
        confidence=0.8, image=full)
    return None if res is None else [Point(item[cx], item[cy]) for item in res].sort()


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
