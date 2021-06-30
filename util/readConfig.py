import os
from util import fileio
import errors as Errors

letters = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m',\
    'n','o','p','q','r','s','t','u','v','w','x','y','z',\
    'A','B','C','D','E','F','G','H','I','J','K','L','M',\
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'\
]

validHotkeys = letters + ["<Control-"+letter+">" for letter in letters] + \
[\
    '<space>','<Return>',\
    '<Left>','<Right>','<Up>','<Down>'\
]

validPositions = ["left","center-left","center","center-right","right"]

defaultHotkeys = {}

def getUserConfig():
    defaultConfig = fileio.readJson("defaults/global.json")
    setDefaultHotkeys(defaultConfig)
    if os.path.exists("config/global.json"):
        userConfig = fileio.readJson("config/global.json")
    else:
        userConfig = {}
    config = mergeConfigs(defaultConfig,userConfig)
    return config

def getCUserConfig(ctype,fileName):
    defaultConfig = fileio.readJson("defaults/"+ctype+".json")
    configPath = "config/" + fileName + ".json"
    if os.path.exists(configPath):
        userConfig = fileio.readJson(configPath)
    else:
        userConfig = {}
    config = mergeConfigs(defaultConfig,userConfig)
    return config

def setDefaultHotkeys(defaultConfig):
    global defaultHotkeys
    for key in defaultConfig["hotkeys"].keys():
        defaultHotkeys[key] = defaultConfig["hotkeys"][key]

def mergeConfigs(original,override):
    new = original
    for key in override.keys():
        if not type(override[key]) is dict:
            try:
                if key == "position" and not override[key] in validPositions:
                    raise Errors.ConfigValueError(key,override[key],original[key])
                new[key] = override[key]
            except Errors.ConfigValueError as e:
                print(e)
        else:
            new[key] = mergeConfigs(original[key], override[key])
    return new

def validateHotkeys(config):
    for key in config["hotkeys"].keys():
        try:
            if not config["hotkeys"][key] in validHotkeys:
                raise Errors.HotKeyTypeError(config["hotkeys"][key],defaultHotkeys[key],key)
        except Errors.HotKeyTypeError as e:
            print(e)
            config["hotkeys"][key] = defaultHotkeys[key]
