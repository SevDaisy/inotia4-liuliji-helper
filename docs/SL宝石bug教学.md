# Inotia 4 盗版大修版 AScript 自动化辅助
>
> 项目开源地址：<https://github.com/SevDaisy/inotia4-liuliji-helper/>

基于 [AScript](https://ascript.cn/docs/android/intro) 框架的《艾诺迪亚 4》自动化辅助工具，利用游戏的存档/读档（SL）机制实现装备强化、宝石合成、宝石开孔等重复性任务的自动化刷取。

## SL宝石 卡背包 自动刷新宝石属性

### 1. 安装 AScript

下载：[AScript.apk](https://ascript.cn/download/android/)，并安装。
启动后选择 ==无障碍模式==，并授予所需权限。
> 注意：共享屏幕时应选择 “整个屏幕”
>
### 2. 下载源代码并安装

下载本项目源代码 inotia4.zip (QQ群文件) ，安装至手机目录: /sdcard/airscript/model
![image.png](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820153147207.png)

### 3. 打开 Web IDE
>
> 注意：电脑与手机应连接同一 WiFi

打开 AScript APP, 在电脑上打开首页给出的网址
![image.png|300](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820153548744.png)
![image.png|300](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820153639178.png)

### 4. 从 Web IDE 打开图色助手

图色助手用于获取坐标点，也就是【标点】
![image.png|547](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820160834275.png)
![image.png|547](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820163053920.png)
顺便，如图所示，当合成出暴击率 ≥ 8.6% 的宝石时, 程序将会停下。
![image.png|546](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820154434918.png)

#### 4.1 标点 背包格00

![image.png](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820163315151.png)
鼠标放在背包格中第一个物品处，右键 - 复制坐标

![image.png](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820163534476.png)
回到 Web IDE, 打开文件 res/point/背包格00
将复制得到的坐标粘贴进括号里, 代替文件中本来的坐标

> 后续标点流程相同，不再赘述，只以==红点==形式给出标点需要复制的坐标位置
>
#### 4.2 标点 融合器-确认融合

![image.png|500](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820164045399.png)

#### 4.3 标点 融合器-确认融合-是

![image.png|500](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820164143436.png)

#### 4.4 标点 融合器-融合成功-确认

![image.png|500](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820164302884.png)

#### 4.5 标点 融合器-材料详情-关闭

![image.png|500](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820164409369.png)

#### 4.6 标点 融合器-宝石属性文本

![image.png|800](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820164952839.png)
左键按住，框选起宝石属性文本区域，复制右侧【搜索范围】中自动生成的坐标
![image.png](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820165323511.png)
回到 Web IDE, 打开文件 res/rect/融合器-宝石属性文本
将复制得到的坐标粘贴进括号里, 代替文件中本来的坐标

> 后续标点流程相同，不再赘述，只以==选框==形式给出标点需要复制的坐标位置
>
#### 4.7 标点 融合器-宝石评级文本

![image.png|500](https://image-1259572441.cos.ap-beijing.myqcloud.com/blog/20260820165735019.png)

### 5. 交互协议

卡背包刷宝石相关教学，详见 [B站视频 卡背包高级教程](https://www.bilibili.com/video/BV1x8411j7Wx?t=179.7)

#### 5.1 游戏界面需满足以下条件

1. 游戏处于融合器 - 宝石强化界面
2. 已选择好宝石配方，并完整添加了所需宝石
3. 已完成卡背包，且背包内第一格就是卡好的背包，也就是融合后得到的宝石。

#### 5.2 本脚本自动完成以下步骤

1. 点击【组合】按钮，发起一次合成
2. 点击【是】按钮，确认材料选择
3. 点击【确认】按钮，确认合成完毕
4. 点击【背包格00】，展开宝石详情
5. 自动截取【宝石评级文本】【宝石属性文本】区域图像，通过OCR得到文本信息。解析文本信息，得到宝石属性。
6. 如果当前宝石属性不满足要求，点击【×】按钮，关闭宝石详情，并回到第一步继续执行

！！！如果当前宝石属性满足 main.py 中的要求，脚本停止运行，请及时手动保存。！！！

！！！脚本停止运行后，AScript 并不会退出，需要手动退出。否则 AScript 会持续工作、发热 ！！！
