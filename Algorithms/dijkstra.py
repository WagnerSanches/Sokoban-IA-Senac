import heapq
from classes import Grid
from classes import No
from functions import *

def dijkstra(grid):
    resultado = process(grid)
    print_output(grid, resultado, 'dijkstra')

def process(grid):
    # estado inicial
    no_inicial = No(
        linha=grid.agente[0],
        col=grid.agente[1],
        caixas_restantes=frozenset(grid.caixas.items()),
        carregando=None,
        custo=0
    )

    # estruturas
    fila       = [(0, no_inicial)]        # min-heap (custo, no)
    distancia  = {no_inicial.estado(): 0} # estado → menor custo conhecido
    visitados  = set()

    while fila:
        custo_atual, no_atual = heapq.heappop(fila)  # retira o menor custo

        # já processamos esse estado?
        if no_atual.estado() in visitados:
            continue
        visitados.add(no_atual.estado())

        # objetivo atingido?
        if len(no_atual.caixas_restantes) == 0 and no_atual.carregando is None:
            return no_atual  # retorna o No final com predecessor encadeado

        # expande vizinhos
        for vizinho in vizinhos(no_atual, grid):
            if vizinho.estado() in visitados:
                continue

            # relaxamento
            if vizinho.custo < distancia.get(vizinho.estado(), float('inf')):
                distancia[vizinho.estado()] = vizinho.custo
                heapq.heappush(fila, (vizinho.custo, vizinho))

    return None  # não encontrou solução