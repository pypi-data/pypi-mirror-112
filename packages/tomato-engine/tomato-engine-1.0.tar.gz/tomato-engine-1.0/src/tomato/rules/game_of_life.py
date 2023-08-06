from ..classes import cell

"""
Implementação do Game of Life. Também pode ser usada como exemplo
de como implementar uma rule arbitrária.

Neste caso há somente um tipo de célula, mas você pode definir
qualquer número de tipos diferentes, cada qual com um
comportamento diferente. Neste caso, você criaria uma classe mãe,
que é a que você passaria para a Board, e ela trataria de
instanciar objetos de classes filhas com base no valor inicial.
Depois faço um exemplo disso.
"""


class Cell(cell.CellTemplate):
    # {{{
    def update(self, state_matrix):
        self.state_matrix = state_matrix

        # Dead cell
        if self.value == 0:
            if self.live_neighbors == 3:
                self.value = 1
            else:
                self.value = 0
        # Live cell
        else:
            if self.live_neighbors in (2, 3):
                self.value = 1
            else:
                self.value = 0

    @property
    def neighbors(self):
        return self.moore_neighborhood

    @property
    def live_neighbors(self):
        return sum(self.neighbors)


# }}}
