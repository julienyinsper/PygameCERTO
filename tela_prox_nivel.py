import pygame
import time

pygame.init()

# Tela principal
WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Entregando')

# ----- CORES
BRANCO = (255, 255, 255)
AMARELO = (255, 215, 0)
PRETO = (0, 0, 0)

# Carega imagens
fundo = pygame.image.load('Assets/Imagens/fundo_inicio.png').convert()
fundo = pygame.transform.scale(fundo, (WIDTH, HEIGHT))

entregador_img = pygame.image.load('Assets/Imagens/Entregador.png').convert_alpha()
cliente_img = pygame.image.load('Assets/Imagens/Cliente.png').convert_alpha()

# Redimensiona se quiser
entregador_img = pygame.transform.scale(entregador_img, (150, 150))
cliente_img = pygame.transform.scale(cliente_img, (130, 130))

# Som
try:
    pygame.mixer.music.load('Assets/Sons/Trilhasonora.mp3')
    pygame.mixer.music.play(-1)
except:
    pass

# Função tela próximo nível
def prox_nivel():
    running = True

    title_font = pygame.font.SysFont(None, 72)
    text_font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 28)

    title = title_font.render("Pedido entregue!", True, AMARELO)

    mensagens = [
        "Você desviou dos carros e chegou ao cliente.",
        "A entrega foi concluída com sucesso!",
        "Prepare-se para a próxima corrida pela cidade."
    ]

    instrucao = small_font.render("Pressione qualquer tecla ou clique para continuar.", True, BRANCO)

    while running:
        window.blit(fundo, (0, 0))

        # Faixa escura para destacar o texto
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        window.blit(overlay, (0, 0))

        # Título
        window.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

        # Texto central
        for i, msg in enumerate(mensagens):
            text = text_font.render(msg, True, BRANCO)
            window.blit(text, (WIDTH // 2 - text.get_width() // 2, 210 + i * 45))

        window.blit(instrucao, (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT - 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                running = False

prox_nivel()