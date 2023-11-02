import pygame
from pygame import display

from Color import Color
from UI import UI

def main():
    pygame.init()
    display.set_caption("-----Tetris-----")

    window_width, window_height = 500, 1000
    grid_size, grid_offset      = 50, 2
    fill_color, blanc_color     = Color.soft_grey, Color.dark_grey
    shape_colors                = (color for color in Color.colors if color not in (Color.black, Color.white))

    ui = UI(window_width, window_height)
    ui.create_game_display(grid_size, grid_offset, fill_color, blanc_color, shape_colors)
    ui.create_surface(display.set_mode(ui.size))
    ui.create_score()
    ui.create_menu(300, 100, 50)

    def reset_button():
        ui.game.reset()
        ui.game.score = 0
        ui.clock.paused = False

    ui.menu.add_button('restart', reset_button)



    ui.create_clock(2, 60)

    clock = pygame.time.Clock()
    running = True

    ui.game.coord.y += 7.5

    while running:
        for event in pygame.event.get():
            if event.type       == pygame.QUIT:            running = False
            elif event.type     == pygame.KEYDOWN:
                if event.key    == pygame.K_SPACE:         ui.game.replace_shape()
                elif event.key  == pygame.K_a:             print(
                                                                ui.game.current_shape.width,
                                                                ui.game.current_shape.height
                                                            )
                ui.input_handler(event.key)
            elif event.type     in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for observer in ui.observers:
                    observer.event_listener(pygame.mouse.get_pos(), event)
            
        

        with ui.clock as tick:
            if tick: ui.input_handler(pygame.K_DOWN)
            ui.display()

        display.update()

        clock.tick(ui.clock.framerate)

    pygame.quit()
    

if __name__ == '__main__':
    main()