import pygame
import sys

pygame.init()

# Tela
WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entregando")

# Fundo
imagem_fundo = pygame.image.load('Assets/Imagens/Perdeu.png').convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))

def perdeu_entrega():

    waiting = True

    while waiting:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                waiting = False

        # Desenha fundo
        window.blit(imagem_fundo, (0, 0))

        # Textos
        title_font = pygame.font.SysFont(None, 72)
        font = pygame.font.SysFont(None, 40)
        font_inicio = pygame.font.SysFont(None, 30)

        title = title_font.render("Entrega atrasada!", True, (255, 215, 0))

        linha2 = font.render("A entrega nao chegou ao cliente.", True, (255, 255, 255))

        inicio = font_inicio.render(
            "Clique para jogar novamente.",
            True,
            (255, 255, 255)
        )

        # Mostra na tela
        window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        window.blit(linha2, (WIDTH // 2 - linha2.get_width() // 2, HEIGHT // 3 + 50))

        window.blit(inicio, (WIDTH // 2 - inicio.get_width() // 2, HEIGHT - 80))

        pygame.display.flip()

perdeu_entrega()