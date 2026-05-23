
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

    # ---------- Sons ----------
    som_perdeu = carregar_som("Perdeu.mp3")
    som_ganhou = carregar_som("Ganhou.mp3")
    som_yay = carregar_som("Yay.mp3")

    try:
        pygame.mixer.music.load(os.path.join(pasta_sons, "Trilhasonora.mp3"))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
    except:
        pass

    # ---------- Variáveis dos carros ----------
    faixas = [250, 360, 480, 600]
    distancia_minima_carros = 230

    def posicao_segura_carro(grupo_carros):
        tentativa = 0

        while tentativa < 100:
            x = random.choice(faixas)
            y = random.randint(-1000, -150)

            pode_colocar = True

            for carro in grupo_carros:
                mesma_faixa = abs(carro.rect.centerx - x) < 20
                muito_perto = abs(carro.rect.y - y) < distancia_minima_carros

                if mesma_faixa and muito_perto:
                    pode_colocar = False
                    break

            if pode_colocar:
                return x, y

            tentativa += 1

        return random.choice(faixas), random.randint(-1200, -900)

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

            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.right > LARGURA:
                self.rect.right = LARGURA

            if self.rect.top < 0:
                self.rect.top = 0

            if self.rect.bottom > ALTURA:
                self.rect.bottom = ALTURA

    class Carro(pygame.sprite.Sprite):
        def __init__(self, grupo_carros):
            pygame.sprite.Sprite.__init__(self)

            self.grupo_carros = grupo_carros
            self.image = random.choice(imagens_carros)
            self.rect = self.image.get_rect()

            self.rect.centerx, self.rect.y = posicao_segura_carro(self.grupo_carros)

            # Carros mais lentos
            self.velocidade = random.randint(5, 9)

        def update(self):
            self.rect.y += self.velocidade

            if self.rect.top > ALTURA:
                self.image = random.choice(imagens_carros)
                self.rect = self.image.get_rect()

                self.rect.centerx, self.rect.y = posicao_segura_carro(self.grupo_carros)

                self.velocidade = random.randint(5, 9)

    class Cliente(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.image = img_cliente
            self.rect = self.image.get_rect()
            self.rect.centerx = LARGURA // 2

            # Quanto mais negativo, mais tempo a fase dura
            self.rect.top = -3000

            self.velocidade = 3

        def update(self):
            self.rect.y += self.velocidade

            if self.rect.top >= 20:
                self.rect.top = 20

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

        return "continuar"

    # ---------- Grupos ----------
    todos_sprites = pygame.sprite.Group()
    grupo_carros = pygame.sprite.Group()

    jogador = Entregador()
    cliente = Cliente()

    todos_sprites.add(jogador)
    todos_sprites.add(cliente)

    for i in range(7):
        carro = Carro(grupo_carros)
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

        # Movimento da rua
        fundo_y1 += velocidade_fundo
        fundo_y2 += velocidade_fundo

        if fundo_y1 >= ALTURA:
            fundo_y1 = -ALTURA

        if fundo_y2 >= ALTURA:
            fundo_y2 = -ALTURA

        todos_sprites.update()

        if pygame.sprite.spritecollide(jogador, grupo_carros, False):
            perdeu = True
            rodando = False

        if jogador.rect.colliderect(cliente.rect):
            ganhou = True
            rodando = False

        tela.blit(fundo, (0, fundo_y1))
        tela.blit(fundo, (0, fundo_y2))

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
        resultado = mostrar_tela_final(tela_perdeu, som_perdeu)

        if resultado == "continuar":
            fase3()

    elif ganhou:
        tocar_som(som_yay)
        mostrar_tela_final(tela_ganhou, som_ganhou)

    pygame.quit()


fase3()
