import pygame
import random
import time
pygame.init()
pygame.mixer.init()

    # Carrega a música
pygame.mixer.music.load('Assets/Sons/Telainicio.mp3')
    
    # Reproduz a música em loop (-1 significa repetir indefinidamente)
pygame.mixer.music.play(-1)
from inicio import*
from fase1 import* 
pygame.mixer.init()

    # Carrega a música
pygame.mixer.music.load('Assets/Sons/Telainicio.mp3')
    
    # Reproduz a música em loop (-1 significa repetir indefinidamente)
pygame.mixer.music.play(-1)
from tela_prox_nivel import*
from fase3 import*