class Manager:
    def __init__(self):
        self.actions = {}

    def assign(self, name):
        def decorate(cb):
            self.actions[name] = cb
        return decorate
    
    def execute(self, name):
        if name not in self.actions:
            print("Action not defined!")
        else:
            self.actions[name](self)