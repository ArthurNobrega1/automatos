class AFD:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def processar_cadeia(self, cadeia):
        estado_atual = self.estado_inicial

        for simbolo in cadeia:
            if simbolo not in self.alfabeto:
                return False

            estado_atual = self.transicoes.get((estado_atual, simbolo))
            if estado_atual is None:
                return False  
        return estado_atual in self.estados_aceitacao
    
class AFN:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def processar_cadeia(self, cadeia):
        estados_atuais = {self.estado_inicial}

        for simbolo in cadeia:
            novos_estados = set()
            for estado in estados_atuais:
                transicoes_estado = self.transicoes.get((estado, simbolo), set())
                novos_estados.update(transicoes_estado)

            estados_atuais = novos_estados

        return bool(estados_atuais.intersection(self.estados_aceitacao))
    
class AFNe:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def processar_cadeia(self, cadeia):
        estados_aux = {}
        estados_atuais = {self.estado_inicial}
        
        estados_visitados = set()
        while True:
            novos_estados = set()
            for estado in estados_atuais:
                transicoes_vazias = self.transicoes.get((estado, ''), set())
                novos_estados.update(transicoes_vazias)
            if novos_estados in estados_visitados or not transicoes_vazias:
                for conjunto in estados_visitados:
                    estados_atuais.update(conjunto)
                break
            
            estados_atuais = novos_estados
            estados_visitados.add(frozenset(estados_atuais))
    
        if (cadeia):
            estados_atuais.update({self.estado_inicial})
            
        for simbolo in cadeia:
            if (not novos_estados and {self.estado_inicial} == estados_aux): 
                break

            novos_estados = set()
            for estado in estados_atuais:
                estados_visitados = set()
                estados_aux = {estado}
                while True:
                    for estado_aux in estados_aux:
                        transicoes_vazias = self.transicoes.get((estado_aux, ''), set())
                        novos_estados.update(transicoes_vazias)
                    if novos_estados in estados_visitados or not transicoes_vazias:
                        break
                    
                    estados_aux = transicoes_vazias
                    estados_visitados.add(frozenset(estados_atuais))

                transicoes_estado = self.transicoes.get((estado, simbolo), set())
                novos_estados.update(transicoes_estado)
            estados_atuais = novos_estados

        estados_visitados = set()
        estados_aux = {estado}
        while True and novos_estados and {self.estado_inicial} == estados_aux:
            for estado_aux in estados_aux:
                transicoes_vazias = self.transicoes.get((estado_aux, ''), set())
                novos_estados.update(transicoes_vazias)
            if novos_estados in estados_visitados or not transicoes_vazias:
                break
            
            estados_aux = transicoes_vazias
            estados_visitados.add(frozenset(estados_atuais))
        if novos_estados:
            estados_atuais = novos_estados

        return bool(estados_atuais.intersection(self.estados_aceitacao))

if __name__ == "__main__":
    # AFD teste
    estados = {'q0', 'q1', 'q2'}
    alfabeto = {'0', '1'}
    transicoes = {
        ('q0', '0'): 'q1',
        ('q0', '1'): 'q0',
        ('q1', '0'): 'q2',
        ('q1', '1'): 'q0',
        ('q2', '0'): 'q2',
        ('q2', '1'): 'q2'
    }
    estado_inicial = 'q0'
    estados_aceitacao = {'q2'}
    afd = AFD(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

    cadeias_teste = ['101', '1001', '010', '1010']
    for cadeia in cadeias_teste:
        if afd.processar_cadeia(cadeia):
            print(f'A cadeia "{cadeia}" foi aceita pelo AFD.')
        else:
            print(f'A cadeia "{cadeia}" foi rejeitada pelo AFD.')

    # AFN teste
    estados = {'q0', 'q1', 'q2'}
    alfabeto = {'0', '1'}
    transicoes = {
        ('q0', '0'): {'q1'},
        ('q0', '1'): {'q0'},
        ('q1', '0'): {'q2'},
        ('q1', '1'): {'q0', 'q2'},
        ('q2', '0'): {'q2'},
        ('q2', '1'): {'q2'}
    }
    estado_inicial = 'q0'
    estados_aceitacao = {'q2'}
    afn = AFN(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

    cadeias_teste = ['101', '1001', '010', '1010']
    for cadeia in cadeias_teste:
        if afn.processar_cadeia(cadeia):
            print(f'A cadeia "{cadeia}" foi aceita pelo AFN.')
        else:
            print(f'A cadeia "{cadeia}" foi rejeitada pelo AFN.')


    # AFNe teste
    estados = {'q0', 'q1', 'q2', 'q3'}
    alfabeto = {'0', '1'}
    transicoes = {
        ('q0', ''): {'q1'}, 
        ('q1', '0'): {'q2'},
        ('q1', ''): {'q2'},
        ('q2', ''): {'q3'},
        ('q3', '1'): {'q1'},
        ('q3', '0'): {'q2'}
    }
    estado_inicial = 'q0'
    estados_aceitacao = {'q3'}

    afne = AFNe(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)

    cadeias_teste = ['001', '1001', '001001','','001010010101000110101']
    for cadeia in cadeias_teste:
        if afne.processar_cadeia(cadeia):
            print(f'A cadeia "{cadeia}" foi aceita pelo AFNe.')
        else:
            print(f'A cadeia "{cadeia}" foi rejeitada pelo AFNe.')