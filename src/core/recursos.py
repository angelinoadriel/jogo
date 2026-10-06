import pygame


class GerenciadorRecursos:

    def __init__(self):
        self.imagens = {}
        self.fontes = {}


    # =====================================================
    # IMAGENS
    # =====================================================
    def carregar_imagem(self, caminho, recortar_transparencia=False):
        chave = (caminho, recortar_transparencia)

        # Se já estiver carregada, reutiliza a imagem
        if chave in self.imagens:
            return self.imagens[chave]

        imagem = pygame.image.load(caminho).convert_alpha()

        # Remove a área totalmente transparente, quando solicitado
        if recortar_transparencia:
            area_visivel = imagem.get_bounding_rect(min_alpha=1)

            if area_visivel.width > 0 and area_visivel.height > 0:
                imagem = imagem.subsurface(area_visivel).copy()

        self.imagens[chave] = imagem

        return imagem


    # =====================================================
    # FONTES
    # =====================================================
    def carregar_fonte(self, caminho, tamanho):
        chave = (caminho, tamanho)

        # Se já estiver carregada, reutiliza a fonte
        if chave in self.fontes:
            return self.fontes[chave]

        fonte = pygame.font.Font(caminho, tamanho)
        self.fontes[chave] = fonte

        return fonte


    # =====================================================
    # LIMPEZA
    # =====================================================
    def limpar(self):

        self.imagens.clear()
        self.fontes.clear()