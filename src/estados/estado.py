from abc import ABC, abstractmethod


class Estado(ABC):

    def __init__(self, jogo):
        self.jogo = jogo

    # =====================================================
    # CICLO DE VIDA
    # =====================================================
    def entrar(self):
        pass

    def sair(self):
        pass


    # =====================================================
    # LOOP DO ESTADO
    # =====================================================
    @abstractmethod
    def processar_eventos(self, entrada):
        pass

    @abstractmethod
    def atualizar(self, dt):
        pass

    @abstractmethod
    def desenhar(self, tela):
        pass