from random import randrange
from pygame import draw, K_UP, K_DOWN, K_RIGHT, K_LEFT

from Shape2 import Shape
from Coord  import Coord

class GameOver(Exception):
    def __init__(self, message="Game Over"):
        self.message = message
        super().__init__(self.message)

class Game_display:
    def __init__(self, x : int, y : int, width : int, height : int, grid_size : int, offset : int, fill_color, blanc_color, colors) -> None:
        self.surface = None

        self.coord = Coord(x, y)
        self.width = (width - offset) // (grid_size + offset)
        self.height = (height - offset) // (grid_size + offset)

        self.grid_size = grid_size
        self.offset = offset

        self.fill_color = fill_color
        # self.colors = (blanc_color, *filter(lambda a: a not in (fill_color, blanc_color),colors))
        self.colors = (blanc_color, *(color for color in colors if color not in (fill_color, blanc_color)))

        self.score:int = 0
        self.current_shape = self._get_new_shape()
    
        self.grid = self.get_new_grid()
        # self.garbage = self.grid.copy()

    def reset(self):
        self.grid = self.get_new_grid()
        self.replace_shape()

    def get_new_grid(self):
        return [
            [0 for x in range(self.width)] for y in range(self.height)
        ]

    def get_random_color_index(self):
        return randrange(1, len(self.colors))

    def _get_new_shape(self):
        shape = Shape(
            self.get_random_color_index(),
        )
        shape.coord += (self.width // 2 - shape.width // 2), 0
        return shape

    def replace_shape(self):
        self.current_shape = self._get_new_shape()

    @property
    def size(self):
        return (
            self.width * (self.grid_size + self.offset) + self.offset,
            self.height * (self.grid_size + self.offset) + self.offset
            )
    
    def display(self):
        def draw_rect(color_index, x, y):
            if color_index:
                draw.rect(
                    self.surface, self.colors[0],
                    (
                        self.coord.x + x * (self.grid_size + self.offset), self.coord.y + y * (self.grid_size + self.offset),
                        self.grid_size + self.offset * 2, self.grid_size + self.offset * 2
                    )
                )
            draw.rect(
                self.surface, self.colors[color_index],
                (
                    self.coord.x + x * (self.grid_size + self.offset) + self.offset, self.coord.y + y * (self.grid_size + self.offset) + self.offset,
                    self.grid_size, self.grid_size
                )
            )
        
        self.surface.fill(self.fill_color)

        for x, y in self.current_shape.coords:

            if y >= 0: self.grid[y][x] = self.current_shape.color_index
            
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):

                draw_rect(col, x, y)
                # self.grid[y][x] = self.garbage[y][x]
                
        for x, y in self.current_shape.coords:

            if y >= 0: self.grid[y][x] = 0

        # display.update()
       
    def __collision_checker(self, shape : Shape):
        for x, y in shape.coords:
            if not (0 <= x < self.width):
                return True
            elif y >= self.height:
                return True
            elif y >= 0 and 0 <= x < self.width and self.grid[y][x] > 0:
                return True
        return False

    def movement_handler(self, movement):
        shape_copy = self.current_shape.copy()

        if movement == K_LEFT:
            self.current_shape.coord -= 1, 0
            if self.__collision_checker(self.current_shape):
                self.current_shape = shape_copy
            else: pass
        elif movement == K_RIGHT:
            self.current_shape.coord += 1, 0
            if self.__collision_checker(self.current_shape):
                self.current_shape = shape_copy
            else: pass
        elif movement == K_DOWN:
            self.current_shape.coord += 0, 1
            if self.__collision_checker(self.current_shape):
                if self.current_shape.coord.y < 0:
                    return True
                shape_copy.remove(self.grid)
                self.__grid_handler()
                self.replace_shape()
            else: pass
        elif movement == K_UP: # rotation
            "                                                                     -----experimentalni rotace-----"
            for position in ((0,0), (1,0), (-1,0), (0,-1), (2,0), (-2,0), (0,-2), (1,-1), (-1,-1), (2,-1), (-2,-1)):
                self.current_shape = shape_copy.copy()
                self.current_shape.coord += position
                self.current_shape.rotate()
                if not self.__collision_checker(self.current_shape): break
            else: self.current_shape = shape_copy
            
        return False

    def __grid_handler(self):
        rows = []
        for y, row in enumerate(self.grid):
            full = False
            for x, col in enumerate(row):
                if self.grid[y][x] == 0:
                    full = False
                    break
                else:
                    full = True
            if full:
                rows.append(y)
        if rows:
            self.score += int((100 / 3) * 3 ** len(rows))
            for i in (item - index for index, item in enumerate(rows)):
                del self.grid[i]

            self.grid = [[0 for col in range(self.width)] for row in rows] + self.grid

