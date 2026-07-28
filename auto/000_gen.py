#!/usr/bin/env python3

import json
import os
import sys

# adb shell dumpsys package com.zidongdianji | grep versionName
# 适配自动点击器版本 2.0.12.31
FILE_EXT = '.accs'
# 获取当前 .py 文件所在目录
currentDir = os.path.dirname(os.path.abspath(__file__))


def parse(content: str):
    """
    解析自动点击器导出文件，（外层 JSON），提取 configList[0].config，
    并将其作为 JSON 字符串解析为 Python 对象（通常是一个列表）。
    """
    outer_data = json.loads(content)
    # 假设 configList 至少有一个元素，取第一个
    config_str = outer_data['configList'][0]['config']
    inner_data = json.loads(config_str)
    return {"actions": inner_data, "preset": {
        "delay": outer_data['configList'][0]['interval'],
        "clickDur": outer_data['configList'][0]['touchDuration'],
        "slideDur": outer_data['configList'][0]['swipeDuration'],
    }}


def readFiles():
    res = {}
    # 遍历目录下所有自动点击器导出文件
    for filename in os.listdir(currentDir):
        if filename.endswith(FILE_EXT):
            filepath = os.path.join(currentDir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                parsed = parse(content)
                res[filename.removesuffix(FILE_EXT)] = parsed
                # print(f"文件 {filename} 解析成功，提取到 {len(parsed)} 个动作")
                # 可根据需要进一步处理 parsed
            except Exception as e:
                print(f"解析文件 {filename} 时出错: {e}")
    return res


def writeFile(fileName, content):
    with open(fileName, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Generated: {fileName}")


def generate(library: dict, target: str):
    target = target.removesuffix(FILE_EXT)
    data = library.get(target)
    if data is None:
        print(f"{target} Not Found")

    writeFile(
        os.path.join(currentDir, f"{target}.json"),
        str(data).replace('\'', '\"'),
    )

    preset = data['preset']
    res = ['from .constrants import *\n\n']
    for _, act in enumerate(data['actions']):
        delay = preset['delay'] if act['delay'] <= 0 else act['delay']
        dur = act['duration']
        match act['type']:
            case 0:
                # 点击
                pt = act['point']
                res.append(
                    f"doClick({pt['x']}, {pt['y']}, before={delay}, dur={preset['clickDur'] if dur <= 10 else dur})"
                )
            case 1:
                # 滑动
                start = act['swipeCombData']['mStartPoint']
                end = act['swipeCombData']['mEndPoint']
                res.append(
                    f"doSlide({start['x']}, {start['y']}, {end['x']}, {end['y']}, before={delay}, dur={preset['slideDur'] if dur <= 300 else dur})"
                )
            case _:
                print(f"Unknown TypeID({act['type']}), not supported")

    writeFile(
        os.path.join(currentDir, f"{target}.py"),
        '\n'.join(res)+'\n',
    )
    return


if __name__ == '__main__':
    generate(readFiles(), sys.argv[1])
    # generate(readFiles(), "拔剑刷钱")
    # generate(readFiles(), "Rule 8")
