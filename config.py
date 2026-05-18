# Arrumar os caminhos
from os import path

# Estabelece a pasta que contem as figuras e sons.
IMAGENS_DIR = path.join(path.dirname(__file__), 'Assets', 'Imagens')
SONS_DIR = path.join(path.dirname(__file__), 'Assets', 'Sons')

# Dados gerais do jogo.
WIDTH = 480 # Largura da tela
HEIGHT = 700 # Altura da tela
FPS = 60 # Frames por segundo

# Define tamanhos
DELIVERY_WIDTH = 50
DELIVERY_HEIGHT = 80
CAR_WIDTH = 70
CAR_HEIGHT = 120

# Define algumas variáveis com as cores básicas
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Estados para controle do fluxo da aplicação
INIT = 0
GAME = 1
QUIT = 2
