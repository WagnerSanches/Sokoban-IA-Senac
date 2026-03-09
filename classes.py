import regex

class No:
    def __init__(self, linha, col, caixas_restantes, carregando=None, custo=0, predecessor=None, movimento=None):
        self.linha = linha
        self.col = col
        self.caixas_restantes = caixas_restantes
        self.carregando = carregando
        self.custo = custo
        self.predecessor = predecessor
        self.movimento = movimento   

    def posicao(self):
        return (self.linha, self.col)

    def estado(self):
        return (self.linha, self.col, self.caixas_restantes, self.carregando)

    def __lt__(self, outro):
        return self.custo < outro.custo
    
class Grid:
    AGENTE   = '🙎'
    VAZIO    = '⚪️'
    BARREIRA = '🧱'
    ALVO     = '🟢'
    NUMEROS  = {'1️⃣':1, '2️⃣':2, '3️⃣':3, '4️⃣':4, '5️⃣':5,
                 '6️⃣':6, '7️⃣':7, '8️⃣':8, '9️⃣':9}

    def __init__(self, caminho):
        self.grid = []
        self.agente = None
        self.caixas = {}       
        self.alvos = []
        self.barreiras = set()
        self.linhas = 0
        self.colunas = 0
        self._ler(caminho)

    def _ler(self, caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            for li, linha in enumerate(f):
                tokens = regex.findall(r'\X', linha.strip())
                row = []
                for ci, tok in enumerate(tokens):
                    pos = (li, ci)
                    if tok == self.AGENTE:
                        self.agente = pos
                    elif tok == self.ALVO:
                        self.alvos.append(pos)
                    elif tok == self.BARREIRA:
                        self.barreiras.add(pos)
                    elif tok in self.NUMEROS:
                        self.caixas[pos] = self.NUMEROS[tok]
                    row.append(tok)
                self.grid.append(row)
        self.linhas = len(self.grid)
        self.colunas = len(self.grid[0])
