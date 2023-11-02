from random import randrange
from pygame import draw, display

from Shape import Shape

class Grid_display:
    def __init__(self, width : int, height : int, grid_size : int, offset : int, fill_color, blanc_color, colors) -> None:
        self.width = (width - offset) // (grid_size + offset)
        self.height = (height - offset) // (grid_size + offset)
        self.size = grid_size
        self.offset = offset
        self.fill_color = fill_color
        self.colors = [blanc_color]

        for i in colors:
            if i == fill_color or i == blanc_color: continue
            else: self.colors.append(i)
    
        self.grid = [
            [0 for x in range(self.width)] for y in range(self.height)
        ]
        self.garbage = [
            [0 for x in range(self.width)] for y in range(self.height)
        ]

    def get_random_color_index(self):
        return randrange(1, len(self.colors))

    def get_window_size(self):
        return (
            self.width * (self.size + self.offset) + self.offset,
            self.height * (self.size + self.offset) + self.offset
            )

    def update_draw(self, window, shape : Shape):
        for x, y in shape.get_coords():
            if y >= 0:
                self.grid[y][x] = shape.color_index
            
        window.fill(self.fill_color)
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if col:
                    draw.rect(
                    window, self.colors[0], 
                    (
                        x * (self.size + self.offset), y * (self.size + self.offset),
                        self.size + self.offset * 2, self.size + self.offset * 2
                        )
                    )
                draw.rect(
                    window, self.colors[col], 
                    (
                        x * (self.size + self.offset) + self.offset, y * (self.size + self.offset) + self.offset,
                        self.size, self.size
                        )
                    )
                self.grid[y][x] = self.garbage[y][x]
                
        for x, y in shape.get_coords():
            if y >= 0:
                self.grid[y][x] = 0

        display.update()
       
    def boundary(self, shape : Shape):
        for x, y in shape.get_coords():
            if x < 0:
                shape.move_by(1,0)
                x += 1
            elif x >= self.width:
                shape.move_by(-1,0)
                x -= 1

            if y >= self.height:
                shape.move_by(0,-1)
                return False
            
            # if shape.last_move is None:
            #     shape.rotate_back()
            #     shape.last_move = (0, 0)
            if y >= 0:
                if self.garbage[y][x] and shape.last_move[1] == -1:
                    shape.move_by(0,-1)
                    return False
                elif 0 <= x < self.width and self.garbage[y][x] > 0:
                    if bool(abs(sum(shape.last_move))):
                        shape.move_back()
                    else:
                        shape.rotate_back()
                    return True
        return True

    def get_new_shape(self):
        return Shape(self.get_random_color_index())

    def chechk_hit(self, shape : Shape):
        if not self.boundary(shape):
            shape.remove(self.garbage)
            return self.get_new_shape()
        return shape
