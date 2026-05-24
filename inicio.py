import pygame
import sys

pygame.init()

# Gera tela principal
WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entregando")

# Carrega a imagem de fundo
imagem_fundo = pygame.image.load('Assets/Imagens/fundo_inicio.png').convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))
imagem_fundo_rect = imagem_fundo.get_rect()


def inicio():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('Assets/Sons/Telainicio.mp3')
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except:
        pass

    window.blit(imagem_fundo, imagem_fundo_rect)

    title_font = pygame.font.SysFont(None, 72)
    title = title_font.render("Entregando", True, (255, 165, 0))

    font = pygame.font.SysFont(None, 40)
    story = [
        "Em uma cidade movimentada e com trânsito",
        "Você é um entregador de pizza que",
        "precisa correr contra o tempo para",
        "fazer suas entregas quentinhas",
        "Desvie dos carros, sobreviva ao trânsito",
        "e entregue as pizzas o mais rápido possível!",
    ]

    font_inicio = pygame.font.SysFont(None, 30)
    inicio_texto = font_inicio.render(
        "Clique em qualquer botão para iniciar o jogo.",
        True,
        (255, 255, 255)
    )

    window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    pygame.display.flip()

    for i, line in enumerate(story):
        rendered_line = ""
        for char in line:
            rendered_line += char
            text = font.render(rendered_line, True, (255, 255, 255))

            window.blit(imagem_fundo, imagem_fundo_rect)
            window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

            for j in range(i):
                previous_text = font.render(story[j], True, (255, 255, 255))
                window.blit(
                    previous_text,
                    (WIDTH // 2 - previous_text.get_width() // 2, HEIGHT // 3 + 40 * (j + 1))
                )

            window.blit(
                text,
                (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + 40 * (i + 1))
            )

            pygame.display.flip()
            pygame.time.wait(50)

    window.blit(inicio_texto, (WIDTH // 2 - inicio_texto.get_width() // 2, HEIGHT - 80))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

    return


if __name__ == "__main__":
    inicio()