# Importa bibliotecas
import pygame
import sys
# Inicia Pygame
pygame.init()
# Incia sistema e áudio
try:
    pygame.mixer.init()
# Continua o jogo se der erro
except:
    pass

# Configuração da tela
WIDTH = 900
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entregando")

# Define cores
BRANCO = (255, 255, 255)
AMARELO = (255, 215, 0)
PRETO = (0, 0, 0)

# Fundo
fundo = pygame.image.load("Assets/Imagens/Passounivel.png").convert()
fundo = pygame.transform.scale(fundo, (WIDTH, HEIGHT))

# Sons
try:
    som_yay = pygame.mixer.Sound("Assets/Sons/Yay.mp3")
# Se der erro, fica sem som, mas o jogo continua
except:
    som_yay = None
# Caminho música de fundo para tocar depois do yay
musica_fundo = "Assets/Sons/Telainicio.mp3"

# Função principal
def tela_prox_nivel():
    # Controla o loop da tela
    running = True
    # Indica se a música já começou
    musica_tocando = False
    # Marca o tempo em que a tela abriu
    tempo_inicio = pygame.time.get_ticks()

    # Toca o yay assim que a tela abre
    if som_yay is not None:
        som_yay.play()

    # Fontes
    title_font = pygame.font.SysFont(None, 72)
    text_font = pygame.font.SysFont(None, 38)
    small_font = pygame.font.SysFont(None, 28)

    # Textos da tela
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
    # Controla o FPS do jogo
    clock = pygame.time.Clock()

    while running:
        # Obtém o tempo atual
        agora = pygame.time.get_ticks()

        # Depois de 2 segundos, inicia a música
        if not musica_tocando and agora - tempo_inicio >= 2000:
            try:
                # Carrega música de fundo e toca em loop
                pygame.mixer.music.load(musica_fundo)
                pygame.mixer.music.play(-1)
            except:
                pass
            # Marca que a música já começou para não tentar tocar de novo
            musica_tocando = True

        # Desenha a tela
        window.blit(fundo, (0, 0))
        # Sobreposição para destacar os textos
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill(PRETO)
        window.blit(overlay, (0, 0))
        # Centraliza e desenha o título 
        window.blit(
            titulo,
            (WIDTH // 2 - titulo.get_width() // 2, 100)
        )
        # Centraliza e desenha as mensagens
        for i, msg in enumerate(mensagens):
            texto = text_font.render(msg, True, BRANCO)
            window.blit(
                texto,
                (WIDTH // 2 - texto.get_width() // 2, 250 + i * 50)
            )
        # Centraliza e desenha a instrução
        window.blit(
            instrucao,
            (WIDTH // 2 - instrucao.get_width() // 2, HEIGHT - 80)
        )

        # Atualiza tudo que foi desenhado
        pygame.display.flip()
        # Fecha jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                running = False
        
        clock.tick(60)

# Executa se o arquivo for iniciado diretamente
if __name__ == "__main__":
    tela_prox_nivel()