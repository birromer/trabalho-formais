class gramatica(object):
    def __init__(self):
        self.terminais = []
        self.variaveis = []
        self.inicial = []
        self.regras = []

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
                    i+=1

    def defFormal(self):
        var = ", ".join(self.variaveis)
        term = ", ".join(self.terminais)
        prod =  ",\n".join(self.regras)
        print("G = ({%s},{%s},P ,%s)" % (var, term, self.inicial))
        print("P = {%s}" % (prod.replace("   "," | ")))

blabla = gramatica()
blabla.leGramatica("gramatica_exemplo2.txt")
blabla.defFormal()
