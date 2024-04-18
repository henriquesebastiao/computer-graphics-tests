from time import time

import matplotlib.pyplot as plt
import numpy as np
from numpy import dot
from tqdm import tqdm  # Progress bar

w, h = 800, 800  # width, height of the image in pixels

screen = np.zeros((h, w, 3))


class Esfera:
    def __init__(self, raio, centro, cor):
        self.raio = raio
        self.centro = centro
        self.cor = cor


e1 = Esfera(1, centro=np.array((0, -1, 5)), cor=np.array((1, 0, 0)))
e2 = Esfera(5000, centro=np.array((0, -5001, 0)), cor=np.array((0, 1, 0)))
esferas_cena = [e1, e2]


def trassar_raio(origem, vetor_d, t_min, t_max, esferas_da_cena):
    t_solucao_final = t_max
    esfera_final = None

    for esfera in esferas_da_cena:
        t1, t2 = resolve_bhaskara(origem, vetor_d, esfera)

        try:
            if t_min < t1 < t_solucao_final:
                t_solucao_final = t1
                esfera_final = esfera
            if t_min < t2 < t_solucao_final:
                t_solucao_final = t2
                esfera_final = esfera

        except:  # noqa
            pass

    return t_solucao_final, esfera_final


def resolve_bhaskara(origem, vetor_d, esfera):
    co = origem - esfera.centro
    r = esfera.raio

    a = dot(vetor_d, vetor_d)
    b = 2 * dot(co, vetor_d)
    c = dot(co, co) - r * r

    delta = b * b - 4 * a * c

    if delta >= 0:
        return (-b + delta**0.5) / (2 * a), (-b - delta**0.5) / (2 * a)
    else:
        return None, None


def pintar_ponto_do_mundo(ponto, esfera):
    x_projetado = ponto[0] * w / ponto[2]
    y_projetado = ponto[1] * h / ponto[2]

    xp = x_projetado + w / 2
    yp = h / 2 - y_projetado

    xp, yp = int(xp), int(yp)

    try:
        screen[yp][xp] = esfera.cor
    except:  # noqa
        pass


origem = np.array((0, 0, 0))

inicio = time()

for x in tqdm(np.arange(-w / 2, w / 2, 0.5)):
    for y in np.arange(-h / 2, h / 2, 0.5):
        vetor_d = np.array((x / h, y / h, 1)) - origem
        t, esfera = trassar_raio(origem, vetor_d, 1, 1e6, esferas_cena)
        if esfera:
            ponto = origem + t * vetor_d
            pintar_ponto_do_mundo(ponto, esfera)

fim = time()

render_time = fim - inicio
print(f'Tempo de renderização: {render_time:.2f} segundos')

plt.imshow(screen)
plt.show()
