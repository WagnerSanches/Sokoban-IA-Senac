# Sokoban — Inteligência Artificial

Implementação e comparação de três algoritmos de busca (Dijkstra, Ganancioso e A*) aplicados ao problema do Sokoban em um grid N×M com caixas de pesos diferenciados.

---

## Modelagem do Problema

### Espaço de Estados

O problema é modelado como um espaço de estados onde cada estado representa uma configuração completa do ambiente:

```
estado = (linha_agente, col_agente, caixas_restantes, carregando)
```

| Componente | Descrição |
|---|---|
| `linha_agente, col_agente` | Posição atual do agente no grid |
| `caixas_restantes` | `frozenset` com as posições e pesos das caixas ainda não entregues |
| `carregando` | `None` se o agente está vazio, ou o peso da caixa que está carregando |

O uso de `frozenset` garante que o estado seja **hashable**, permitindo seu uso como chave nos dicionários `distancia[]` e `visitados`.

---

### Função Sucessora

A função sucessora está implementada em `functions.py` na função `vizinhos(no, grid)`.

Ela recebe um estado (`No`) e retorna todos os estados alcançáveis a partir dele. O agente pode se mover nas 4 direções: `↑ ↓ ← →`

Para cada movimento, são verificadas as seguintes condições:

- A célula destino está dentro dos limites do grid
- A célula destino não é uma barreira `🧱`
- Se a célula destino contém uma caixa e o agente está **sem carga** → o agente pega a caixa (remove de `caixas_restantes`, salva peso em `carregando`)
- Se a célula destino é um alvo `🟢` e o agente está **carregando** → o agente entrega a caixa (`carregando` volta para `None`)

---

### Função Objetivo

A verificação do objetivo está implementada **dentro do loop principal** de cada algoritmo em `Algorithms/dijkstra.py`, `ganancioso.py` e `astar.py`:

```python
if len(no_atual.caixas_restantes) == 0 and no_atual.carregando is None:
    return no_atual
```

O objetivo é atingido quando todas as caixas foram entregues e o agente não está carregando nenhuma caixa.

---

### Calcular Custo

O cálculo do custo está implementado em `functions.py` dentro da função `vizinhos()`, no momento em que cada novo `No` é gerado:

```python
if carregando is not None:
    custo_movimento = 1 + carregando
else:
    custo_movimento = 1
```

O custo acumulado `g` é atualizado em cada novo `No` criado:

```python
custo=no.custo + custo_movimento
```

---

### Função Heurística

A heurística utilizada é a **distância Manhattan** entre o agente e o objetivo mais próximo:

```
h = |linha_atual - linha_destino| + |col_atual - col_destino|
```

O cálculo varia conforme o estado do agente:

- **Carregando uma caixa** → distância até o alvo mais próximo
- **Sem carga** → distância até a caixa mais próxima + distância dessa caixa até o alvo mais próximo

```python
def heuristica(no, grid):
    if no.carregando is not None:
        return min(manhattan(agente, alvo) for alvo in grid.alvos)
    return min(
        manhattan(agente, caixa) + min(manhattan(caixa, alvo) for alvo in grid.alvos)
        for caixa in caixas_restantes
    )
```

#### Por que a heurística é admissível?

Uma heurística é **admissível** quando nunca superestima o custo real, ou seja: `h(n) ≤ custo_real(n)`

A distância Manhattan é admissível neste problema por três motivos:

1. **Caminho mínimo em grid**: em um grid sem diagonal, a distância Manhattan representa o menor número possível de passos entre dois pontos — o custo real só pode ser igual ou maior
2. **Ignora barreiras**: barreiras forçam caminhos mais longos, então o custo real será sempre ≥ h
3. **Ignora o peso das caixas**: a heurística conta 1 por passo, mas o custo real de carregar é `1 + peso` — portanto h nunca superestima

---

### Como os Estados são Salvos Internamente

Cada estado da busca é representado por um objeto `No`, que carrega:

```python
class No:
    linha, col          # posição atual
    caixas_restantes    # frozenset — imutável, usado como chave
    carregando          # None ou peso da caixa
    custo               # g — custo acumulado real
    predecessor         # No anterior — permite reconstruir o caminho
    movimento           # direção tomada (↑ ↓ ← →)
```

O caminho final é reconstruído percorrendo os predecessores de trás para frente, a partir do nó objetivo até o estado inicial.

---

## Algoritmos

### Dijkstra

Expande sempre o nó com **menor custo acumulado** (`g`). Garante o caminho ótimo mas pode explorar muitos nós desnecessários pois não tem noção de direção.

```
fila ordenada por: g
```

### Ganancioso

Expande sempre o nó com **menor estimativa até o objetivo** (`h`). É mais rápido mas não garante o caminho ótimo — pode tomar decisões ruins ao ignorar o custo já acumulado.

```
fila ordenada por: h
```

### A*

Combina os dois: expande o nó com **menor custo total estimado** (`g + h`). Garante o caminho ótimo e é mais eficiente que o Dijkstra pois usa a heurística para guiar a busca.

```
fila ordenada por: f = g + h
```

---

## Comparação dos Resultados

Grid de teste (5×5):

```
🙎⚪️⚪️⚪️⚪️
🟢🧱🧱1️⃣⚪️
⚪️⚪️🧱⚪️8️⃣
⚪️⚪️🧱⚪️⚪️
⚪️🟢⚪️⚪️⚪️
```

| Algoritmo | Custo Total | Movimentos | Caminho Ótimo? |
|---|---|---|---|
| **Dijkstra** | 64 | 19 | ✅ Sim |
| **Ganancioso** | 84 | 23 | ❌ Não |
| **A\*** | 64 | 19 | ✅ Sim |

O Ganancioso foi para a caixa `8️⃣` primeiro por estar mais próxima (`h` menor), sem considerar o alto custo de carregá-la. O Dijkstra e o A* identificaram que carregar a caixa `1️⃣` primeiro resulta no menor custo total.

---

## Execução

```bash
python solucao.py input/entrada.txt
```

Os arquivos de saída são gerados em `output/`:

- `dijkstra.txt`
- `ganancioso.txt`
- `a_estrela.txt`

Cada arquivo contém o estado final do grid, a sequência de movimentos e a quantidade total de movimentos.

---

## Estrutura do Projeto

```
Sokoban/
├── solucao.py
├── classes.py
├── functions.py
├── input/
│   └── entrada.txt
├── output/
│   ├── dijkstra.txt
│   ├── ganancioso.txt
│   └── a_estrela.txt
└── Algorithms/
    ├── __init__.py
    ├── dijkstra.py
    ├── ganancioso.py
    └── astar.py
```