from .constrants import *

# res = FindImages.find_template(R.img(f"{part}.png"))


pBack = imgFind("上一级")
if pBack is None:
    toast("找不到 上一级")
    # exit()

pClick(pBack)
