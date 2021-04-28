import os
from util import fileio

def getLayouts():
    if os.path.exists("layouts"):
        layoutFiles = [f[:-5] for f in os.listdir("layouts")]
        layoutFiles.insert(0,"System Default")
    else:
        layoutFiles = ["System Default"]
    return layoutFiles

def resolveLayout(name):
    if name == "System Default":
        return fileio.readJson("defaults/layout.json")
    return fileio.readJson("layouts/"+name+".json")
