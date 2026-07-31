# from .pkg.SL强化 import SL强化

# SL强化(saveIndex=1, packIndex=4, maxRetry=0, maxSuccess=12)


from .pkg.SL宝石 import SL宝石
from .utils.model import GemLevel

# print("main OK")

SL宝石(saveIndex=1, target=GemLevel.顶级)
