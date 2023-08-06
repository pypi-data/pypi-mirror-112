from ..classes import cell
import numpy as np


class Cell(cell.CellTemplate):
    # {{{
    # Este exemplo é particularmente simples porque, francamente,
    # o CellTemplate foi feito pensando nele.

    def update(self, state_matrix):
        self.state_matrix = state_matrix

        # Célula morta:
        if self.value == 0:
            if self.live_neighbors in (3, 6):
                self.value = 1
            else:
                self.value = 0
        # Célula viva:
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
