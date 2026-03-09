import heapq
from classes import Grid
from classes import No

MOVIMENTOS = [(-1,0,'↑'), (1,0,'↓'), (0,-1,'←'), (0,1,'→')]

def vizinhos(no, grid):
    resultado = []

    for dl, dc, mov in MOVIMENTOS:
        nova_linha = no.linha + dl
        nova_col   = no.col + dc
        nova_pos   = (nova_linha, nova_col)

        if not (0 <= nova_linha < grid.linhas and 0 <= nova_col < grid.colunas):
            continue

        if nova_pos in grid.barreiras:
            continue

        caixas_dict = dict(no.caixas_restantes)
        carregando  = no.carregando  

        if carregando is not None:
            custo_movimento = 1 + carregando
        else:
            custo_movimento = 1

        novas_caixas = dict(caixas_dict)
        novo_carregando = carregando

        if nova_pos in caixas_dict and carregando is None:
            novo_carregando = caixas_dict[nova_pos]
            del novas_caixas[nova_pos]
        
        elif nova_pos in grid.alvos and carregando is not None:
            novo_carregando = None 

        novo_no = No(
            linha=nova_linha,
            col=nova_col,
            caixas_restantes=frozenset(novas_caixas.items()),
            carregando=novo_carregando,
            custo=no.custo + custo_movimento,
            predecessor=no,
            movimento=mov    
        )
        resultado.append(novo_no)

    return resultado

def reconstruir_caminho(no_final):
    caminho = []
    no = no_final
    while no is not None:
        caminho.append(no)
        no = no.predecessor
    caminho.reverse()
    return caminho

def gerar_estado_final(grid, caminho_nos):
    import copy

    estado = copy.deepcopy(grid.grid)

    for li in range(grid.linhas):
        for ci in range(grid.colunas):
            cel = estado[li][ci]
            if cel == '🙎' or cel.rstrip() in ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']:
                estado[li][ci] = '⚪️'

    no_final = caminho_nos[-1]

    estado[no_final.linha][no_final.col] = '🙎'

    return estado

def salvar_saida(caminho_arquivo, grid, caminho_nos):
    estado_final = gerar_estado_final(grid, caminho_nos)
    movimentos = [no.movimento for no in caminho_nos if no.movimento is not None]

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:

        f.write("Estado final\n")
        for linha in estado_final:
            f.write(''.join(linha) + '\n')

        f.write("Movimentos\n")
        f.write(' '.join(movimentos) + '\n')

        f.write("Quantidade de movimentos\n")
        f.write(str(len(movimentos)) + '\n')

def print_output(grid, resultado, nome_algoritmo):
    if resultado:
        nos = reconstruir_caminho(resultado)
        salvar_saida(f'output/{nome_algoritmo}.txt', grid, nos)
        print(f"{nome_algoritmo} - Custo: {resultado.custo} | Movimentos: {len(nos)-1}")
    else:
        print("Sem solução!")


def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def heuristica(no, grid):
    agente = (no.linha, no.col)
    caixas_dict = dict(no.caixas_restantes)

    if no.carregando is not None:
        return min(manhattan(agente, alvo) for alvo in grid.alvos)

    if len(caixas_dict) == 0:
        return 0

    return min(
        manhattan(agente, caixa) + min(manhattan(caixa, alvo) for alvo in grid.alvos)
        for caixa in caixas_dict.keys()
    )