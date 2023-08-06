from ..functions import file
from .cellmatrix import CellMatrix
from .window import Window
import numpy as np
from time import time


class Board:

    """
    O nome dessa classe é vago, mas ela é importante. Esta é a
    interface do usuário, e também coordena a CellMatrix e a
    Window.
    """

    def __init__(self, rule_module, **kwargs):
        # {{{
        """
        Recebe a regra a ser adotada, assim como algumas
        configurações. A simulação em si começa com a função
        start.

        A rule_module é o módulo importado contendo a regra, no
        formato especificado pelo exemplo game_of_life.py.
        """

        self.rule_module = rule_module

        # Configurações opcionais são passadas por kwargs.
        self.debug = kwargs.get("debug", False)
        self.title = kwargs.get("title", "Simulação")
        self.paused = kwargs.get("paused", False)
        self.max_fps = kwargs.get("max_fps", 60)
        self.cell_size = kwargs.get("cell_size", 4)

        self.generation = 0

        if self.debug:
            # Lista com o tempo transcorrido para cada geração
            self.gen_time = []

    # }}}

    def start(self, state_matrix, show_window=True, paused=False):
        # {{{
        """
        Inicia a simulação, o estado inicial sendo dado pela
        state_matrix. state_matrix pode ser o caminho para uma
        imagem ou uma matriz de numpy com os valores desejados.
        """

        self.load_state(state_matrix)
        self.paused = paused

        if show_window:
            self.show_window()
        else:
            self.mainloop()

    # }}}

    def update(self):
        # {{{
        """
        Atualiza o estado da simulação, ou seja, realiza uma nova
        iteração.
        """

        if not self.debug:
            self.cellMatrix.update()
        else:
            initial_time = time()
            self.cellMatrix.update()
            self.gen_time.append(1000.0 * (time() - initial_time))

        self.generation += 1

    # }}}

    def show_window(self, paused=None):
        # {{{
        """
        Começa a simulação, mostrando a janelinha.
        """

        paused = paused if paused is not None else self.paused
        window = Window(
            self.cellMatrix.display(),
            debug=self.debug,
            title=self.title,
            paused=paused,
            max_fps=self.max_fps,
            cell_size=self.cell_size,
        )

        while window.running:
            window.query_inputs()

            if window.paused is False:
                self.update()
                window.update(self.cellMatrix.display())

                if self.debug:
                    self.print_debug()

        if self.debug:
            self.print_avg_update_time()

        # Para lembrar como o usuário deixou a janela
        self.paused = window.paused
        self.max_fps = window.max_fps

        window.quit()

    # }}}

    def mainloop(self):
        # {{{
        """
        Começa a simulação, sem mostrar a janelinha.
        """

        # Neste caso se escapa do loop com um ctrl+c
        while True:
            try:
                self.update()
            except KeyboardInterrupt:
                break

            if self.debug:
                self.print_debug()

        if self.debug:
            self.print_avg_update_time()

    # }}}

    def load_state(self, state_matrix):
        # {{{
        """
        Carrega uma matriz de estados a partir de uma imagem, uma
        matriz numpy ou uma lista de listas.
        """

        if isinstance(state_matrix, str):
            png_matrix = file.load_png(state_matrix, size=self.cell_size)
            self.cellMatrix = CellMatrix.from_display(png_matrix, self.rule_module)
        elif isinstance(state_matrix, np.ndarray):
            self.cellMatrix = CellMatrix(state_matrix, self.rule_module)
        elif isinstance(state_matrix, list):
            state_matrix = np.array(state_matrix)
            self.cellMatrix = CellMatrix(state_matrix, self.rule_module)
        else:
            raise TypeError(
                f"{type(state_matrix)} is not a valid type for a state matrix."
            )

    # }}}

    def print_debug(self):
        # {{{
        """
        Auto-explicativo. Printa as informações de depuração.
        """

        print(
            "| {:<16} {:<8} | {:<16} {:<8.4f} ms |".format(
                "Generation:",
                self.generation,
                "Generation time:",
                self.gen_time[-1],
            )
        )

    # }}}

    def print_avg_update_time(self):
        # {{{
        """
        Método bem específico. Printa o tempo médio das gerações
        e o desvio padrão.
        """

        print(
            "| Average generation time: {} +- {} ms |".format(
                np.mean(self.gen_time),
                np.std(self.gen_time),
            )
        )

    # }}}

    def save_png(self, path=None):
        # {{{
        """
        Salva o estado da cellMatrix em uma png, para
        visualização e para retomar a simulação depois.
        """

        if path is None:
            path = f"{self.title}_{self.generation}.png"

        display_matrix = self.cellMatrix.display()
        file.save_png(path, display_matrix, self.cell_size)

    # }}}

    @property
    def debug_info(self):
        # {{{
        """
        Retorna um dicionário com informações de depuração.
        """
        debug_info = {
            "generation": self.generation,
            "generation_time": self.gen_time,
        }
        return debug_info


# }}}
