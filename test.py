# class A():
#     l = {
#         'a': 5
#     }
#     a = 4

#     def __getattr__(self, name):
#         if name in self.l:
#             return self.l[name]
#         else:
#             raise AttributeError(f'{name} neni v seznamu barev')
        
#     @property
#     def c(self):
#         return self.x, self.y
    
#     @c.setter
#     def c(self, value):
#         self.x, self.y = value


# a = A()
# A.a = 3

# b = A()
# print(b.a)
# # a.c += 1, 1

# # print(a.c)

# class Coord():
#     def __init__(self, *args, **kwargs):
#         print(args, kwargs)

# a = Coord(0,1)

# class ColorMeta(type):
#     def __getattr__(cls, name):
#         if name in cls.colors:
#             return cls.colors[name]
#         raise AttributeError(f'{name} není v seznamu barev')

# class Color(metaclass=ColorMeta):
#     colors = {
#         'blue': (30, 40, 200),
#         'red': (200, 40, 30)
#     }


# print(Color.blue)
# print(Color.red)

from typing import Any


class Coord():
    dimensions = 'xyzt'

    def __init__(self, *args, **kwargs):
        self.value = args

    def __repr__(self):
        return f'coord: {self.value}'

    def __iter__(self):
        return iter(self.value)

    def __set__(self, __, value):
        self.value = value

    def __getitem__(self, key):
        return self.value[key]
    
    def __setitem__(self, key, value):
        self.value = self.value[:key] + (value,) + self.value[key + 1:]

    def __getattr__(self, name):
        if name in self.dimensions:
            i = self.dimensions.index(name)
            return self.value[i]
        else:
            raise ValueError
        
    def __setattr__(self, __name: str, __value: Any):
        if __name == 'value':
            super().__setattr__(__name, __value)
        elif __name in self.dimensions:
            i = self.dimensions.index(__name)
            self.value = self.value[:i] + (__value,) + self.value[i + 1:]
        else:
            raise ValueError

    def __iadd__(self, other):
        return tuple(a + b for a, b in zip(self.value, other))

    def __isub__(self, other):
        return tuple(a - b for a, b in zip(self.value, other))
    
    def __add__(self, other):
        # print(other)
        return tuple(a + b for a, b in zip(self.value, other))


class TestClass:
    coord = Coord()
    def __init__(self):
        self.coord = 0, 1

test = TestClass()
test.coord = 0, 2
test.coord.x = 1

test.coord += (1, 2)
# test.coord -= 2, 4
# test.coord[0] = 5

# a = test.coord + (1, 2)

print(test.coord)
# x, y = test.coord
# print(x,y)


# print([i for i in filter(lambda a: a not in [1,2], range(3))])

# for i in test.coord:
#     print(i)


# L = [1, 2, '3', 4, 5, '6', 7, '8', 9, 10]  # příklad seznamu
# indexes = [2, 5, 7]  # příklad seznamu indexů k odstranění

# # Odstraň prvky podle indexů
# for i in (item - index for index, item in enumerate(indexes)):
#     del L[i]

# print(L)
from dataclasses import dataclass, astuple

@dataclass
class Color:
    black       :tuple = ( 10,  0,  0)
    soft_grey   :tuple = ( 60, 62, 65)
    dark_grey   :tuple = ( 35, 32, 30)
    white       :tuple = (255,255,255)
    red         :tuple = (220, 40, 30)
    green       :tuple = ( 30,200, 40)
    blue        :tuple = ( 30, 40,200)
    yellow      :tuple = (255,220,  0)

    __instance = None

    @classmethod
    @property
    def colors(cls):
        if cls.__instance is None: cls.__instance = Color()
        return astuple(cls.__instance)

# Color.__instance = Color()


main_tuple = ((1, 2, 3), (4, 5, 6))
tuple_to_remove = (1, 2, 3)

result = tuple(item for item in main_tuple if item != tuple_to_remove)
print(result)  # Vypíše: ((4, 5, 6),)

