from random import randrange, choice
from typing import Generator

class Shape:
    dict = {
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
    _list = list(dict.keys())

    def __init__(self, color_index=0):
        k = choice(self._list)
        self.shape = [k ,randrange(0, len(Shape.dict[k]))]
        self.x, self.y = 0, -len(self.get_shape())
        self.color_index = color_index
        self.last_move = (0, 0)

    def get_shape(self):
        return Shape.dict[self.shape[0]][self.shape[1]]

    def get_coords(self):
        for y, row in enumerate(self.get_shape()):
            for x in row:
                yield self.x + x, self.y + y

    def move_by(self, x, y):
        self.x += x
        self.y += y
        self.last_move = (-x, -y)

    def rotate(self):
        max_index, index = len(Shape.dict[self.shape[0]]) - 1, self.shape[1]
        if index >= max_index: self.shape[1] = 0
        else: self.shape[1] += 1
        self.last_move = (0, 0)

    def rotate_back(self):
        max_index, index = len(Shape.dict[self.shape[0]]) - 1, self.shape[1]
        if index <= 0: self.shape[1] = max_index
        else: self.shape[1] -= 1

    def remove(self, garbage : list):
        for x, y in self.get_coords():
            garbage[y][x] = self.color_index

    def move_back(self):
        self.move_by(*self.last_move)


