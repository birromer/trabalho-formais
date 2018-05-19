import itertools

class gramatica(object):
    def __init__(self):
        self.terminais = []
        self.variaveis = []
        self.inicial = []
        self.regras = []
        self.bonito = []




    def defFormal(self):
        var = ", ".join(self.variaveis)
        term = ", ".join(self.terminais)
        prod = ",\n".join(self.bonito)
        print("G = ({%s},{%s},P ,%s)" % (var, term, self.inicial))
        print("P = {%s}" % (prod.replace(", ", ",\n")))


    def removeVazios(self):
        prodVazio = []
        #faz fecho com produções vazias diretas
        for prod in self.regras:
            for var in prod:
                if var == 'V':
                    prodVazio.append(prod[0])
        diretoVazio = prodVazio.copy()
        #faz fecho com produções vazias indiretas
        tam = 0
        while (len(prodVazio) != tam):
            tam = len(prodVazio)
            for i in range(len(self.regras)):
                naoGeraVazio = 0
                for j in range(1, len(self.regras[i])):
                    if self.regras[i][j] not in prodVazio:
                        naoGeraVazio = 1
                if not naoGeraVazio and self.regras[i][0] not in prodVazio:
                        prodVazio.append(self.regras[i][0])
        #remove produções vazias diretas
        for prod in self.regras:
            naoGeraVazio = 0
            if prod[1] == 'V':
                self.regras.remove(prod)
        #gera produções substituindo as ocorrências das variáveis do fecho
        for var in prodVazio:
            for prod in self.regras:
                for item in prod:
                    if var in  item:
                        novaProd = [item for item in prod if item == prod[0] or item != var]
                        if novaProd not in self.regras and len(novaProd) > 1:
                            self.regras.append(novaProd)
        """
        #gera produção vazia a partir do inicial caso necessário
        if self.inicial in prodVazio:
            self.regras.append([self.inicial, 'V'])
        """

    def removeUnit(self):
        #cria fechos
        fechos = []
        for var in self.variaveis:
            fechos.append([var])
        #aumenta fecho com produções unitárias correspondentes
        for i in range(len(fechos)):
            tam = 0
            j = 0
            while tam != len(fechos[i]):
                tam = len(fechos[i])
                for prod in self.regras:
                    if prod[0] == fechos[i][j] and len(prod) == 2 and prod[1] not in fechos[i] and prod[1] in self.variaveis:
                        fechos[i].append(prod[1])
                j+=1        
        #remove produções unitárias
        i = 0
        while i < len(self.regras):
             if len(self.regras[i]) == 2 and self.regras[i][1] in self.variaveis:
                 self.regras.remove(self.regras[i])
             else:
                 i+=1
        #guacumula produções
        for fecho in fechos:
            for i in range(1,len(fecho)):
                for prod in self.regras:
                    if fecho[i] == prod[0]:
                        novaProd = []
                        novaProd.append(fecho[0])
                        for v in prod[1:]:
                            novaProd.append(v)
                        if novaProd not in self.regras:
                            self.regras.append(novaProd)
                        

    def removeInuteis(self):
        uteis = []
        #inicializa com variáveis que chegam em terminais
        for prod in self.regras:
            for item in prod[1:]:
                if item in self.terminais and prod[0] not in uteis:
                    uteis.append(prod[0])
        #elimina casos com variáveis do lado direito
        bla =[]
        #print(uteis)
        for var in uteis:
            for prod in self.regras:
                if prod[0] == var:
                    flag = 0
                    for l in prod[1:]:
                        if l in self.variaveis:
                            flag = 1
                    if flag == 0 and prod[0] not in uteis:
                        bla.append(prod[0])

        print(bla)

"""
criar lista com todas variaveis que levam APENAS a terminais (nao pode haver variavel do lado direito da produção)        
"""

#        print(uteis)
        input("k")

        #gera lista de símbolos antingíveis
        atingiveis = [self.inicial]
        for prod in self.regras:
            if prod[0] == self.inicial:
                for i in range(1,len(prod)):
                    if prod[i] not in self.terminais and prod[i] not in atingiveis:
                        atingiveis.append(prod[i])
        #exclui produções de variáveis que não levam a terminais
#        self.regras = filter(lambda x: x in uteis, self.regras)

                        

        

blabla = gramatica()
blabla.leGramatica("gramatica_exemplo3.txt")
#blabla.defFormal()
blabla.removeVazios()
blabla.removeUnit()
blabla.removeInuteis()
