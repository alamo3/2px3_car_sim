class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self):
        return self.x, self.y

    @staticmethod
    def t2p(tup):
        return Point(tup[0], tup[1])