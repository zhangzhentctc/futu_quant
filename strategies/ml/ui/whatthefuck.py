class whatthefuck:
    def __init__(self):
        self.cnt = 0
        self.string = ""

    def add_x(self, x):
        self.cnt += x

    def assign(self, val):
        self.cnt = val