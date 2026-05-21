
import pygame
import random
import sys


def mostrar_derrota(window, WIDTH, HEIGHT, background):
    fonte_titulo = pygame.font.SysFont(None, 72)
    fonte_texto = pygame.font.SysFont(None, 36)

    titulo = fonte_titulo.render("Você perdeu!", True, (255, 165, 0))
    msg1 = fonte_texto.render("Um carro te atingiu.", True, (255, 255, 255))
    msg2 = fonte_texto.render(
        "Pressione qualquer tecla ou clique para continuar.",
        True,
        (255, 255, 255)
    )

    window.blit(background, (0, 0))
    window.blit(titulo, (WIDTH // 2 - titulo.get_width() // 2, HEIGHT // 4))
    window.blit(msg1, (WIDTH // 2 - msg1.get_width() // 2, HEIGHT // 2))
    window.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                esperando = False


def fase1():
    pygame.init()

    try:
        pygame.mixer.init()

        # Música de fundo da fase
        pygame.mixer.music.load("Assets/Sons/Trilhasonora.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # Som de começo da fase: "Let's go"
        som_comeco = pygame.mixer.Sound("Assets/Sons/Comeco.mp3")
        som_comeco.set_volume(0.8)
        som_comeco.play()

        # Som de game over
        som_gameover = pygame.mixer.Sound("Assets/Sons/Gameover.mp3")
        som_gameover.set_volume(0.8)

    except:
        som_comeco = None
        som_gameover = None

    WIDTH, HEIGHT = 900, 600
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Entregando")
    clock = pygame.time.Clock()
    FPS = 30

    # Fundo fixo
    imagem_fundo = pygame.image.load("Assets/Imagens/Rua.png").convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))

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

    # Cliente no topo
    cliente_width = 120
    cliente_height = 80
    imagem_cliente = pygame.image.load("Assets/Imagens/Cliente.png").convert_alpha()
    imagem_cliente = pygame.transform.scale(imagem_cliente, (cliente_width, cliente_height))
    cliente_rect = imagem_cliente.get_rect()
    cliente_rect.midtop = (ROAD_CENTER, 10)

    # Área de entrega pequena
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
        car_images[color] = pygame.transform.scale(img, (CAR_WIDTH, CAR_HEIGHT))

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
            self.rect.y = random.randint(-500, -CAR_HEIGHT)
            self.speedy = random.randint(4, 7)

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT:
                self.reset()

    all_sprites = pygame.sprite.Group()
    all_cars = pygame.sprite.Group()

    jogador = Entregador(imagem_entregador)
    all_sprites.add(jogador)

    # Apenas 3 carros no início, um por faixa
    for lane_x in LANE_XS:
        carro = Carro(random.choice(list(car_images.values())), lane_x)
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

        # Movimento contínuo pelo teclado
        teclas = pygame.key.get_pressed()
        jogador.speedx = 0
        jogador.speedy = 0

        if teclas[pygame.K_LEFT]:
            jogador.speedx = -5
        if teclas[pygame.K_RIGHT]:
            jogador.speedx = 5
        if teclas[pygame.K_UP]:
            jogador.speedy = -5
        if teclas[pygame.K_DOWN]:
            jogador.speedy = 5

        all_sprites.update()

        # Colisão com carros: derrota
        if pygame.sprite.spritecollide(jogador, all_cars, False, pygame.sprite.collide_mask):
            pygame.mixer.music.stop()

            if som_gameover:
                som_gameover.play()

            mostrar_derrota(window, WIDTH, HEIGHT, imagem_fundo)
            resultado = 0
            game = False
            continue

        # Vitória: quando o jogador toca no cliente / zona de entrega
        if jogador.rect.colliderect(zona_entrega):
            resultado = 3
            game = False
            continue

        # Desenho
        window.blit(imagem_fundo, (0, 0))
        window.blit(imagem_cliente, cliente_rect)
        all_sprites.draw(window)
        pygame.display.flip()

    pygame.quit()
    return resultado


if __name__ == "__main__":
    fase1()