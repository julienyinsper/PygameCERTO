import sys

from inicio import inicio
from fase1 import fase1
from fase2 import fase2
from fase3 import fase3


def main():

    # TELA DE INÍCIO
    inicio()

    fase_atual = 1

    while True:

        # ---------------- FASE 1 ----------------
        if fase_atual == 1:

            resultado = fase1()

            # PASSOU DA FASE 1
            if resultado == 1:
                fase_atual = 2

            # PERDEU
            else:
                fase_atual = 1

        # ---------------- FASE 2 ----------------
        elif fase_atual == 2:

            resultado = fase2()

            # PASSOU DA FASE 2
            if resultado == 1:
                fase_atual = 3

            # PERDEU
            else:
                fase_atual = 1

        # ---------------- FASE 3 ----------------
        elif fase_atual == 3:

            fase3()
            break

        else:
            break

    sys.exit()


if __name__ == "__main__":
    main()