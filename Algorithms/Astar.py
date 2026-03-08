import heapq
from classes import No
from functions import *
from itertools import count

def astar(grid):
    resultado_astar = process(grid)
    print_output(grid, resultado_astar, 'astar')

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
    f_inicial = 0 + h_inicial               # f = g + h

    fila      = [(f_inicial, next(contador), no_inicial)]
    distancia = {no_inicial.estado(): 0}
    visitados = set()

    while fila:
        f_atual, _, no_atual = heapq.heappop(fila)

        if no_atual.estado() in visitados:
            continue
        visitados.add(no_atual.estado())

        if len(no_atual.caixas_restantes) == 0 and no_atual.carregando is None:
            return no_atual

        for viz in vizinhos(no_atual, grid):
            if viz.estado() in visitados:
                continue

            # relaxamento igual ao Dijkstra
            if viz.custo < distancia.get(viz.estado(), float('inf')):
                distancia[viz.estado()] = viz.custo
                h = heuristica(viz, grid)
                f = viz.custo + h            # f = g + h
                heapq.heappush(fila, (f, next(contador), viz))

    return None