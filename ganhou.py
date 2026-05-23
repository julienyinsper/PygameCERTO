import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# Gera tela principal
WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entregando")

clock = pygame.time.Clock()

# Carrega imagem de fundo
imagem_fundo = pygame.image.load('Assets/Imagens/Ganhou.png').convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))

# Sons
som_ganhou = pygame.mixer.Sound("Assets/Sons/Ganhou.mp3")
musica_fundo = "Assets/Sons/Telainicio.mp3"


# Função para mostrar a tela de vitória
def entrega_concluida():

    # TOCA O SOM DE VITÓRIA
    som_ganhou.play()

    # Marca o tempo inicial
    tempo_inicio = pygame.time.get_ticks()

    # Controla se a música já começou
    musica_iniciada = False

    # Título
    title_font = pygame.font.SysFont(None, 72)
    title = title_font.render("Você ganhou!", True, (255, 215, 0))

    # Texto da história
    font = pygame.font.SysFont(None, 40)

    acontecimento = [
        "O entregador passou todas as fases",
        "e chegou ao cliente com sucesso!"
    ]

    font_inicio = pygame.font.SysFont(None, 30)

    inicio = font_inicio.render(
        "Clique em qualquer botão para continuar o jogo.",
        True,
        (255, 255, 255)
    )

    # Texto animado
    for i, line in enumerate(acontecimento):

        rendered_line = ""

        for char in line:

            rendered_line += char

            text = font.render(
                rendered_line,
                True,
                (255, 255, 255)
            )

            # Eventos durante animação
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # Começa música após 2 segundos
            if not musica_iniciada and pygame.time.get_ticks() - tempo_inicio >= 2000:

                pygame.mixer.music.load(musica_fundo)
                pygame.mixer.music.play(-1)

                musica_iniciada = True

            # Fundo
            window.blit(imagem_fundo, (0, 0))

            # Título
            window.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4)
            )

            # Linhas anteriores
            for j in range(i):

                previous_text = font.render(
                    acontecimento[j],
                    True,
                    (255, 255, 255)
                )

                window.blit(
                    previous_text,
                    (
                        WIDTH // 2 - previous_text.get_width() // 2,
                        HEIGHT // 3 + 40 * (j + 1)
                    )
                )

            # Linha atual
            window.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 3 + 40 * (i + 1)
                )
            )

            # Texto inferior
            window.blit(
                inicio,
                (
                    WIDTH // 2 - inicio.get_width() // 2,
                    HEIGHT - 80
                )
            )

            pygame.display.flip()
            clock.tick(60)

    # Espera clique ou tecla
    waiting = True

    while waiting:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                waiting = False

        # Garante que a música comece mesmo se ainda não começou
        if not musica_iniciada and pygame.time.get_ticks() - tempo_inicio >= 2000:

            pygame.mixer.music.load(musica_fundo)
            pygame.mixer.music.play(-1)

            musica_iniciada = True

        # Redesenha tela
        window.blit(imagem_fundo, (0, 0))

        window.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4)
        )

        for j, linha in enumerate(acontecimento):

            texto = font.render(
                linha,
                True,
                (255, 255, 255)
            )

            window.blit(
                texto,
                (
                    WIDTH // 2 - texto.get_width() // 2,
                    HEIGHT // 3 + 40 * (j + 1)
                )
            )

        window.blit(
            inicio,
            (
                WIDTH // 2 - inicio.get_width() // 2,
                HEIGHT - 80
            )
        )

        pygame.display.flip()
        clock.tick(60)

    import jogo


entrega_concluida()