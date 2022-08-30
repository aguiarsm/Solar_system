import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Constantes:
    def __init__(self):
        self.G = 6.67e-11
        self.Mb = 4.0e30  # black hole
        self.Ms = 2.0e30  # sun
        self.Mt = 5.972e24  # earth
        self.Mm = 6.41e23  # mars
        self.Mc = 6.39e20  # unknown comet
        self.AU = 1.5e11
        self.dt = 24*60*60
_constantes = Constantes()

class CorpoCeleste:

    def __init__(self, nome, pos_x, pos_y, vel_x, vel_y, massa, cor, size, G):
        self.nome = nome
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.massa = massa
        self.cor = cor
        self.point_plot = None
        self.lineplot = None
        self.textplot = None
        self.size = size
        self.historia_x = []
        self.historia_y = []
        self.G = G

    def atualizaX(self, dt):
        self.pos_x += self.vel_x * dt

    def atualizaY(self, dt):
        self.pos_y += self.vel_y * dt

    def atualizaVX(self, dt, fx_total):
        self.vel_x += (fx_total * dt) / self.massa

    def atualizaVY(self, dt, fy_total):
        self.vel_y += (fy_total * dt) / self.massa

    def dist_x(self, other):
        return abs(self.pos_x - other.pos_x)

    def dist_y(self, other):
        return abs(self.pos_y - other.pos_y)

    def distancia(self, other):
        return np.sqrt(self.dist_x(other) ** 2 + self.dist_y(other) ** 2)

    def theta_horizontal(self, other):
        if self.dist_x(other) == 0:
            if self.dist_y(other) > 0:
                return np.pi / 2
            else:
                return (3 * np.pi) / 2
        else:
            return np.arctan(self.dist_y(other) / self.dist_x(other))

    def modulo_forca(self, other):
        F = (self.G * self.massa * other.massa) / (self.distancia(other) ** 2)
        return F

    def Fx(self, other):
        F = self.modulo_forca(other) * np.cos(self.theta_horizontal(other))
        if self.pos_x > other.pos_x:
            return -1 * abs(F)
        else:
            return abs(F)

    def Fy(self, other):
        F = self.modulo_forca(other) * np.sin(self.theta_horizontal(other))
        if self.pos_y > other.pos_y:
            return -1 * abs(F)
        else:
            return abs(F)

    def inicia_plots(self, ax, plot_trace = True, plot_text = True):
        self.point_plot, = ax.plot([self.pos_x], [self.pos_y], marker="o", markersize=self.size,
                                   markeredgecolor=self.cor, markerfacecolor=self.cor)
        if plot_trace:
            self.lineplot, = ax.plot([self.pos_x], [self.pos_y], lw=1, c=self.cor)
        if plot_text:
            self.textplot = ax.text(self.pos_x, self.pos_y, self.nome)

    def plota_tudo(self, plot_trace = True, plot_text = True):
        if plot_trace:
            self.historia_x.append(self.pos_x)
            self.historia_y.append(self.pos_y)
            self.lineplot.set_data(self.historia_x, self.historia_y)
        if plot_text:
            self.textplot.set_position((self.pos_x, self.pos_y))
        self.point_plot.set_data(self.pos_x, self.pos_y)


def calcula_forca_total(lista_de_corpos):
    dados = {}
    for primeiro in lista_de_corpos:
        dados[primeiro.nome] = []
        fx_total = fy_total = 0
        prov = lista_de_corpos[:]
        prov.remove(primeiro)
        for segundo in prov:
            fx_total += primeiro.Fx(segundo)
            fy_total += primeiro.Fy(segundo)
        dados[primeiro.nome].append([primeiro, fx_total, fy_total])
    return dados


def atualiza_all_pos(lista_corpos, corpo, dt):
    corpos = calcula_forca_total(lista_corpos)

    corpo.atualizaVX(dt, corpos[corpo.nome][0][1])
    corpo.atualizaVY(dt, corpos[corpo.nome][0][2])

    corpo.atualizaX(dt)
    corpo.atualizaY(dt)


def inicia_figura(size_fig, x_lim, y_lim):
    fig, ax = plt.subplots(figsize=size_fig)
    ax.set_xlim(x_lim, y_lim)
    ax.set_ylim(x_lim, y_lim)
    ax.grid()
    return fig, ax


def show_animation():
    plt.show()


if __name__ == "__main__":

    terra = CorpoCeleste('terra', _constantes.AU, 0, 0, 30000, _constantes.Mt * 1000, 'blue', 5, _constantes.G)
    sol = CorpoCeleste('sol', 0, 0, 0, 0, _constantes.Ms, 'yellow', 10, _constantes.G)
    marte = CorpoCeleste('Marte', 1.666 * _constantes.AU, 0, 0, 21970, _constantes.Mm * 10000, 'red', 4, _constantes.G)
    cometa = CorpoCeleste('Cometa', 2 * _constantes.AU, 0.3 * _constantes.AU, 0, 7000, _constantes.Mc, 'black', 3, _constantes.G)

    lista_corpos = [terra, sol, marte, cometa]

    fig, ax = inicia_figura((5, 5), - 2 * _constantes.AU, 2 * _constantes.AU)

    for corpo in lista_corpos:
        corpo.inicia_plots(ax)

    def animation_frame(i):
        for corpo in lista_corpos:
            corpo.plota_tudo()
            atualiza_all_pos(lista_corpos, corpo, _constantes.dt)

    animation = FuncAnimation(fig, func=animation_frame, frames=10000, interval=5)
    show_animation()
