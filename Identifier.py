class ID:
    def __init__(self, seed):
        self.counter = seed

    def getNext(self):
        self.counter += 1
        return self.counter