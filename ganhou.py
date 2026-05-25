# Importa bibliotecas
import pygame
import sys
# Inicia Pygame
pygame.init()
# Inicia sistema e áudio
try:
    pygame.mixer.init()
except:
    # Se o áudio falhar, o jogo continua
    pass

# Tela configurações
WIDTH = 900
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Entregando")
clock = pygame.time.Clock()

# Fundo imagem
imagem_fundo = pygame.image.load("Assets/Imagens/Ganhou.png").convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))

# Sons
try:
    som_ganhou = pygame.mixer.Sound("Assets/Sons/Ganhou.mp3")
except:
    # Se der erro, não usa som
    som_ganhou = None
# Caminho da música de fundo para tocar depois do som de ganhou
musica_fundo = "Assets/Sons/Telainicio.mp3"

# Função para desenhar a tela 
def desenhar_tela():
    window.blit(imagem_fundo, (0, 0))
    # Fontes para os textos
    title_font = pygame.font.SysFont(None, 72)
    font = pygame.font.SysFont(None, 40)
    font_inicio = pygame.font.SysFont(None, 30)
    # Textos da tela 
    title = title_font.render("Você ganhou!", True, (255, 215, 0))
    linha1 = font.render("O entregador passou todas as fases", True, (255, 255, 255))
    linha2 = font.render("e chegou ao cliente com sucesso!", True, (255, 255, 255))
    inicio = font_inicio.render("Clique para continuar o jogo.", True, (255, 255, 255))
    # Posiciona os textos na tela
    window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    window.blit(linha1, (WIDTH // 2 - linha1.get_width() // 2, HEIGHT // 2 - 10))
    window.blit(linha2, (WIDTH // 2 - linha2.get_width() // 2, HEIGHT // 2 + 35))
    window.blit(inicio, (WIDTH // 2 - inicio.get_width() // 2, HEIGHT - 80))
    # Atualiza a tela
    pygame.display.flip()

# Função principal 
def ganhou():
    # Toca o som de vitória se ele foi carregado corretamente
    if som_ganhou is not None:
        som_ganhou.play()
    # Marca o tempo inicial da tela
    tempo_inicio = pygame.time.get_ticks()
    # Controla se a música já começou
    musica_iniciada = False
    # Mantém a tela aberta até interação do jogador
    waiting = True
    
    while waiting:
        for event in pygame.event.get():
            # Fecha jogo
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Sai da tela ao apertar qualquer tecla ou clicar com o mouse
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                waiting = False

        # Espera 2 segundos para tocar a música
        if not musica_iniciada and pygame.time.get_ticks() - tempo_inicio >= 2000:
            try:
                pygame.mixer.music.load(musica_fundo)
                pygame.mixer.music.play(-1)
            except:
                pass
            musica_iniciada = True

        desenhar_tela()
        clock.tick(60)
    # Importa o jogo principal ao sair da tela de vitória
    import jogo

# Executa se o arquivo for aberto diretamente
if __name__ == "__main__":
    ganhou()