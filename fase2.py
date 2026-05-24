
import pygame
import random
import sys
from perdeu import perdeu
from tela_prox_nivel import tela_prox_nivel


def fase2():
    pygame.init()

    WIDTH = 900
    HEIGHT = 600
    FPS = 30

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Entregando - Fase 2")
    clock = pygame.time.Clock()

    # Sons
    try:
        pygame.mixer.init()

        pygame.mixer.music.load("Assets/Sons/Trilhasonora.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        som_comeco = pygame.mixer.Sound("Assets/Sons/Comeco.mp3")
        som_comeco.set_volume(0.8)
        som_comeco.play()

    except:
        print("Algum som não carregou, mas o jogo vai continuar.")

    # Fundo com movimento vertical
    imagem_fundo = pygame.image.load("Assets/Imagens/Rua.png").convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))

    fundo_y = 0
    velocidade_fundo = 5

    # Limites da rua
    ROAD_LEFT = 300
    ROAD_RIGHT = 680
    ROAD_CENTER = (ROAD_LEFT + ROAD_RIGHT) // 2

    # Faixas da rua
    LANE_XS = [
        ROAD_LEFT + 55,
        ROAD_CENTER,
        ROAD_RIGHT - 55
    ]

    # Cliente
    cliente_width = 120
    cliente_height = 80

    imagem_cliente = pygame.image.load("Assets/Imagens/Cliente.png").convert_alpha()
    imagem_cliente = pygame.transform.scale(imagem_cliente, (cliente_width, cliente_height))

    cliente_rect = imagem_cliente.get_rect()
    cliente_rect.midtop = (ROAD_CENTER, 10)

    zona_entrega = pygame.Rect(ROAD_CENTER - 45, 0, 90, 85)

    # Entregador
    entregador_width = 100
    entregador_height = 70

    imagem_entregador = pygame.image.load("Assets/Imagens/Entregador.png").convert_alpha()
    imagem_entregador = pygame.transform.scale(imagem_entregador, (entregador_width, entregador_height))

    # Carros
    CAR_WIDTH = 80
    CAR_HEIGHT = 140

    car_colors = ["azul", "vermelho", "amarelo"]
    car_images = {}

    for color in car_colors:
        img = pygame.image.load(f"Assets/Imagens/Carro_{color}.png").convert_alpha()
        img = pygame.transform.scale(img, (CAR_WIDTH, CAR_HEIGHT))
        car_images[color] = img

    class Entregador(pygame.sprite.Sprite):
        def __init__(self, img):
            super().__init__()
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.centerx = ROAD_CENTER
            self.rect.bottom = HEIGHT - 20
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
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT

    class Carro(pygame.sprite.Sprite):
        def __init__(self, img, lane_x):
            super().__init__()
            self.image = img
            self.rect = self.image.get_rect()
            self.mask = pygame.mask.from_surface(self.image)
            self.lane_x = lane_x
            self.reset()

        def reset(self):
            self.rect.centerx = self.lane_x
            self.rect.y = random.randint(-800, -CAR_HEIGHT)
            self.speedy = random.randint(7, 10)

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT:
                self.reset()

    all_sprites = pygame.sprite.Group()
    all_cars = pygame.sprite.Group()

    jogador = Entregador(imagem_entregador)
    all_sprites.add(jogador)

    # Mais carros que na fase 1
    for lane_x in LANE_XS:
        carro = Carro(random.choice(list(car_images.values())), lane_x)
        all_sprites.add(carro)
        all_cars.add(carro)

    for _ in range(3):
        carro = Carro(
            random.choice(list(car_images.values())),
            random.choice(LANE_XS)
        )
        all_sprites.add(carro)
        all_cars.add(carro)

    game = True
    resultado = 0

    while game:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()

        jogador.speedx = 0
        jogador.speedy = 0

        if teclas[pygame.K_LEFT]:
            jogador.speedx = -7
        if teclas[pygame.K_RIGHT]:
            jogador.speedx = 7
        if teclas[pygame.K_UP]:
            jogador.speedy = -7
        if teclas[pygame.K_DOWN]:
            jogador.speedy = 7

        all_sprites.update()

        # Movimento da rua
        fundo_y += velocidade_fundo
        if fundo_y >= HEIGHT:
            fundo_y = 0

        # Colisão com carros = perdeu
        if pygame.sprite.spritecollide(jogador, all_cars, False, pygame.sprite.collide_mask):
            pygame.mixer.music.stop()
            perdeu()
            return 0

        # Vitória = passa para próxima tela
        if jogador.rect.colliderect(zona_entrega):
            tela_prox_nivel()
            return 1

        # Desenho
        window.blit(imagem_fundo, (0, fundo_y))
        window.blit(imagem_fundo, (0, fundo_y - HEIGHT))
        window.blit(imagem_cliente, cliente_rect)
        all_sprites.draw(window)

        pygame.display.flip()

    return resultado


if __name__ == "__main__":
    fase2()