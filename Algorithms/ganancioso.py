import heapq
from classes import Grid
from classes import No
from functions import *
from itertools import count

def ganancioso(grid):
    resultado_ganancioso = process(grid)
    print_output(grid, resultado_ganancioso, 'ganancioso')

def process(grid):
    no_inicial = No(
        linha=grid.agente[0],
        col=grid.agente[1],
        caixas_restantes=frozenset(grid.caixas.items()),
        carregando=None,
        custo=0
    )

    contador = count()
    h_inicial = heuristica(no_inicial, grid)
    fila      = [(h_inicial, next(contador), no_inicial)]
    visitados = set()

    while fila:
        h_atual, _, no_atual = heapq.heappop(fila)  # ← desempacota 3 valores

        if no_atual.estado() in visitados:
            continue
        visitados.add(no_atual.estado())

        if len(no_atual.caixas_restantes) == 0 and no_atual.carregando is None:
            return no_atual

        for viz in vizinhos(no_atual, grid):
            if viz.estado() in visitados:
                continue
            h = heuristica(viz, grid)
            heapq.heappush(fila, (h, next(contador), viz))  # ← 3 valores

    return None