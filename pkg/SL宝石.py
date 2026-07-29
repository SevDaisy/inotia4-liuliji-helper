from ..utils.constrants import imgFind, pClick, pSlide, toast
from ..utils.db import loadPoint


# saveIndex: 第几个存档
# target: 融合到几级宝石：[中级|高级|顶级|混沌]
def SL宝石(saveIndex=1, level=0):
    short = 200
    long = 700
    v = {}
    for item in [
        # 退出重进
            "菜单", "上一级", "主菜单页", "主菜单选项", "返回主菜单-是", "开始游戏", "跳过登录-否", f"存档{saveIndex}",
        # 去融合
            "平A", "融合器-宝石强化", "宝石配方选择", "宝石配方中级", "宝石配方高级", "宝石配方顶级", "宝石配方混沌",
            "宝石材料位1", "宝石材料位2", "宝石材料位3", "宝石材料添加", "融合器-确认融合", "融合器-确认融合-是", "融合器-融合成功-确认",
        # 辅助按键
            "背包页1", "背包页2", "背包页3", "背包页4", "背包页5",
        # 保存
            "马上存档", "马上存档-确认"
    ]:
        v[item] = loadPoint(item)
    for k, p in v.items():
        # print(f"{k}: {"Not found" if p is None else str(p)}")
        if p is None:
            toast("有坐标没取到，程序退出")
            return

    def 重新登录():
        # 点击 主菜单页
        pClick(v["主菜单页"], before=long, msg="打开主菜单页")
        # 点击 主菜单选项
        pClick(v["主菜单选项"], before=short, msg="点击主菜单选项")
        # 点击 是 (返回主菜单-是)
        pClick(v["返回主菜单-是"], before=short, msg="点击返回主菜单-是")
        # 点击 开始游戏
        pClick(v["开始游戏"], before=long, msg="点击开始游戏")
        # 点击 否 (跳过登录-否)
        pClick(v["跳过登录-否"], before=short, msg="点击跳过登录-否")
        # 点击 存档{saveIndex}
        pClick(v[f"存档{saveIndex}"], before=long, msg=f"点击存档{saveIndex}")
        # 点击 菜单
        pClick(v["菜单"], before=long, msg="打开菜单")

    def 打开背包():
        # 点击 背包菜单
        pClick(v["背包菜单"], before=short, msg="打开背包")
        # 点击 背包页{packIndex}
        if 1 < packIndex < 5:
            pClick(v[f"背包页{packIndex}"], before=short, msg=f"打开第{packIndex}背包")

    def 确认并保存():
        # 点击 强化成功
        pClick(v["强化成功"])
        # 点击 主菜单页
        pClick(v["主菜单页"], before=short, msg="打开主菜单")
        # 点击 保存选项
        pClick(v["保存选项"], before=short, msg="点击保存")
        # 点击 确认保存
        pClick(v["确认保存"], before=short, msg="点击确认保存")

    cnt = 0
    success = 0
    while maxRetry <= 0 or cnt < maxRetry:
        while success < maxSuccess:
            pSlide(v["背包格21"], v["背包格22"], before=short)
            confirm = imgFind("确认", before=long)
            # 没强化成功, 则重新登录再来
            if confirm is None:
                toast("下次一定", duration=1000)
                break
            success += 1
            toast(f"失败 {cnt} 次, 成功 {success} 次")
            确认并保存()
            打开背包()
        # 强化满了 退出
        if success >= maxSuccess:
            break
        cnt += 1
        toast(f"失败 {cnt} 次, 成功 {success} 次")
        重新登录()
        打开背包()

    pClick(v["背包格22"], before=short, msg="打开背包")
