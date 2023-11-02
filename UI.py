from pygame import draw, font as pyfont, Surface, SRCALPHA, K_ESCAPE, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP

from Coord          import Coord
from Color          import Color
from Grid_display2  import Game_display
from Clock          import Clock

class UI:
    class Element:
        def __init__(self, surface, coord : Coord):
            self.coord = coord
            self.surface = surface
    class Element_with_size(Element):
        def __init__(self, surface, coord : Coord, width : int, height : int, fill_color=Color.black):
            super().__init__(surface, coord)

            self.width, self.height = width, height
            self.fill_color = fill_color

        def display(self):
            draw.rect(
                    self.surface, self.fill_color,
                    (
                        self.coord.x, self.coord.y,
                        self.width, self.height
                    )
                )
    
    class TextBox(Element):
        def __init__(self, surface, coord:Coord, text:str='', font_size=36, font_color=Color.white, fill_color=Color.black):
            super().__init__(surface, coord)

            self.font_size  = font_size
            self.font_color = font_color
            self.__text       = text
        
        @property
        def text(self):
            return self.__text
        
        @text.setter
        def text(self, value):
            self.__text = value
            self.display()

        def display(self):
            font = pyfont.Font(None, self.font_size)
            text_render = font.render(self.text, True, self.font_color)
            self.surface.blit(text_render, tuple(self.coord))

    class Menu(Element_with_size):
        def __init__(self, surface, coord: Coord, item_width:int, item_height:int, border:int, items:list[any]=[], alpha:int=200, fill_color=Color.black):
            self.item_width     = item_width
            self.item_height    = item_height
            self.border         = border
            self.header:str     = ''

            self.items :list[UI.Element] = items

            super().__init__(surface, coord, item_width + 2 * border, len(self.items) * item_height + 2 * border, fill_color)

            self.transparent = Surface((self.width, self.height), SRCALPHA)
            self.alpha = alpha

        @property
        def size(self):
            return (
                self.border * 2 + self.item_width,
                self.border * 2 + len(self.items) * self.item_height
            )

        def display(self):
            draw.rect(self.transparent, self.fill_color + (self.alpha,), self.transparent.get_rect())
            self.surface.blit(self.transparent, tuple(self.coord))

            font = pyfont.Font(None, 36)
            text_render = font.render(self.header, True, Color.white)
            self.surface.blit(text_render, tuple(self.coord + (5, 5)))

            w, h = font.size('menu')

            text_render = font.render(f'menu', True, Color.white)
            self.surface.blit(text_render, tuple(self.coord + (self.width // 2 - w // 2, 5)))

            for item in self.items:
                item.display()

        def add_button(self, label:str, func):
            self.items.append(
                UI.Button(self.surface,
                          Coord(self.coord.x + self.border, self.coord.y + len(self.items) * self.item_height + self.border),
                          self.item_width, self.item_height, label, func, fill_color=Color.soft_grey
                          )
            )
            self.transparent = Surface(self.size, SRCALPHA)

    class Button(Element_with_size):
        def __init__(self, surface, coord: Coord, width: int, height: int, label:str, func, fill_color=Color.black):
            super().__init__(surface, coord, width, height, fill_color)
            self.label      = label
            self.function   = func
            UI.observers.append(self)
            self.mouse_in   = False
            self.mouse_down = False

        def hit_box(self, x, y):
            if self.coord.x < x < self.coord.x + self.width and self.coord.y < y < self.coord.y + self.height:
                return True
            else:
                return False

        def event_listener(self, mouse_pos, event):
            if event.type == MOUSEMOTION:
                self.mouse_in = self.hit_box(*mouse_pos)
            elif event.type == MOUSEBUTTONDOWN and self.mouse_in:
                self.mouse_down = True
            elif event.type == MOUSEBUTTONUP:
                if self.mouse_down:
                    self.function()
                self.mouse_down = False
                

        def on_mouse_over(self):
            pass

        def on_mose_leave(self):
            pass

        def on_press(self):
            pass

        def display(self):
            if self.mouse_down:
                self.fill_color = Color.lighter(self.fill_color, 30)
            if self.mouse_in:
                self.fill_color = Color.lighter(self.fill_color, 20)
            super().display()
            if self.mouse_down:
                self.fill_color = Color.darker(self.fill_color, 30)
            if self.mouse_in:
                self.fill_color = Color.darker(self.fill_color, 20)

            font = pyfont.Font(None, 56)
            w, h = font.size(self.label)

            text_render = font.render(self.label, True, Color.dark_grey)
            self.surface.blit(text_render, tuple(self.coord + (self.width // 2 - w // 2, self.height // 2 - h // 2)))


    observers = []
    __instance = None
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(UI, cls).__new__(cls)
        return cls.__instance

    def __init__(self, game_window_width, game_window_height):
        self.border = 25
        self.score_position = 5

        self.game_width, self.game_height = game_window_width, game_window_height

        self.game           = None
        self.score          = None
        self.surface        = None
        self.clock          = None
        self.menu           = None

    def create_surface(self, value):
        self.game.surface = value
        self.surface = value

    @property
    def size(self):
        gw, gh = self.game.size
        return (gw + 2 * self.border, gh + 2 * self.border)

    def create_game_display(self, grid_size : int, grid_offset : int, fill_color, blanc_color, colors):
        self.game = Game_display(self.border, self.border, self.game_width, self.game_height, grid_size, grid_offset, fill_color, blanc_color, colors)

    def create_score(self, font_size=36, font_color=Color.white, fill_color=Color.black):
        self.score = UI.TextBox(self.surface, Coord(self.score_position, self.score_position))

    def create_clock(self, tick_speed, frame_rate):
        self.clock = Clock(tick_speed, frame_rate)

    def create_menu(self, item_width:int, item_height:int, border:int):
        w, h = self.size
        x = (w - item_width  - border * 2) // 2
        y = (h - item_height - border * 2) // 2

        self.menu = UI.Menu(self.surface, Coord(x, y), item_width, item_height, border)

    def display(self):
        self.game.display()
        if not self.clock.paused:
            self.score.text = f'score: {self.game.score}'
        else:
            self.menu.header = f'score: {self.game.score}'
            self.menu.display()


    def input_handler(self, py_key):
        if py_key == K_ESCAPE:
            self.clock.paused = not self.clock.paused
        elif not self.clock.paused:
            game_over = self.game.movement_handler(py_key)

        pass


    


