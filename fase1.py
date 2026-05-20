import pygame
import random

def fase1():
    pygame.init()
    # pygame.mixer.init()

   # Música de fundo
    pygame.mixer.music.load('Assets/Sons/Trilhasonora.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    # ----- Gera tela principal
    WIDTH = 900
    HEIGHT = 600
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Entregando')

    # ----- Carrega imagens
    # Carregando a imagem de fundo
    imagem_fundo = pygame.image.load('Assets/Imagens/Rua.png').convert()
    imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))
    imagem_fundo_rect = imagem_fundo.get_rect()
    speed_fundo = 10

    # Imagem do cliente
    imagem_cliente = pygame.image.load('Assets/Imagens/Cliente.png').convert_alpha()
    cliente_width = 120
    cliente_height = 80
    imagem_cliente = pygame.transform.scale(imagem_cliente, (cliente_width, cliente_height))
    cliente_rect = imagem_cliente.get_rect()
    cliente_rect.centery = HEIGHT / 2  # Centraliza cliente verticalmente
    cliente_rect.right = 120

    # Imagem entregador
    entregador_width = 100
    entregador_height = 70
    imagem_entregador = pygame.image.load('Assets/Imagens/Entregador.png').convert_alpha()
    imagem_entregador = pygame.transform.scale(imagem_entregador, (entregador_width, entregador_height))

    # Carregando imagens dos carros
    CAR_WIDTH = 80
    CAR_HEIGHT = 140
    car_colors = ['azul', 'vermelho', 'amarelo']
    car_images = {}
    for color in car_colors:
        img = pygame.image.load(f'Assets/Imagens/Carro_{color}.png').convert_alpha()
        car_images[color] = pygame.transform.scale(img, (CAR_WIDTH, CAR_HEIGHT))

    # ----- CLASSE ENTREGADOR
    class ENTREGADOR(pygame.sprite.Sprite):
        def __init__(self, img, all_sprites):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 20
            self.speedx = 0
            self.speedy = 0
            self.all_sprites = all_sprites

        def update(self):
            # Atualização da posição do entegador
            self.rect.x += self.speedx
            self.rect.y += self.speedy

            # Mantem dentro da tela
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            if self.rect.top < 0:
                self.rect.top = 0

    # ----- CLASSE CARROS
    class CARRO(pygame.sprite.Sprite):
        def __init__(self, img):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, WIDTH - CAR_WIDTH)
            self.rect.y = random.randint(-200, -CAR_HEIGHT)
            self.speedx = random.randint(-2, 2)
            self.speedy = random.randint(5, 12)

        def update(self):
            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
                self.rect.x = random.randint(0, WIDTH - CAR_WIDTH)
                self.rect.y = random.randint(-200, -CAR_HEIGHT)
                self.speedx = random.randint(-2, 2)
                self.speedy = random.randint(5, 12)

    # ----- Definindo outras variáveis do jogo
    game = True
    clock = pygame.time.Clock()
    FPS = 30

    # ----- Criando um grupo de sprites para os carros
    all_sprites = pygame.sprite.Group()
    all_cars = pygame.sprite.Group()

    # Criando o jogador
    jogador = ENTREGADOR(imagem_entregador, all_sprites)
    all_sprites.add(jogador)

    # ----- Criando os carros e adicionando ao grupo de sprites
    num_cars = 6
    for _ in range(num_cars):
        car = CARRO(random.choice(list(car_images.values())))
        all_sprites.add(car)
        all_cars.add(car)

    # Variável para controlar o tempo e adicionar mais carros
    car_add_counter = 0
    car_add_interval = 200  # Intervalo para adicionar carros

    # ===== Loop principal =====
    K =0
    while game:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                game = False
            # Verifica se apertou alguma tecla.
            if event.type == pygame.KEYDOWN:
                # Dependendo da tecla, altera a velocidade.
                if event.key == pygame.K_LEFT:
                    jogador.speedx -= 4
                if event.key == pygame.K_RIGHT:
                    jogador.speedx += 4
                if event.key == pygame.K_UP:
                    jogador.speedy = -5
                if event.key == pygame.K_DOWN:
                    jogador.speedy = 5

            # Verifica se soltou alguma tecla.
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    jogador.speedx = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    jogador.speedy = 0

        # Atualiza estado do jogo
        all_sprites.update()

        window.fill((0, 0, 0))
        # Atualiza a posição da imagem de fundo.
        imagem_fundo_rect.x += speed_fundo
        # Se o fundo saiu da janela, faz ele voltar para dentro.
        if imagem_fundo_rect.left > WIDTH:
            imagem_fundo_rect.x -= imagem_fundo_rect.width
        # Desenha o fundo e uma cópia para a direita.
        window.blit(imagem_fundo, imagem_fundo_rect)
        imagem_fundo_rect_2 = imagem_fundo_rect.copy()
        imagem_fundo_rect_2.x -= imagem_fundo_rect_2.width
        window.blit(imagem_fundo, imagem_fundo_rect_2)

        # Verifica se houve colisão entre carros
        if pygame.sprite.spritecollide(jogador, all_cars, False):
            # import perdeu_carro
            # perdeu_carro()
                    
                # ----- Gera tela principal
            WIDTH = 900
            HEIGHT = 600
            window = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('Entregando')
        
        # ----- Carrega imagens
            # Carregando a imagem de fundo
            imagem_fundo = pygame.image.load('assets/img/Rua.png').convert()
            imagem_fundo = pygame.transform.scale(imagem_fundo, (WIDTH, HEIGHT))
            imagem_fundo_rect = imagem_fundo.get_rect()
            imagem_fundo_rect_2 = imagem_fundo_rect.copy()
            imagem_fundo_rect_2.x -= imagem_fundo_rect_2.width
            speed_fundo = 10 

        # ----- Função para mostrar a quando é atingido por carro
            def perdeu_carro():
                window.blit(imagem_fundo, imagem_fundo_rect)
                window.blit(imagem_fundo, imagem_fundo_rect_2)

                 # Fonte maior e cor laranja para o título
                title_font = pygame.font.SysFont(None, 72)
                title = title_font.render("Você perdeu!", True, (255, 165, 0))  # Laranja
                
                # Fonte menor para a história
                font = pygame.font.SysFont(None, 40)
                acontecimento = ["Um carro te atingiu."]

                font_inicio = pygame.font.SysFont(None, 30)
                inicio = font_inicio.render("Clique em qualquer botão para reiniciar o jogo.", True, (255, 255, 255))

                # Desenha o título
                window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
                pygame.display.flip()

                # Desenha a história de forma animada
                for i, line in enumerate(acontecimento):
                    rendered_line = ""
                    for char in line:
                        rendered_line += char
                        text = font.render(rendered_line, True, (255, 255, 255))
                        window.blit(imagem_fundo, imagem_fundo_rect)
                        window.blit(imagem_fundo, imagem_fundo_rect_2)
                        window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
                        for j in range(i):
                            previous_text = font.render(acontecimento[j], True, (255, 255, 255))
                            window.blit(previous_text, (WIDTH // 2 - previous_text.get_width() // 2, HEIGHT // 3 + 40 * (j + 1)))
                        window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + 40 * (i + 1)))
                        pygame.display.flip()
                        pygame.time.wait(50)  # Delay de 50ms entre cada letra

                window.blit(inicio, (WIDTH // 2 - inicio.get_width() // 2, HEIGHT // 38))
                pygame.display.flip()

                # Aguarda o jogador pressionar uma tecla ou botão do mouse para iniciar o jogo
                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP:
                            waiting = False
                        
            perdeu_carro()
            pygame.init()
            fase1()

             # Verifica se houve colisão cliente
        elif jogador.rect.colliderect(cliente_rect):
            import tela_prox_nivel
            K = 3
            game = False


        # Adiciona mais carros após um intervalo
        car_add_counter += 1
        if car_add_counter >= car_add_interval:
            car_add_counter = 0
            for _ in range(2):  # Adiciona 2 novos carros a cada intervalo
                car = CARRO(random.choice(list(car_images.values())))
                all_sprites.add(car)
                all_cars.add(car)
            

        # Gera saídas
        window.blit(imagem_cliente, cliente_rect)  # Desenha o cliente
        all_sprites.draw(window)
        pygame.display.update()

    pygame.quit()
    return K




fase1()



        