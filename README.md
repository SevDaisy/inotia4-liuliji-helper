# Inotia 4 盗版大修版 AScript 自动化辅助

基于 [AScript](https://ascript.cn/docs/android/intro) 框架的《艾诺迪亚 4》自动化辅助工具，利用游戏的存档/读档（SL）机制实现装备强化、宝石合成、宝石开孔等重复性任务的自动化刷取。

## 功能

| 模块 | 说明 |
| ------ | ------ |
| **SL 强化** | 自动装备强化，支持普通强化和混沌强化（+31），失败时回档重试 |
| **SL 宝石** | 自动宝石合成与筛选，支持低→中→高→顶→混沌逐级合成，按属性阈值过滤保留/合成 |
| **SL 孔位** | 自动装备开孔（融合器），SL 刷取 4 孔结果，支持武器/防具和饰品 |

## 环境要求

- Android 手机（无需 root，但需要开启无障碍服务）
- [AScript APK](https://ascript.cn/download/android/)（已授权屏幕录制、无障碍辅助）
- PC 端浏览器（访问 `http://<手机IP>:9096/` 进行开发调试）
- PaddleOCR V5 插件（AScript 内加载）

### 【可选】 ADB 权限配置

永久授予屏幕录制权限，手机重启前有效。避免每次共享屏幕都要弹窗

```bash
# 授予 AScript 屏幕录制权限
adb shell appops set com.aojoy.airscript PROJECT_MEDIA allow
```

## 项目结构

```
inotia4/
├── __init__.py            # 入口：加载 PaddleOCR 插件，触发 main
├── main.py                # 主脚本：定义宝石过滤器，调用各自动化模块
├── build.as               # AScript 项目配置（pip 依赖）
│
├── pkg/                   # 核心自动化逻辑
│   ├── SL强化.py          # 装备强化 SL 自动化
│   ├── SL宝石.py          # 宝石合成筛选 SL 自动化
│   └── SL孔位.py          # 宝石开孔 SL 自动化
│
├── utils/                 # 工具模块
│   ├── auto.py            # 屏幕交互：OCR、图像匹配、点击/滑动、Canvas 绘制
│   ├── db.py              # 坐标数据库：加载 point/rect 文件
│   └── model.py           # 数据模型：GemLevel、Gem、GemFilter、Entry
│
├── auto/                  # 第三方自动点击器脚本（从 .accs 文件生成）
│   └── 000_gen.py         # .accs → Python 脚本转换器
│
├── res/                   # 资源文件（同步至手机）
│   ├── point/             # 坐标点数据文件（每个文件一个坐标）
│   ├── rect/              # 矩形区域数据文件
│   ├── img/               # 图像匹配模板（PNG）
│   ├── point.sh           # 坐标点定义脚本
│   ├── rect.sh            # 矩形区域定义脚本
│   └── hack.sh            # 重新生成坐标数据文件
│
└── docs/
    └── 工作记录.md         # 开发笔记（API 文档、环境配置、地图 ID）
```

## 快速开始

1. 手机安装 AScript APK 并完成权限配置（参见上方 ADB 命令）
2. PC 浏览器打开 `http://<手机IP>:9096/`
3. 在 AScript IDE 中打开本项目，确保文件已同步至手机
4. 运行脚本

## 配置宝石过滤器

在 `main.py` 中定义 `GemFilter`，指定保留的属性及最低阈值：

```python
gf = GemFilter([
    Entry.from_str("暴击率: 9%"),        # 暴击率 ≥ 9%
    Entry.from_str("暴击伤害增加率: 16.5%"), # 暴伤 ≥ 16.5%
    Entry.from_str("回避率: 4.5%"),       # 闪避 ≥ 4.5%
])
```

宝石等级：`低级` → `中级` → `高级` → `顶级` → `混沌`，合成规则为 3 颗同级合 1 颗高一级。

支持 36 种属性，包括：力量、敏捷、体力、智力、暴击率、暴击伤害增加率、回避率、HP 吸收、MP 增加/恢复、各种元素抗性等（详见 [utils/model.py](utils/model.py)）。

## 坐标标定

坐标数据存储在 `res/point/` 和 `res/rect/` 目录中。修改坐标后重新生成：

```bash
cd res
./hack.sh          # Linux / Git Bash
hack.bat           # Windows
```

或右键运行 `res/右键使用 powershell 运行.ps1`。

## 相关资源

- AScript 文档：<https://ascript.cn/docs/android/intro>
- AScript 下载：<https://ascript.cn/download/android/>
- ESP32 HID 固件：<https://ascript.cn/hid>
- ESP32 HID API：<http://dev.airscript.cn/docs/android/esp32>

## 地图 ID 参考

> 规则：左+1 右-1 上+10 下-10

| 地图 | ID |
| ------ | ----- |
| 记忆一层 | 364 |
| 记忆二层 | 375 |
| 记忆三层 | 386 |
| 记忆四层 | 396 |
| 记忆末层 | 406 |
