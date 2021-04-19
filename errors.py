class Error(Exception):
    pass

class ComponentTypeError(Error):
    message = ""

    def __init__(self,message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'The component type "{self.message}" is not a valid type'

class HotKeyTypeError(Error):
    message = ""
    default = ""
    control = ""

    def __init__(self,message,default,control):
        self.message = message
        self.default = default
        self.control = control
        super().__init__(self.message)

    def __str__(self):
        return f'The hotkey "{self.message}" is an invalid key.  Using the default hotkey "{self.default}" for the control action "{self.control}"'
