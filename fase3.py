
import pygame
import random
import os
import sys

def fase3():
    pygame.init()

    try:
        pygame.mixer.init()
    except:
        pass

    LARGURA = 900
    ALTURA = 600
    FPS = 30

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Entregando - Fase 3")
    clock = pygame.time.Clock()

    pasta_imagens = os.path.join("Assets", "Imagens")
    pasta_sons = os.path.join("Assets", "Sons")

    def carregar_imagem(nome, tamanho=None, alpha=True):
        caminho = os.path.join(pasta_imagens, nome)

        if alpha:
            imagem = pygame.image.load(caminho).convert_alpha()
        else:
            imagem = pygame.image.load(caminho).convert()

        if tamanho is not None:
            imagem = pygame.transform.scale(imagem, tamanho)

        return imagem

    def carregar_som(nome):
        caminho = os.path.join(pasta_sons, nome)
        try:
            return pygame.mixer.Sound(caminho)
        except:
            return None

    def tocar_som(som):
        if som is not None:
            som.play()

    # ---------- Imagens ----------
    fundo = carregar_imagem("Rua.png", (LARGURA, ALTURA), alpha=False)

    fundo_y = 0
    velocidade_fundo = 10

    img_entregador = carregar_imagem("Entregador.png", (100, 70))
    img_cliente = carregar_imagem("Cliente.png", (120, 80))

    imagens_carros = [
        carregar_imagem("Carro_amarelo.png", (80, 140)),
        carregar_imagem("Carro_azul.png", (80, 140)),
        carregar_imagem("Carro_vermelho.png", (80, 140))
    ]

    tela_ganhou = carregar_imagem("Ganhou.png", (LARGURA, ALTURA), alpha=False)
    tela_perdeu = carregar_imagem("Perdeu.png", (LARGURA, ALTURA), alpha=False)

    # ---------- Sons ----------
    som_perdeu = carregar_som("Perdeu.mp3")
    som_ganhou = carregar_som("Ganhou.mp3")
    som_yay = carregar_som("Yay.mp3")

    try:
        pygame.mixer.music.load(os.path.join(pasta_sons, "Trilhasonora.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except:
        pass

    # ---------- Rua ----------
    ROAD_LEFT = 300
    ROAD_RIGHT = 680
    ROAD_CENTER = (ROAD_LEFT + ROAD_RIGHT) // 2

    LANE_XS = [
        ROAD_LEFT + 55,
        ROAD_CENTER,
        ROAD_RIGHT - 55
    ]

    # Velocidade da fase 3:
    # fase 2 era 10 a 15, então aqui está um pouco mais rápido.
    velocidades_faixas = {}

    for lane_x in LANE_XS:
        velocidades_faixas[lane_x] = random.randint(12, 17)

    DISTANCIA_ENTRE_CARROS = 420

    # ---------- Classes ----------
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

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy

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

            self.lane_x = lane_x
            self.posicao_na_faixa = posicao_na_faixa

            self.image = random.choice(imagens_carros)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

            self.speedy = velocidades_faixas[self.lane_x]

            self.rect.centerx = self.lane_x
            self.rect.y = -200 - self.posicao_na_faixa * DISTANCIA_ENTRE_CARROS

        def reset(self):
            self.image = random.choice(imagens_carros)
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)

            self.speedy = velocidades_faixas[self.lane_x]
            self.rect.centerx = self.lane_x

            # Volta bem para cima, mantendo distância.
            self.rect.y = random.randint(-900, -300)

            # Verifica se tem outro carro perto na mesma faixa.
            for outro_carro in grupo_carros:
                if outro_carro != self and outro_carro.lane_x == self.lane_x:
                    while abs(self.rect.y - outro_carro.rect.y) < DISTANCIA_ENTRE_CARROS:
                        self.rect.y -= DISTANCIA_ENTRE_CARROS

        def update(self):
            self.rect.y += self.speedy

            if self.rect.top > ALTURA:
                self.reset()

    class Cliente(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()

            self.image = img_cliente
            self.rect = self.image.get_rect()
            self.rect.centerx = ROAD_CENTER

            # Quanto mais negativo, mais tempo a fase dura.
            self.rect.top = -3500

            self.speedy = 3

        def update(self):
            self.rect.y += self.speedy

            if self.rect.top >= 10:
                self.rect.top = 10

    # ---------- Tela final ----------
    def mostrar_tela_final(imagem, som=None):
        pygame.mixer.music.stop()
        tocar_som(som)

        esperando = True

        while esperando:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False

            tela.blit(imagem, (0, 0))

            fonte = pygame.font.SysFont(None, 32)
            texto = fonte.render(
                "Clique ou aperte qualquer tecla para continuar",
                True,
                (255, 255, 255)
            )

            tela.blit(
                texto,
                (LARGURA // 2 - texto.get_width() // 2, ALTURA - 50)
            )

            pygame.display.update()

    # ---------- Grupos ----------
    todos_sprites = pygame.sprite.Group()
    grupo_carros = pygame.sprite.Group()

    jogador = Entregador()
    cliente = Cliente()

    todos_sprites.add(jogador)
    todos_sprites.add(cliente)

    # Dois carros por faixa, mas espaçados.
    for lane_x in LANE_XS:
        for posicao in range(2):
            carro = Carro(lane_x, posicao)
            todos_sprites.add(carro)
            grupo_carros.add(carro)

    # ---------- Loop principal ----------
    rodando = True
    ganhou = False
    perdeu = False

    while rodando:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()

        jogador.speedx = 0
        jogador.speedy = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogador.speedx = -7

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogador.speedx = 7

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jogador.speedy = -7

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jogador.speedy = 7

        todos_sprites.update()

        # Movimento da rua
        fundo_y += velocidade_fundo

        if fundo_y >= ALTURA:
            fundo_y = 0

        # Colisão com carros
        if pygame.sprite.spritecollide(jogador, grupo_carros, False, pygame.sprite.collide_mask):
            perdeu = True
            rodando = False
            continue

        # Vitória ao encostar no cliente
        if jogador.rect.colliderect(cliente.rect):
            ganhou = True
            rodando = False
            continue

        # Desenho do fundo em movimento
        tela.blit(fundo, (0, fundo_y))
        tela.blit(fundo, (0, fundo_y - ALTURA))

        todos_sprites.draw(tela)

        fonte = pygame.font.SysFont(None, 32)
        texto = fonte.render(
            "Fase 3 - Entregue o pedido ao cliente!",
            True,
            (255, 255, 255)
        )
        tela.blit(texto, (20, 20))

        pygame.display.update()

    if perdeu:
        mostrar_tela_final(tela_perdeu, som_perdeu)
        fase3()

    elif ganhou:
        tocar_som(som_yay)
        mostrar_tela_final(tela_ganhou, som_ganhou)

    pygame.quit()


if __name__ == "__main__":
    fase3()