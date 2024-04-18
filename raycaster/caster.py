from time import time

import matplotlib.pyplot as plt
import numpy as np
from numpy import dot
from tqdm import tqdm  # Progress bar

w, h = 800, 800  # width, height of the image in pixels

screen = np.zeros((h, w, 3))


class Esfera:
    def __init__(self, raio, centro, cor, brilho):
        self.raio = raio
        self.centro = centro
        self.cor = cor
        self.brilho = brilho


class LuzPontual:
    def __init__(self, intensidade, origem):
        self.intensidade = intensidade
        self.origem = origem
        self.tipo = 'pontual'


class LuzAmbiente:
    def __init__(self, intensidade):
        self.intensidade = intensidade
        self.tipo = 'ambiente'


class LuzDirecional:
    def __init__(self, intensidade, direcao):
        self.intensidade = intensidade
        self.direcao = direcao
        self.tipo = 'direcional'


e1 = Esfera(1, centro=np.array((0, -1, 5)), cor=np.array((1, 0, 0)), brilho=500)
e2 = Esfera(5000, centro=np.array((0, -5001, 0)), cor=np.array((0, 1, 0)), brilho=10)
e3 = Esfera(raio=1, centro=np.array((1, 1, 7)), cor=np.array((0, 0, 1)), brilho=20)

luz_pontual = LuzPontual(intensidade=0.7, origem=np.array((-1, 2, 5)))
luz_ambiente = LuzAmbiente(0.1)
luz_direcional = LuzDirecional(intensidade=0.2, direcao=np.array((1, 4, 4)))

esferas_cena = [e1, e2, e3]
luzes_cena = [luz_pontual, luz_ambiente, luz_direcional]


def retornar_vetor_refletido(vetor_incidente, vetor_normal):
    return 2 * vetor_normal * dot(vetor_incidente, vetor_normal) - vetor_incidente


def calcular_luz(p, esfera, luzes_cena):
    vetor_normal = p - esfera.centro
    vetor_normal_tamanho = dot(vetor_normal, vetor_normal) ** 0.5
    vetor_normal_normalizado = vetor_normal / vetor_normal_tamanho

    vetor_olho = origem - ponto
    vetor_olho_tamanho = dot(vetor_olho, vetor_olho) ** 0.5
    vetor_olho_normalizado = vetor_olho / vetor_olho_tamanho

    luz_final = 0

    for luz in luzes_cena:
        if luz.tipo == 'ambiente':
            luz_final += luz.intensidade

        if luz.tipo == 'pontual':
            vetor_l = luz.origem - p
            t_sombra, esfera_sombra = trassar_raio(
                p, vetor_l, t_min=0.001, t_max=1, esferas_da_cena=esferas_cena
            )
            if esfera_sombra is None:
                vetor_l_tamanho = dot(vetor_l, vetor_l) ** 0.5
                vetor_l_normalizado = vetor_l / vetor_l_tamanho
                n_dot_l = dot(vetor_normal_normalizado, vetor_l_normalizado)
                if n_dot_l > 0:
                    luz_pontual = luz.intensidade * n_dot_l
                    luz_final += luz_pontual

                if (
                    dot(
                        vetor_olho,
                        retornar_vetor_refletido(vetor_l, vetor_normal),
                    )
                    > 0
                ):
                    r = retornar_vetor_refletido(vetor_l, vetor_normal)
                    r_normalizado = r / dot(r, r) ** 0.5
                    olho_dot_r = dot(vetor_olho_normalizado, r_normalizado)
                    intensidade_brilho = luz.intensidade * (olho_dot_r**esfera.brilho)
                    luz_final += intensidade_brilho

        if luz.tipo == 'direcional':
            vetor_l = luz.direcao
            t_sombra, esfera_sombra = trassar_raio(
                p,
                vetor_l,
                t_min=0.001,
                t_max=1e6,
                esferas_da_cena=esferas_cena,
            )
            if esfera_sombra is None:
                vetor_l_tamanho = dot(vetor_l, vetor_l) ** 0.5
                vetor_l_normalizado = vetor_l / vetor_l_tamanho
                n_dot_l = dot(vetor_normal_normalizado, vetor_l_normalizado)
                if n_dot_l > 0:
                    luz_direcional = luz.intensidade * n_dot_l
                    luz_final += luz_direcional

                if (
                    dot(
                        vetor_olho,
                        retornar_vetor_refletido(vetor_l, vetor_normal),
                    )
                    > 0
                ):
                    r = retornar_vetor_refletido(vetor_l, vetor_normal)
                    r_normalizado = r / dot(r, r) ** 0.5
                    olho_dot_r = dot(vetor_olho_normalizado, r_normalizado)
                    intensidade_brilho = luz.intensidade * (olho_dot_r**esfera.brilho)
                    luz_final += intensidade_brilho

        return np.clip(luz_final, 0, 1)


def trassar_raio(origem, vetor_d, t_min, t_max, esferas_da_cena):
    t_solucao_final = t_max
    esfera_final = None
    a = dot(vetor_d, vetor_d)

    for esfera in esferas_da_cena:
        t1, t2 = resolve_bhaskara(origem, vetor_d, esfera, a)

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


def resolve_bhaskara(origem, vetor_d, esfera, a):
    co = origem - esfera.centro
    r = esfera.raio

    b = 2 * dot(co, vetor_d)
    c = dot(co, co) - r * r

    delta = b * b - 4 * a * c

    if delta >= 0:
        return (-b + delta**0.5) / (2 * a), (-b - delta**0.5) / (2 * a)
    else:
        return None, None


def pintar_ponto_do_mundo(ponto, esfera, luz):
    x_projetado = ponto[0] * w / ponto[2]
    y_projetado = ponto[1] * h / ponto[2]

    xp = x_projetado + w / 2
    yp = h / 2 - y_projetado

    xp, yp = int(xp), int(yp)

    try:
        screen[yp][xp] = luz * esfera.cor
    except:  # noqa
        pass


origem = np.array((0, 0, 0))

inicio = time()

for x in tqdm(np.arange(-w / 2, w / 2, 0.5)):
    for y in np.arange(-h / 2, h / 2, 0.5):
        vetor_d = np.array((x / h, y / h, 1)) - origem
        a = dot(vetor_d, vetor_d)
        t, esfera = trassar_raio(origem, vetor_d, 1, 1e6, esferas_cena)
        if esfera:
            ponto = origem + t * vetor_d
            luz = calcular_luz(ponto, esfera, luzes_cena)
            pintar_ponto_do_mundo(ponto, esfera, luz)

fim = time()

render_time = fim - inicio
print(f'Tempo de renderização: {render_time:.2f} segundos')

plt.imshow(screen)
plt.show()
