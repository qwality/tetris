from random import randrange, choice
from typing import Generator
from Coord  import Coord

class Shape:

    possible_shapes = {
        0: [
            [
                [0,1],
                [0,1]
            ] 
        ],
        1: [
            [
                [],
                [0],
                [0,1,2]
            ],
            [
                [0,1],
                [0],
                [0]
            ],
            [
                [0,1,2],
                [2]
            ],
            [
                [2],
                [2],
                [1,2]
            ]
        ],
        2: [
            [
                [],
                [2],
                [0,1,2]
            ],
            [
                [0],
                [0],
                [0,1]
            ],
            [
                [0,1,2],
                [0]
            ],
            [
                [1,2],
                [2],
                [2]
            ]
        ],
        3: [
            [
                [0],
                [0,1],
                [1]
            ],
            [
                [],
                [1,2],
                [0,1]
            ],
            [
                [1],
                [1,2],
                [2]
            ],
            [
                [1,2],
                [0,1]
            ]
        ],
        4: [
            [
                [2],
                [1,2],
                [1]
            ],
            [
                [],
                [0,1],
                [1,2]
            ],
            [
                [0],
                [0,1],
                [1]
            ],
            [
                [0,1],
                [1,2]
            ]
        ],
        5: [
            [
                [],
                [0,1,2,3]
            ],
            [
                [1],
                [1],
                [1],
                [1]
            ],
            [
                [],
                [],
                [0,1,2,3]
            ],
            [
                [2],
                [2],
                [2],
                [2]
            ]
        ],
        6: [
            [
                [],
                [1],
                [0,1,2]
            ],
            [
                [0],
                [0,1],
                [0]
            ],
            [
                [0,1,2],
                [1]
            ],
            [
                [2],
                [1,2],
                [2]
            ]
        ]
    }

    def __init__(self, color_index=0, shape=None, coord=None):
        random_shape_index      = choice(list(Shape.possible_shapes.keys()))
        random_shape_rotation   = randrange(0, len(Shape.possible_shapes[random_shape_index]))

        self.shape              = (random_shape_index, random_shape_rotation)   if shape is None else shape
        self.coord              = Coord(0, -self.height)                    if coord is None else coord
        self.color_index        = color_index

    def __repr__(self):
        return f'shape: ({self.color_index}, {self.shape}, {self.coord})'

    @property
    def width(self):
        return max(map(len, self.shape))

    @property
    def height(self):
        return len(self.shape)

    @property
    def shape(self):
        # print(f'internal values: {self._si}, {self._sr}')
        return Shape.possible_shapes[self._si][self._sr]
    
    @shape.setter
    def shape(self, value):
        # print(f'{value}')
        self._si, self._sr = value
        # print(f'setter: {self._si}, {self._sr}')


    @property
    def coords(self) -> Generator:
        for y, row in enumerate(self.shape):
            for x in row:
                # yield self.x + x, self.y + y
                yield self.coord + (x, y)

    #obsolete
    def move_by(self, x, y):
        """use += instead"""
        self.coord += x, y
        # self.x += x
        # self.y += y

    def rotate(self):
        max_index, index = len(Shape.possible_shapes[self._si]) - 1, self._sr
        if index >= max_index: self._sr = 0
        else: self._sr += 1

    def remove(self, garbage):
        for x, y in self.coords:
            if y >= 0:
                garbage[y][x] = self.color_index

    def copy(self):
        # print(f'copy: {(self._si, self._sr)}')
        return Shape(self.color_index, (self._si, self._sr), self.coord)