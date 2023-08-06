import numpy as np
from PIL import Image
from . import utils

"""
Funções relacionadas a ler e escrever arquivos.
"""


def load_png(path, size=1):
    # {{{
    """
    O 'size' se refere ao tamanho da célula na imagem. Se for 1,
    a imagem inteira será usada, se for 2, cada segundo pixel
    será excluído, e assim por diante.
    """

    img = Image.open(path).convert()
    # O :: é o que faz considerar somente os elementos de índice
    # divisível por size
    img_matrix = np.array(img)[0::size, 0::size]

    return img_matrix


# }}}


def save_png(path, display_matrix, size=1):
    # {{{
    y, x = (size * val for val in reversed(display_matrix.shape[:2]))

    img = Image.fromarray(display_matrix)
    img = img.resize(
        (x, y),
        resample=Image.NEAREST,
    )

    print(f"Imagem salva em {path}.")
    img.save(path, "PNG")


# }}}
