class PVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mag(self):
        return self.x**2 + self.y**2

    def limit(self, maxMag):
        mg = self.mag()
        if mg > 0 and mg > maxMag:
            self.x *= maxMag / mg
            self.y *= maxMag / mg

    def __add__(self, o):
        return PVector(self.x + o.x, self.y + o.y)

    def __sub__(self, o):
        return PVector(self.x - o.x, self.y - o.y)

    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        return self

    def __isub__(self, o):
        self.x -= o.x
        self.y -= o.y
        return self

    def __repr__(self):
        return f"vec({self.x}, {self.y})"

    @staticmethod
    def _test():
        p1 = PVector(1, 2)
        p2 = PVector(3, 4)
        print(f"p1: {p1}")
        print(f"p2: {p2}")
        print(f"p1 + p2: {p1 + p2}")
        print(f"p1: {p1}")
        print(f"p2: {p2}")


if __name__ == "__main__":
    PVector._test()
