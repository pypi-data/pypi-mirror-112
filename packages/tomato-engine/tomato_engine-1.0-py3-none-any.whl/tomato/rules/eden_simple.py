from ..classes import cell
import random

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
    # Este exemplo é particularmente simples porque, francamente,
    # o CellTemplate foi feito pensando nele.

    def update(self, state_matrix):
        self.state_matrix = state_matrix
        live_neighbors = self.live_neighbors

        if live_neighbors > 7:
            self.value = 1
        elif live_neighbors > 1:
            zz = random.choice(range(1, 1000))
            if zz <= 158:
                self.value = 0  # morte
            elif zz > 158 and zz <= 500:
                self.value = 0  # normal
            elif zz > 500 and zz <= 850:
                self.value = 1  # tumor
            else:
                if live_neighbors > 2:
                    self.value = 1  # spread
                else:
                    self.value = 1  # tumor
        else:
            self.value = 0

    @property
    def neighbors(self):
        return self.moore_neighborhood

    @property
    def live_neighbors(self):
        return sum(self.neighbors)


# }}}
