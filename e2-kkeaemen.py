import itertools

class gramatica(object):
    def __init__(self):
        self.terminais = []
        self.variaveis = []
        self.inicial = []
        self.regras = []
        self.bonito = []

    def formataProd(self):
        self.regras =  ",".join(self.regras)
        self.regras = self.regras.replace(" ", "", 1)
        self.regras = self.regras.replace("   "," ")
        self.regras = self.regras.replace("  >  "," ")
        self.regras = self.regras.replace(" ,",",")
        self.regras = self.regras.split(", ")
        for i in range(len(self.regras)):
            self.regras[i] = self.regras[i].split(' ')
        self.regras[-1].remove('')

        
    def leGramatica(self, nomeArquivo):
        with open(nomeArquivo,"r") as arq:
            conteudo= arq.read().splitlines()
        for i in range(0,conteudo.index("#Regras")):
            conteudo[i] = conteudo[i].replace('\t', '')
            conteudo[i] = conteudo[i].replace('[', '')
            conteudo[i] = conteudo[i].replace(']', '')
            conteudo[i] = conteudo[i].replace(' ', '')
        for i in range(conteudo.index("#Regras"),len(conteudo)):
            conteudo[i] = conteudo[i].replace('\t', '')
            conteudo[i] = conteudo[i].replace('[', '')
            conteudo[i] = conteudo[i].replace(']', '')
        for i in range(len(conteudo)):
            if conteudo[i] == "#Terminais":
                for n in range(i+1,conteudo.index("#Variaveis")):
                    self.terminais.append(conteudo[n])
                    i+=1
            elif conteudo[i] == "#Variaveis":
                for n in range(i+1,conteudo.index("#Inicial")):
                    self.variaveis.append(conteudo[n])
                    i+=1
            elif conteudo[i] == "#Inicial":
                self.inicial = conteudo[i+1]
            elif conteudo[i] == "#Regras":
                for n in range(i+1,len(conteudo)):
                    self.regras.append(conteudo[n])
                    self.bonito.append(conteudo[n])
                    i+=1
        self.formataProd()


    def defFormal(self):
        var = ", ".join(self.variaveis)
        term = ", ".join(self.terminais)
        prod = ",\n".join(self.bonito)
        print("G = ({%s},{%s},P ,%s)" % (var, term, self.inicial))
        print("P = {%s}" % (prod.replace(", ", ",\n")))


    def removeVazios(self):
        prodVazio = []
        for prod in self.regras:
            for var in prod:
                if var == 'V':
                    prodVazio.append(prod[0])
        tam = 0
        while (len(prodVazio) != tam):
            tam = len(prodVazio)
            for prod in self.regras:
                for i in range(1,len(prod)):
                    if var in prodVazio:
                        prodVazio.append(prod[0])

        P1 = []

        for prod in self.regras:
            for i in range(1,len(prod)):
                if i == 'V':
                    pass
                else:
                    P1.append(prod)
                    

        print(P1)
        input("kk")
                        
        thatsWhatYouGottaDo = []
        

    def removeUnit(self):
        pass

    def removeInuteis(self):
        pass
    
blabla = gramatica()
blabla.leGramatica("gramatica_exemplo2.txt")
blabla.defFormal()
blabla.removeVazios()
