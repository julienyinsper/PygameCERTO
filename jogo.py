# Importa as bibliotecas
import sys
# Importa as telas e fases
from inicio import inicio
from fase1 import fase1
from fase2 import fase2
from fase3 import fase3
from perdeu import perdeu
from ganhou import ganhou

# Função principal jogo
def main():

    # Tela de início
    inicio()
    # Define a fase inicial do jogo
    fase_atual = 1

    # Loop principal do jogo para controlar a transição entre as fases
    while True:

        #  Fase 1 
        # Verifica se a fase atual é a fase 1
        if fase_atual == 1:
            # Executa a fase 1 e armazena o resultado
            resultado = fase1()

            # Passou da fase 1
            if resultado == 1:
                fase_atual = 2

            # Perdeu
            else:
                fase_atual = 1

        # Verifica se a fase atual é a fase 2 
        elif fase_atual == 2:
            # Executa a fase 2 e armazena o resultado
            resultado = fase2()

            # Passou da fase 2
            if resultado == 1:
                fase_atual = 3

            # Perdeu
            else:
                fase_atual = 1

        # Verifica se a fase atual é a fase 3
        elif fase_atual == 3:
            # Executa a fase 3 e armazena o resultado
            resultado = fase3()

            # Passou da fase 3
            if resultado == 1:
                ganhou()

            # Perdeu
            else:
                perdeu()

            # Encerra o loop principal
            break
        # Caso aconteça algum valor inválido, encerra o jogo
        else:
            break
    # Fecha o programa
    sys.exit()

# Executa se o arquivo for iniciado diretamente
if __name__ == "__main__":
    main()