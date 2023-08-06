import numpy as np

"""
Estrutura de dados para a matriz que contém todos os autômatos.
"""


class CellMatrix:
    def __init__(self, state_matrix, rule_module):
        # {{{
        """
        Cria a matriz de autômatos a partir de uma regra e a
        matriz de estado inicial.
        """

        Cell = rule_module.Cell
        self.state_matrix = state_matrix

        self.cell_matrix = np.array(
            [
                Cell(value, (lin_num, col_num))
                for lin_num, lin in enumerate(self.state_matrix)
                for col_num, value in enumerate(lin)
            ]
        )

        self.display_func = np.vectorize(rule_module.Cell.display)

    # }}}

    def update(self):
        # {{{
        """
        Atualiza o estado de todas as células. Detalhe que é
        necessário copiar a matriz de estados porque matrizes do
        numpy são passadas por referência. A state_matrix é
        modificada in-place.
        """

        old_state_matrix = self.state_matrix.copy()

        for cell in self.cell_matrix:
            cell.update(old_state_matrix)
            self.state_matrix[cell.pos] = cell.value

        return self.state_matrix

    # }}}

    @classmethod
    def from_display(cls, display_matrix, rule_module):
        # {{{
        """
        Inicializa a partir da matriz de valores RGB ou valor de
        escala monocromática extraídos de uma imagem. Essa
        provavelmente é a maneira mais lenta possível de se fazer
        isso.
        """

        cell_from_display = rule_module.Cell.from_display
        pixels_gen = (cell_from_display(col) for lin in display_matrix for col in lin)

        state_matrix = np.array(list(pixels_gen))
        state_matrix = state_matrix.reshape(display_matrix.shape[:2])

        return CellMatrix(state_matrix, rule_module)

    # }}}

    def display(self):
        # {{{
        """
        Retorna a matriz para representação visual do conjunto de
        células. É feio desse jeito para suportar o células
        retornando tanto inteiros (caso grayscale) quanto tuplas.
        """

        rgb_tuple = self.display_func(self.state_matrix)

        if not isinstance(rgb_tuple, tuple):
            # Isso cheira a um anti-padrão...
            rgb_tuple = (rgb_tuple, rgb_tuple, rgb_tuple)

        rgb_matrix = np.dstack(rgb_tuple).astype(np.uint8)
        #
        return rgb_matrix

    # }}}

    @property
    def shape(self):
        return self.state_matrix.shape
