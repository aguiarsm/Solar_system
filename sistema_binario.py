import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import astronomy2

cte = astronomy2.Constantes()

e1 = astronomy2.CorpoCeleste('e1', -600, 0, 0, -2.01, 10000000, 'yellow', 20, 1e-3)
e2 = astronomy2.CorpoCeleste('e2', 600, 0, 0, 2.01, 10000000, 'yellow', 20, 1e-3)
planeta = astronomy2.CorpoCeleste('planeta', 800, 0, 0, 10, 1000, 'blue', 10, 1e-3)


lista_corpos = [e1, e2, planeta]


fig, ax = astronomy2.inicia_figura((5, 5), -850, 850)
for corpo in lista_corpos:
    corpo.inicia_plots(ax)

def animation_frame(i):
    for corpo in lista_corpos:
        corpo.plota_tudo()
        astronomy2.atualiza_all_pos(lista_corpos, corpo, 1)

animation = FuncAnimation(fig, func=animation_frame, frames=10000, interval=1)
astronomy2.show_animation()
