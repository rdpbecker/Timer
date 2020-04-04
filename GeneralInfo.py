class GeneralInfo:
    show = False
    startCallback = None
    generalCallback = None

    def __init__(self,show,startCallback,generalCallback):
        self.show = show
        self.startCallback = startCallback
        self.generalCallback = generalCallback
