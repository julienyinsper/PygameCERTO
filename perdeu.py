# Importa bibliotecas
import pygame
import sys
# Inicia Pygame
pygame.init()
# Inicia sistema e áudio
try:
    pygame.mixer.init()
# Caso o áudio falhe, o jogo continua funcionando
except:
    pass

# Tela configurações
WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entregando")
# Controla os FPS do jogo
clock = pygame.time.Clock()

# Fundo
imagem_fundo = pygame.image.load('Assets/Imagens/Perdeu.png').convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))

# Carregamento sons
try:
    som_perdeu = pygame.mixer.Sound("Assets/Sons/Perdeu.mp3")
# Se houver erro, o som fica vazio, mas o jogo continua
except:
    som_perdeu = None
# Caminho da música de fundo para tocar depois do som de perdeu
musica_fundo = "Assets/Sons/Telainicio.mp3"

# Função para desenhar a tela
def desenhar_tela():
    window.blit(imagem_fundo, (0, 0))
    # Fontes para os textos
    title_font = pygame.font.SysFont(None, 72)
    font = pygame.font.SysFont(None, 40)
    font_inicio = pygame.font.SysFont(None, 30)
    # Textos da tela
    title = title_font.render("Entrega atrasada!", True, (255, 215, 0))
    linha2 = font.render("A entrega não chegou ao cliente.", True, (255, 255, 255))
    # Instrução para reiniciar o jogo
    inicio = font_inicio.render("Clique para jogar novamente.", True, (255, 255, 255))
    # Centraliza e desenha o título e os textos
    window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    window.blit(linha2, (WIDTH // 2 - linha2.get_width() // 2, HEIGHT // 3 + 50))
    window.blit(inicio, (WIDTH // 2 - inicio.get_width() // 2, HEIGHT - 80))
    # Atualiza tudo que foi desenhado
    pygame.display.flip()

# Função principal
def perdeu():
    desenhar_tela()
    # Verifica se o som foi carregado corretamente
    if som_perdeu is not None:
        # Toca o som de perdeu
        som_perdeu.play()
    # Marca o tempo inicial da tela
    inicio_tempo = pygame.time.get_ticks()
    # Indica se a música de fundo já começou
    musica_iniciada = False

    # Espera por clique para reiniciar o jogo
    waiting = True
    while waiting:
        for event in pygame.event.get():
            # Fecha o jogo se o usuário clicar no X
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Reinicia o jogo ao clicar ou pressionar qualquer tecla
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                waiting = False
        # Espera 2 segundos antes de tocar a música
        if not musica_iniciada and pygame.time.get_ticks() - inicio_tempo >= 2000:
            # Carrega e toca a música de fundo em loop
            try:
                pygame.mixer.music.load(musica_fundo)
                pygame.mixer.music.play(-1)
            except:
                # Ignora erros de áudio
                pass
            # Marca que a música começou para não tentar tocar de novo
            musica_iniciada = True
        # Atualiza os elementos visuais
        desenhar_tela()
        clock.tick(60)

# Executa ao chamar o arquivo diretamente
if __name__ == "__main__":
    perdeu()