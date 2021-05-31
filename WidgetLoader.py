import importlib
from util import fileio
from util import readConfig as rc
import errors as Errors

class WidgetLoader:
    app = None
    state = None
    rootWindow = None
    configDict = None
    configKeys = None

    def __init__(self,app,state,rootWindow):
        self.app = app
        self.state = state
        self.rootWindow = rootWindow
        self.configDict = fileio.readJson("Widgets/widgetList.json")
        self.configKeys = self.configDict.keys()

    def loadWidget(self,ctype,configFileName=""):
        if not ctype in self.configKeys:
            raise Errors.WidgetTypeError(ctype)

        module = importlib.import_module(self.configDict[ctype]["module_name"])
        myClass = getattr(module,self.configDict[ctype]["class_name"])
        config = rc.getCUserConfig(ctype,configFileName)
        if self.configDict[ctype]["class_name"] == "Buttons":
            return myClass(self.rootWindow,self.state,config,self.app)
        else:
            return myClass(self.rootWindow,self.state,config)
