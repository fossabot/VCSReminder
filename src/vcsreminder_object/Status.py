

class Status:

    def __init__(self, *args, **kwargs):
        self.stop = True
        self.start = False


    def start(self):
        self.start = True
        self.stop = False

    def stop(self):
        self.stop = True
        self.start = False

    def isStopped(self):
        return self.stop

    def isStarted(self):
        return self.start