import importlib
from util import fileio
from util import readConfig as rc
import errors as Errors

class ComponentLoader:
    app = None
    state = None
    rootWindow = None
    configDict = None
    configKeys = None

    def __init__(self,app,state,rootWindow):
        self.app = app
        self.state = state
        self.rootWindow = rootWindow
        self.configDict = fileio.readJson("Components/componentList.json")
        self.configKeys = self.configDict.key()
        for key in self.configKeys:
            self.configDict[key]["numLoaded"] = 0

    def loadComponent(self,ctype):
        if not ctype in self.configKeys:
            raise Errors.ComponentTypeError(ctype)

        module = importlib.import_module(self.configDict[ctype]["module_name"])
        myClass = getattr(module,self.configDict[ctype]["class_name"])
        config = rc.getCUserConfig(ctype,self.configDict[ctype]["numLoaded"])
        self.configDict[ctype]["numLoaded"] = self.configDict[ctype]["numLoaded"] + 1
        if self.configDict[ctype]["class_name"] == "Buttons":
            return myClass(self.app,self.state,self.rootWindow)
        else:
            return myClass(self.app,self.state)
