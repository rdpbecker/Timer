import os, fileio

def getUserConfig():
    defaultConfig = fileio.readJson("defaultConfig.json")
    if os.path.exists("config.json"):
        userConfig = fileio.readJson("config.json")
    else:
        userConfig = {}
    config = mergeConfigs(defaultConfig,userConfig)
    return config

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
