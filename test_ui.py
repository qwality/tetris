import pygame
import pygame_gui

pygame.init()

# Inicializace okna
window_surface = pygame.display.set_mode((800, 600))
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600))

# Definice HTML komponent
html_message = """
<html>
    <body style='background-color: #000000; color: #ffffff;'>
        <h1>Hello, Pygame GUI!</h1>
        <p>Welcome to Pygame GUI. This is an HTML message.</p>
    </body>
</html>
"""

# Vykreslení HTML
html_container = pygame_gui.elements.UITextBox(html_message, pygame.Rect((50, 50), (700, 500)), manager, window_surface)

# Definice tlačítka
button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 500), (100, 50)),
                                      text='Click me!',
                                      manager=manager)

clock = pygame.time.Clock()
is_running = True

# Hlavní smyčka
while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                print("Hello, World!")
                if event.ui_element == button:
                    print("Hello, World!")  # Výpis při stisku tlačítka

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
