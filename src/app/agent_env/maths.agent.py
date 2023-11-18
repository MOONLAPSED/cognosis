from math import sqrt, hypot

a = 0b1010 #Binary Literals
b = 100 #Decimal Literal 
c = 0o310 #Octal Literal
d = 0x12c #Hexadecimal Literal
#Float Literal
float_1 = 10.5 
float_2 = 1.5e2
#Complex Literal 
x = 3.14j


Number = int | float
Vector = tuple[Number, ...]
"""https://en.wikipedia.org/wiki/Coordinate_vector"""
Point = tuple[Number, Number]
"""x, y"""
Rectangle = tuple[Number, Number, Number, Number]
"""x, y, width, height"""

SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60

SECONDS_IN_HOUR = MINUTES_IN_HOUR * SECONDS_IN_MINUTE


def min_max_scale(x: Number, min_x: Number, max_x: Number):
    """https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)"""
    return (x - min_x) / (max_x - min_x)


def dot_product(a: Vector, b: Vector):
    """https://en.wikipedia.org/wiki/Dot_product"""
    return sum(i * j for i, j in zip(a, b))


def cosine_similarity(a: Vector, b: Vector):
    """https://en.wikipedia.org/wiki/Cosine_similarity"""
    return dot_product(a, b) / (
        sqrt(sum(i**2 for i in a)) * sqrt(sum(i**2 for i in b))
    )


def average(a: Vector) -> Number:
     """https://en.wikipedia.org/wiki/Average"""
     return sum(a) / len(a)


def center(rectangle: Rectangle) -> Point:
    return (
        rectangle[0] + rectangle[2] / 2,
        rectangle[1] + rectangle[3] / 2,
    )


def distance(a: Point, b: Point) -> float:
    return hypot(a[0] - b[0], a[1] - b[1])


def build_quadratic(a, b, c):
    '''takes and plugs a, b & c into quad funct and returns val or error'''
    return lambda x: a*x**2 +b*x +c


def scalar_multiplication(required, *args):
    '''(vector) X (scaling_factor'''
    '''(*args) X (required)'''
    try: 
        v = [*args]
        w = [4*x for x in v]
    except:
        return


def remainders(self):
    remainder = [x**2 % self for x in range (1, 101)]
    print(remainder)
    return remainder
