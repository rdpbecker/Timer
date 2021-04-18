import os
from util import fileio

validHotkeys = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m',\
    'n','o','p','q','r','s','t','u','v','w','x','y','z',\
    'A','B','C','D','E','F','G','H','I','J','K','L','M',\
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',\
    '<space>','<Return>',\
    '<Left>','<Right>','<Up>','<Down>'\
]

defaultHotkeys = {}

def getUserConfig():
    defaultConfig = fileio.readJson("defaultConfig.json")
    setDefaultHotkeys(defaultConfig)
    if os.path.exists("config.json"):
        userConfig = fileio.readJson("config.json")
    else:
        userConfig = {}
    config = mergeConfigs(defaultConfig,userConfig)
    return config

def setDefaultHotkeys(defaultConfig):
    global defaultHotkeys
    for key in defaultConfig["hotkeys"].keys():
        defaultHotkeys[key] = defaultConfig["hotkeys"][key]

def getGameConfig(baseDir,game,category):
    cateFile = baseDir + "/" + game + "/" + category + "_config.json"
    if os.path.exists(cateFile):
        return fileio.readJson(cateFile)
    return {}

def mergeConfigs(original,override):
    new = original
    for key in override.keys():
        if not type(override[key]) is dict:
            new[key] = override[key]
        else:
            new[key] = mergeConfigs(original[key], override[key])
    return new

def validateHotkeys(config):
    for key in config["hotkeys"].keys():
        if not config["hotkeys"][key] in validHotkeys:
            config["hotkeys"][key] = defaultHotkeys[key]
