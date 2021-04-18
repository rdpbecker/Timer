class Error(Exception):
    pass

class ComponentTypeError(Error):
    message = ""

    def __init__(self,message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'The component type {self.message} is not a valid type'
