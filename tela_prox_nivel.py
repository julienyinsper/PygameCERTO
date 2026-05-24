import pygame
import sys

pygame.init()

try:
    pygame.mixer.init()
except:
    pass

# Configuração da tela
WIDTH = 900
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entregando")

# Cores
BRANCO = (255, 255, 255)
AMARELO = (255, 215, 0)
PRETO = (0, 0, 0)

# Fundo
fundo = pygame.image.load("Assets/Imagens/Passounivel.png").convert()
fundo = pygame.transform.scale(fundo, (WIDTH, HEIGHT))

# Sons
try:
    som_yay = pygame.mixer.Sound("Assets/Sons/Yay.mp3")
except:
    som_yay = None

musica_fundo = "Assets/Sons/Telainicio.mp3"


def tela_prox_nivel():
    running = True
    musica_tocando = False
    tempo_inicio = pygame.time.get_ticks()

    # toca o yay assim que a tela abre
    if som_yay is not None:
        som_yay.play()

    # Fontes
    title_font = pygame.font.SysFont(None, 72)
    text_font = pygame.font.SysFont(None, 38)
    small_font = pygame.font.SysFont(None, 28)

    titulo = title_font.render("ENTREGA CONCLUÍDA!", True, AMARELO)

    mensagens = [
        "Parabéns!",
        "Você desviou dos carros com sucesso.",
        "Prepare-se para a próxima entrega!"
    ]

    instrucao = small_font.render(
        "Pressione qualquer tecla ou clique para continuar",
        True,
        BRANCO
    )

    clock = pygame.time.Clock()

    while running:
        agora = pygame.time.get_ticks()

        # depois de 2 segundos, inicia a música
        if not musica_tocando and agora - tempo_inicio >= 2000:
            try:
                pygame.mixer.music.load(musica_fundo)
                pygame.mixer.music.play(-1)
            except:
                pass
            musica_tocando = True

        # desenha a tela
        window.blit(fundo, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill(PRETO)
        window.blit(overlay, (0, 0))

        window.blit(
            titulo,
            (WIDTH // 2 - titulo.get_width() // 2, 100)
        )

        for i, msg in enumerate(mensagens):
            texto = text_font.render(msg, True, BRANCO)
            window.blit(
                texto,
                (WIDTH // 2 - texto.get_width() // 2, 250 + i * 50)
            )

        window.blit(
            instrucao,
            (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT - 80)
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                running = False

        clock.tick(60)


if __name__ == "__main__":
    tela_prox_nivel()