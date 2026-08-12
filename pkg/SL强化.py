from ..utils.auto import imgFind, ocrPaddle_V5, pClick, pSlide, toast, pin, ocrGet
from ..utils.db import loadPoint, loadRect


def SL强化(saveIndex=1, packIndex=1, maxRetry=0, maxSuccess=15, mode="Normal"):
    """
    # saveIndex: 第几个存档
    # packIndex: 第几个背包
    # maxSuccess: 强化成功几次
    # mode: Normal 正常强化
    #   else: 作为 PositionID 合法值 00、01、02、10、11、12...33, 指定混沌强化卷轴的位置
    """
    min = 100
    short = 200
    long = 700
    v = {}
    r = {}
    r["评级文本"] = loadRect("背包-装备评级文本")
    for item in [
        "主菜单页", "主菜单选项", "返回主菜单-是", "开始游戏", "跳过登录-否", f"存档{saveIndex}",
        "菜单", "背包菜单", f"背包页{packIndex}",
        "背包格00", "背包格01", "背包格02", "背包格03",
        "背包格10", "背包格11", "背包格12", "背包格13",
        "背包格20", "背包格21", "背包格22", "背包格23",
        "背包格30", "背包格31", "背包格32", "背包格33",
        "强化成功", "主菜单页", "保存选项", "确认保存"
    ]:
        v[item] = loadPoint(item)
    for k, p in v.items():
        if p is None:
            toast(f"坐标 {k} 没取到，程序退出")
            return

    def 重新登录并打开菜单():
        pClick(v["主菜单页"], before=long)
        pClick(v["主菜单选项"], before=short)
        pClick(v["返回主菜单-是"], before=short)
        pClick(v["开始游戏"], before=long)
        pClick(v["跳过登录-否"], before=short)
        pClick(v[f"存档{saveIndex}"], before=long)
        pClick(v["菜单"], before=long)

    def 打开背包():
        pClick(v["背包菜单"], before=short, msg="打开背包")
        # 点击 背包页{packIndex}
        if 1 < packIndex < 5:
            pClick(v[f"背包页{packIndex}"], before=short)

    def 保存():
        pClick(v["主菜单页"], before=short)
        pClick(v["保存选项"], before=short)
        pClick(v["确认保存"], before=short)

    def 识别当前装备等级() -> int:
        pClick(v["背包格12"], before=short, after=min)
        img评级 = pin(rect=r["评级文本"])
        txt = ocrPaddle_V5(img=img评级)
        if not (txt and len(txt) > 0):
            toast("未识别到装备评级文本")
            return -1
        split = txt[0].split("+")
        if len(split) != 2:
            toast(f"异常文本：{txt[0]}")
            return -1
        return int(split[1])

    # 无误触风险, 无需判断背包是否已经打开
    pClick(v["菜单"], before=min)
    打开背包()

    if mode == "Normal":
        # 普通强化
        cnt = 0
        success = 0
        while maxRetry <= 0 or cnt < maxRetry:
            while success < maxSuccess:
                pSlide(v["背包格11"], v["背包格12"], before=short)
                confirm = imgFind("确认", before=long)
                # 没强化成功, 则重新登录再来
                if confirm is None:
                    # toast("下次一定", duration=1000)
                    break
                success += 1
                pClick(v["强化成功"])
                toast(f"失败 {cnt} 次, 成功 {success} 次")
                保存()
                打开背包()
            # 强化满了 退出
            if success >= maxSuccess:
                break
            cnt += 1
            toast(f"失败 {cnt} 次, 成功 {success} 次")
            重新登录并打开菜单()
            打开背包()

        pClick(v["背包格12"], before=short)
    else:
        # 混沌卷轴强化
        posID = 11
        try:
            posID = int(mode)
        except ValueError:
            toast("非法 mode 值, 混沌卷轴位置使用默认值 11")
        finally:
            if posID == 12:
                toast("不行哦, 这个是放装备的位置")
                return

        cnt = 0
        lv = 识别当前装备等级()
        if lv < 0:
            return

        # 先强化到奇数
        if lv % 2 == 0:
            while True:
                cnt += 1
                pSlide(v[f"背包格{posID:02d}"], v["背包格12"], before=short)
                lv = 识别当前装备等级()
                if imgFind("确认", before=short):
                    pClick(v["强化成功"])
                toast(f"A 强化 {cnt} 次, 当前等级: +{lv}")
                if lv < 0 or lv % 2 == 0:
                    重新登录并打开菜单()
                    打开背包()
                else:
                    保存()
                    break

        # 一直强化到 +31
        oldLv = lv
        while oldLv < 31:
            打开背包()

            # 强化 1 次
            cnt += 1
            pSlide(v[f"背包格{posID:02d}"], v["背包格12"], before=short)
            lv = 识别当前装备等级()
            toast(f"B 强化 {cnt} 次, 当前等级: +{lv}")

            # 成功 强化+2, 处理一下确认
            if imgFind("确认", before=short):
                pClick(v["强化成功"], msg="+2 保存一下")

            # 有进步就保存
            if oldLv < lv:
                保存()
                oldLv = lv
                continue
            # SL 重来
            重新登录并打开菜单()
