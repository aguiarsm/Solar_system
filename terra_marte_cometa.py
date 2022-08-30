import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import astronomy2

cte = astronomy2.Constantes()

terra = astronomy2.CorpoCeleste('terra', cte.AU, 0, 0, 30000, cte.Mt, 'blue', 5, cte.G)
sol = astronomy2.CorpoCeleste('sol', 0, 0, 0, 0, cte.Ms, 'yellow', 10, cte.G)
marte = astronomy2.CorpoCeleste('Marte', 1.666 * cte.AU, 0, 0, 21970, cte.Mm, 'red', 4, cte.G)
cometa = astronomy2.CorpoCeleste('Cometa', 2 * cte.AU, 0.3 * cte.AU, 0, 7000, cte.Mc, 'black', 3, cte.G)


lista_corpos = [terra, sol, marte, cometa]


fig, ax = astronomy2.inicia_figura((5, 5), - 2 * cte.AU, 2 * cte.AU)
for corpo in lista_corpos:
    corpo.inicia_plots(ax)

def animation_frame(i):
    for corpo in lista_corpos:
        corpo.plota_tudo()
        astronomy2.atualiza_all_pos(lista_corpos, corpo, cte.dt)

animation = FuncAnimation(fig, func=animation_frame, frames=10000, interval=1)
astronomy2.show_animation()
