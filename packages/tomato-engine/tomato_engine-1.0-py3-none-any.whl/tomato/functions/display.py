import numpy as np
import pygame

"""
Funções relacionadas a mostrar e atualizar a janelinha de
observação dos autômatos.
"""


def create_screen(cells, cell_size, title):
    # {{{
    cells_x, cells_y = cells

    screen = pygame.display.set_mode((cells_x * cell_size, cells_y * cell_size))
    pygame.display.set_caption(title)

    return screen


# }}}


def draw_screen(screen, display_matrix, size):
    # {{{
    y, x = tuple(size * n for n in display_matrix.shape[:2])

    surface = pygame.surfarray.make_surface(display_matrix)
    surface = pygame.transform.scale(surface, (y, x))
    screen.blit(surface, (0, 0))
    array_from_display = pygame.surfarray.pixels3d(surface)

# }}}
