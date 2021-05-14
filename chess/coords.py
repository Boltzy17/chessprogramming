LETTER_COORDS = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}


class Coords:
    def __init__(self, x, y):
        if 0 <= x <= 7:
            self.x = x
        else:
            raise CoordsOutOfBoundsException("x out of bounds")
        if 0 <= y <= 7:
            self.y = y
        else:
            raise CoordsOutOfBoundsException("y out of bounds")

    def __str__(self):
        return f"{LETTER_COORDS[self.x]}{8-self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class CoordsOutOfBoundsException(Exception):
    pass


def pawns_white():
    yield A2
    yield B2
    yield C2
    yield D2
    yield E2
    yield F2
    yield G2
    yield H2


def pawns_black():
    yield A7
    yield B7
    yield C7
    yield D7
    yield E7
    yield F7
    yield G7
    yield H7


A1 = Coords(0, 7)
B1 = Coords(1, 7)
C1 = Coords(2, 7)
D1 = Coords(3, 7)
E1 = Coords(4, 7)
F1 = Coords(5, 7)
G1 = Coords(6, 7)
H1 = Coords(7, 7)
A2 = Coords(0, 6)
B2 = Coords(1, 6)
C2 = Coords(2, 6)
D2 = Coords(3, 6)
E2 = Coords(4, 6)
F2 = Coords(5, 6)
G2 = Coords(6, 6)
H2 = Coords(7, 6)
A3 = Coords(0, 5)
B3 = Coords(1, 5)
C3 = Coords(2, 5)
D3 = Coords(3, 5)
E3 = Coords(4, 5)
F3 = Coords(5, 5)
G3 = Coords(6, 5)
H3 = Coords(7, 5)
A4 = Coords(0, 4)
B4 = Coords(1, 4)
C4 = Coords(2, 4)
D4 = Coords(3, 4)
E4 = Coords(4, 4)
F4 = Coords(5, 4)
G4 = Coords(6, 4)
H4 = Coords(7, 4)
A5 = Coords(0, 3)
B5 = Coords(1, 3)
C5 = Coords(2, 3)
D5 = Coords(3, 3)
E5 = Coords(4, 3)
F5 = Coords(5, 3)
G5 = Coords(6, 3)
H5 = Coords(7, 3)
A6 = Coords(0, 2)
B6 = Coords(1, 2)
C6 = Coords(2, 2)
D6 = Coords(3, 2)
E6 = Coords(4, 2)
F6 = Coords(5, 2)
G6 = Coords(6, 2)
H6 = Coords(7, 2)
A7 = Coords(0, 1)
B7 = Coords(1, 1)
C7 = Coords(2, 1)
D7 = Coords(3, 1)
E7 = Coords(4, 1)
F7 = Coords(5, 1)
G7 = Coords(6, 1)
H7 = Coords(7, 1)
A8 = Coords(0, 0)
B8 = Coords(1, 0)
C8 = Coords(2, 0)
D8 = Coords(3, 0)
E8 = Coords(4, 0)
F8 = Coords(5, 0)
G8 = Coords(6, 0)
H8 = Coords(7, 0)

