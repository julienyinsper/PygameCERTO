import pygame

pygame.init()
pygame.mixer.init()

# Configuração da tela
WIDTH = 900
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entregando")

#Cores
BRANCO = (255, 255, 255)
AMARELO = (255, 215, 0)
PRETO = (0, 0, 0)

# Fundo
fundo = pygame.image.load("Assets/Imagens/Passounivel.png").convert()
fundo = pygame.transform.scale(fundo, (WIDTH, HEIGHT))

# Sons
som_yay = pygame.mixer.Sound("Assets/Sons/Yay.mp3")
musica_fundo = "Assets/Sons/Telainicio.mp3"

# Função tela
def prox_nivel():
    running = True
    musica_tocando = False
    tempo_inicio = pygame.time.get_ticks()

    # toca o yay assim que a tela abre
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
        "Pressione qualquer tecla para continuar",
        True,
        BRANCO
    )

    clock = pygame.time.Clock()

    while running:
        agora = pygame.time.get_ticks()

        # depois de 1 segundo, inicia a música
        if not musica_tocando and agora - tempo_inicio >= 1000:
            pygame.mixer.music.load(musica_fundo)
            pygame.mixer.music.play(-1)
            musica_tocando = True

        # desenha a tela imediatamente, sem delay
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
                exit()

            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                running = False

        clock.tick(60)

prox_nivel()

pygame.quit()