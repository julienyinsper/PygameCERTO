
import pygame
import random
import os

def fase3():
    pygame.init()
    pygame.mixer.init()

    LARGURA = 900
    ALTURA = 600
    FPS = 60

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Entregando - Fase 3")

    clock = pygame.time.Clock()

    # Caminhos das pastas
    pasta_imagens = os.path.join("Assets", "Imagens")
    pasta_sons = os.path.join("Assets", "Sons")

    # ---------- Funções auxiliares ----------
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

    # ---------- Carregando imagens ----------
    fundo = carregar_imagem("Rua.png", (LARGURA, ALTURA), alpha=False)

    fundo_y1 = 0
    fundo_y2 = -ALTURA
    velocidade_fundo = 5

    img_entregador = carregar_imagem("Entregador.png", (90, 110))
    img_cliente = carregar_imagem("Cliente.png", (100, 120))

    imagens_carros = [
        carregar_imagem("Carro_amarelo.png", (90, 150)),
        carregar_imagem("Carro_azul.png", (90, 150)),
        carregar_imagem("Carro_vermelho.png", (90, 150))
    ]

    tela_ganhou = carregar_imagem("Ganhou.png", (LARGURA, ALTURA), alpha=False)
    tela_perdeu = carregar_imagem("Perdeu.png", (LARGURA, ALTURA), alpha=False)

    # ---------- Carregando sons ----------
    som_perdeu = carregar_som("Perdeu.mp3")
    som_ganhou = carregar_som("Ganhou.mp3")
    som_yay = carregar_som("Yay.mp3")

    try:
        pygame.mixer.music.load(os.path.join(pasta_sons, "Trilhasonora.mp3"))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except:
        pass

    # ---------- Classes ----------
    class Entregador(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = img_entregador
            self.rect = self.image.get_rect()
            self.rect.centerx = LARGURA // 2
            self.rect.bottom = ALTURA - 20
            self.velocidade = 7

        def update(self):
            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                self.rect.x -= self.velocidade
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                self.rect.x += self.velocidade
            if teclas[pygame.K_UP] or teclas[pygame.K_w]:
                self.rect.y -= self.velocidade
            if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
                self.rect.y += self.velocidade

            # Mantém o entregador dentro da tela
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > LARGURA:
                self.rect.right = LARGURA
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > ALTURA:
                self.rect.bottom = ALTURA

    class Carro(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.image = random.choice(imagens_carros)
            self.rect = self.image.get_rect()

            faixas = [250, 360, 480, 600]
            self.rect.centerx = random.choice(faixas)
            self.rect.y = random.randint(-900, -100)

            # Velocidade da fase 3
            self.velocidade = random.randint(7, 12)

        def update(self):
            self.rect.y += self.velocidade

            if self.rect.top > ALTURA:
                self.image = random.choice(imagens_carros)
                self.rect = self.image.get_rect()

                faixas = [250, 360, 480, 600]
                self.rect.centerx = random.choice(faixas)
                self.rect.y = random.randint(-900, -150)
                self.velocidade = random.randint(8, 14)

    class Cliente(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.image = img_cliente
            self.rect = self.image.get_rect()
            self.rect.centerx = LARGURA // 2

            # Quanto mais negativo, mais tempo a fase dura
            self.rect.top = -3000

            # Velocidade com que o cliente vai aparecendo
            self.velocidade = 3

        def update(self):
            self.rect.y += self.velocidade

            # Quando chegar no topo da tela, ele para
            if self.rect.top >= 20:
                self.rect.top = 20

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
                    return "sair"

                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    esperando = False

            tela.blit(imagem, (0, 0))

            fonte = pygame.font.SysFont(None, 32)
            texto = fonte.render("Clique ou aperte qualquer tecla para continuar", True, (255, 255, 255))
            tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA - 50))

            pygame.display.update()

        return "continuar"

    # ---------- Grupos ----------
    todos_sprites = pygame.sprite.Group()
    grupo_carros = pygame.sprite.Group()

    jogador = Entregador()
    cliente = Cliente()

    todos_sprites.add(jogador)
    todos_sprites.add(cliente)

    # Mais carros na fase 3 para deixar mais difícil
    for i in range(7):
        carro = Carro()
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
                rodando = False

        # Movimento vertical da rua
        fundo_y1 += velocidade_fundo
        fundo_y2 += velocidade_fundo

        if fundo_y1 >= ALTURA:
            fundo_y1 = -ALTURA
        if fundo_y2 >= ALTURA:
            fundo_y2 = -ALTURA

        # Atualiza sprites
        todos_sprites.update()

        # Colisão com os carros
        if pygame.sprite.spritecollide(jogador, grupo_carros, False):
            perdeu = True
            rodando = False

        # Colisão com o cliente
        if jogador.rect.colliderect(cliente.rect):
            ganhou = True
            rodando = False

        # Desenha fundo
        tela.blit(fundo, (0, fundo_y1))
        tela.blit(fundo, (0, fundo_y2))

        # Desenha sprites
        todos_sprites.draw(tela)

        # Texto da fase
        fonte = pygame.font.SysFont(None, 32)
        texto = fonte.render("Fase 3 - Entregue o pedido ao cliente!", True, (255, 255, 255))
        tela.blit(texto, (20, 20))

        pygame.display.update()

    # ---------- Resultado ----------
    if perdeu:
        resultado = mostrar_tela_final(tela_perdeu, som_perdeu)

        if resultado == "continuar":
            fase3()

    elif ganhou:
        tocar_som(som_yay)
        mostrar_tela_final(tela_ganhou, som_ganhou)

    pygame.quit()


fase3()