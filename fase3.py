# Importa bibliotecas
import pygame
import random
import os
import sys
# Importa telas
from perdeu import perdeu
from ganhou import ganhou

# Função principal fase 3
def fase3():
    # Inicia Pygame
    pygame.init()
    # Inicia sistema e áudio
    try:
        pygame.mixer.init()
    except:
        # Se o áudio falhar, o jogo continua
        pass

# Configurações da tela
    LARGURA = 900
    ALTURA = 600
    FPS = 30

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Entregando - Fase 3")
    # Controla os FPS
    clock = pygame.time.Clock()

    # Caminho pasta imagens e sons
    pasta_imagens = os.path.join("Assets", "Imagens")
    pasta_sons = os.path.join("Assets", "Sons")

    # Função para carregar imagens e sons 
    def carregar_imagem(nome, tamanho=None, alpha=True):
        caminho = os.path.join(pasta_imagens, nome)

        if alpha:
            imagem = pygame.image.load(caminho).convert_alpha() # Com transparência
        else:
            imagem = pygame.image.load(caminho).convert() # Sem transparência
        # Redimensiona a imagem se necessário
        if tamanho is not None:
            imagem = pygame.transform.scale(imagem, tamanho)
        # Retorna imagem pronta
        return imagem
    # Função para carregar sons
    def carregar_som(nome):
        caminho = os.path.join(pasta_sons, nome)
        try:
            return pygame.mixer.Sound(caminho)
        except:
            # Se falhar, retorna vazio, mas o jogo continua
            return None

    # Carrega fundo
    fundo = carregar_imagem("Rua.png", (LARGURA, ALTURA), alpha=False)
    fundo_y = 0
    velocidade_fundo = 10

    # Carrega pessoas
    img_entregador = carregar_imagem("Entregador.png", (100, 70))
    img_cliente = carregar_imagem("Cliente.png", (120, 80))

    # Carrega carros
    imagens_carros = [
        carregar_imagem("Carro_amarelo.png", (80, 140)),
        carregar_imagem("Carro_azul.png", (80, 140)),
        carregar_imagem("Carro_vermelho.png", (80, 140))
    ]

    # Carrega sons Yay e trilha sonora
    som_yay = carregar_som("Yay.mp3")

    try:
        pygame.mixer.music.load(os.path.join(pasta_sons, "Trilhasonora.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except:
        pass

    # Rua configurações
    ROAD_LEFT = 300
    ROAD_RIGHT = 680
    ROAD_CENTER = (ROAD_LEFT + ROAD_RIGHT) // 2
    # Faixas da rua
    LANE_XS = [
        ROAD_LEFT + 55,
        ROAD_CENTER,
        ROAD_RIGHT - 55
    ]

    velocidades_faixas = {}
    # Define velocidade para cada faixa
    for lane_x in LANE_XS:
        velocidades_faixas[lane_x] = random.randint(10, 15)

    DISTANCIA_ENTRE_CARROS = 420

    # Classes para entregador, carros e cliente
    class Entregador(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = img_entregador
            self.rect = self.image.get_rect()
            self.rect.centerx = ROAD_CENTER
            self.rect.bottom = ALTURA - 20
            self.speedx = 0
            self.speedy = 0
            self.mask = pygame.mask.from_surface(self.image)
        # Atualiza posição
        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            # Limita o jogador dentro da estrada
            if self.rect.left < ROAD_LEFT:
                self.rect.left = ROAD_LEFT
            if self.rect.right > ROAD_RIGHT:
                self.rect.right = ROAD_RIGHT
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > ALTURA:
                self.rect.bottom = ALTURA

    class Carro(pygame.sprite.Sprite):
        def __init__(self, lane_x, posicao_na_faixa):
            super().__init__()
            # Faixa onde o carro estará e posição para evitar que dois carros fiquem muito próximos
            self.lane_x = lane_x
            self.posicao_na_faixa = posicao_na_faixa
            self.image = random.choice(imagens_carros)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.speedy = velocidades_faixas[self.lane_x]
            self.rect.centerx = self.lane_x
            self.rect.y = -200 - self.posicao_na_faixa * DISTANCIA_ENTRE_CARROS

        # Reinicia carro e aparece na rua 
        def reset(self):
            self.image = random.choice(imagens_carros)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.speedy = velocidades_faixas[self.lane_x]
            self.rect.centerx = self.lane_x
            self.rect.y = random.randint(-900, -300)
            # Impede que dois carros apareçam muito próximos um do outro
            for outro_carro in grupo_carros:
                if outro_carro != self and outro_carro.lane_x == self.lane_x:
                    while abs(self.rect.y - outro_carro.rect.y) < DISTANCIA_ENTRE_CARROS:
                        self.rect.y -= DISTANCIA_ENTRE_CARROS
        # Movimento do carro
        def update(self):
            self.rect.y += self.speedy
            # Reinicia o carro ao sair da tela
            if self.rect.top > ALTURA:
                self.reset()

    class Cliente(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = img_cliente
            self.rect = self.image.get_rect()
            # Posiciona no centro da rua, mas mais próximo do topo
            self.rect.centerx = ROAD_CENTER
            self.rect.top = 20
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            pass

    # Grupos de sprites
    todos_sprites = pygame.sprite.Group()
    grupo_carros = pygame.sprite.Group()

    # Criação dos personagens
    jogador = Entregador()
    cliente = Cliente()

    todos_sprites.add(jogador)
    todos_sprites.add(cliente)

    # Cria 2 carros por faixa
    for lane_x in LANE_XS:
        for posicao in range(2):
            carro = Carro(lane_x, posicao)
            todos_sprites.add(carro)
            grupo_carros.add(carro)

    # Loop principal fase 3 
    rodando = True

    while rodando:
        clock.tick(FPS)
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Controle do jogador
        teclas = pygame.key.get_pressed()

        jogador.speedx = 0
        jogador.speedy = 0
        # Movimento para esquerda
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogador.speedx = -7
        # Movimento para direita
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogador.speedx = 7
        # Movimento para cima
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jogador.speedy = -7
        # Movimento para baixo
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jogador.speedy = 7

        # Atualiza sprites
        todos_sprites.update()

        # Movimento do fundo
        fundo_y += velocidade_fundo
        if fundo_y >= ALTURA:
            fundo_y = 0

        # Colisão com carros = perdeu
        if pygame.sprite.spritecollide(jogador, grupo_carros, False, pygame.sprite.collide_mask):
            # Para a música
            try:
                pygame.mixer.music.stop()
            except:
                pass
            # Mostra tela de derrota
            perdeu()
            return

        # Encostou no cliente = ganhou
        if jogador.rect.colliderect(cliente.rect):
            # Para a música
            try:
                pygame.mixer.music.stop()
            except:
                pass
            # Toca som de vitória
            if som_yay is not None:
                som_yay.play()
            # Mostra tela de vitória
            ganhou()
            return

        # Desenho
        tela.blit(fundo, (0, fundo_y))
        tela.blit(fundo, (0, fundo_y - ALTURA))

        todos_sprites.draw(tela)
        # Cria fonte do texto da fase
        fonte = pygame.font.SysFont(None, 32)
        texto = fonte.render(
            "Fase 3 - Entregue o pedido ao cliente!",
            True,
            (255, 255, 255)
        )
        tela.blit(texto, (20, 20))

        pygame.display.update()
    # Encerra o Pygame ao sair do loop
    pygame.quit()

# Executa se o arquivo for aberto diretamente
if __name__ == "__main__":
    fase3()