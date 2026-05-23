import pygame
import sys

pygame.init()
pygame.mixer.init()

# Tela
WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entregando")
clock = pygame.time.Clock()

# Fundo
imagem_fundo = pygame.image.load('Assets/Imagens/Perdeu.png').convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))

# Sons
som_perdeu = pygame.mixer.Sound("Assets/Sons/Perdeu.mp3")
musica_fundo = "Assets/Sons/Telainicio.mp3"

def desenhar_tela():
    window.blit(imagem_fundo, (0, 0))

    title_font = pygame.font.SysFont(None, 72)
    font = pygame.font.SysFont(None, 40)
    font_inicio = pygame.font.SysFont(None, 30)

    title = title_font.render("Entrega atrasada!", True, (255, 215, 0))
    linha2 = font.render("A entrega nao chegou ao cliente.", True, (255, 255, 255))
    inicio = font_inicio.render("Clique para jogar novamente.", True, (255, 255, 255))

    window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    window.blit(linha2, (WIDTH // 2 - linha2.get_width() // 2, HEIGHT // 3 + 50))
    window.blit(inicio, (WIDTH // 2 - inicio.get_width() // 2, HEIGHT - 80))

    pygame.display.flip()

def perdeu_entrega():
    # Mostra a tela primeiro
    desenhar_tela()

    # Toca o som de perdeu
    som_perdeu.play()

    # Espera 2 segundos sem travar a janela
    inicio_tempo = pygame.time.get_ticks()
    musica_iniciada = False

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                waiting = False

        # Depois de 2 segundos, começa a música da tela inicial
        if not musica_iniciada and pygame.time.get_ticks() - inicio_tempo >= 2000:
            pygame.mixer.music.load(musica_fundo)
            pygame.mixer.music.play(-1)
            musica_iniciada = True

        desenhar_tela()
        clock.tick(60)

perdeu_entrega()