import os

from .db import Initialize, loadPoint, RootDir
from .constrants import *


# for x in ["背包分格"]:
#     Initialize(x)

# dd = os.listdir(os.path.join(RootDir, "point"))

# print(f"已保存：{str(len(dd))} {' '.join(dd)}")

# b = []
# for i in range(1, 6):
#     b.append(loadPoint(f"背包页{i}"))
s = []
s.append(loadPoint("背包分格21"))
s.append(loadPoint("背包分格22"))

print(s)
pSlide(s[0], s[1])
