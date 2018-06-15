import itertools as it
import math
#import numpy as np
#import pandas as pd

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
        if '' in self.regras[-1]:
                        self.regras[-1].remove('')
        #for prod in self.regras:
        #   print(prod)


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
        #faz fecho com producoes vazias diretas
        for prod in self.regras:
            for var in prod:
                if var == 'V':
                    prodVazio.append(prod[0])
        diretoVazio = prodVazio[:]
        #faz fecho com producoes vazias indiretas
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
        #remove producoes vazias diretas
        for prod in self.regras:
            naoGeraVazio = 0
            if prod[1] == 'V':
                self.regras.remove(prod)

        def geraProdComb(prod, nRepetidas, posicoes, self):
            combInd =[]
            for i in range(1,nRepetidas+1):
                combInd += ([x for x in it.combinations(posicoes,i)])

            #combInd = lambda lista: [item for sublista in lista for item in sublista]

            for comb in combInd:
                novaProd = []
                for i in range(len(prod)):
                    if i not in comb:
                        novaProd.append(prod[i])
                if novaProd not in self.regras and len(novaProd) > 1:
                    self.regras.append(novaProd)


        #gera producoes substituindo as ocorrencias das variaveis do fecho
        for var in prodVazio:
            for prod in self.regras:
                for item in prod:
                    if var ==  item:
                        novaProd = [prod[0]]
                        varsProdVazioIguais = 0
                        varsIndices = []
                        for i in range(1,len(prod)):
                                if prod[i] == var:
                                    varsProdVazioIguais +=1
                                    varsIndices.append(i)

                        if varsProdVazioIguais >=2:
                            geraProdComb(prod,varsProdVazioIguais,varsIndices,self)
                        else:
                            for i in range(1,len(prod)):
                                if prod[i] != var:
                                    novaProd.append(prod[i])
                            if novaProd not in self.regras and len(novaProd) > 1:
                                self.regras.append(novaProd)

        #gera producao vazia a partir do inicial caso necessario
        if self.inicial in prodVazio:
            self.regras.append([self.inicial, 'V'])
            if 'V' not in self.terminais:
                self.terminais.append('V')


    def removeUnit(self):
        #cria fechos
        fechos = []
        for var in self.variaveis:
            fechos.append([var])
        #aumenta fecho com producoes unitarias correspondentes
        for i in range(len(fechos)):
            tam = 0
            j = 0
            while tam != len(fechos[i]):
                tam = len(fechos[i])
                for prod in self.regras:
                    if prod[0] == fechos[i][j] and len(prod) == 2 and prod[1] not in fechos[i] and prod[1] in self.variaveis:
                        fechos[i].append(prod[1])
                j+=1
        #remove producoes unitarias
        i = 0
        while i < len(self.regras):
             if len(self.regras[i]) == 2 and self.regras[i][1] in self.variaveis:
                 self.regras.remove(self.regras[i])
             else:
                 i+=1
        #guacumula producoes
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
        #inicializa com variaveis que chegam apenas em terminais
        for prod in self.regras:
            temp = list(filter(lambda x: x in self.terminais, prod))
            if len(temp) == len(prod) - 1 and prod[0] not in uteis:
                uteis.append(prod[0])
        #gera lista de todos simbolos indiretamente que chegam em terminais
        for prod in self.regras:
            for util in uteis:
                if util in prod[1:] and prod[0] not in uteis:
                    uteis.append(prod[0])
        #remove as variaveis que nao chegam em terminais
        self.variaveis = [var for var in self.variaveis if var in uteis]
        temp = []
        for prod in self.regras:
            adiciona = 1
            for item in prod:
                if item not in uteis :
                    adiciona = 0
                    break
            if adiciona == 1:
                temp.append(prod)
            elif  adiciona == 0 and item in self.terminais:
                temp.append(prod)
        self.regras = temp
        #gera lista de variaveis antingiveis
        varAtingiveis = [self.inicial]
        tam = 0
        while tam !=  len(varAtingiveis):
            tam = len(varAtingiveis)
            for prod in self.regras:
                if prod[0] in varAtingiveis:
                    for i in range(1,len(prod)):
                        if prod[i] not in self.terminais and prod[i] not in varAtingiveis:
                            varAtingiveis.append(prod[i])
         #gera lista de terminais atingiveis
        terAtingiveis = []
        for prod in self.regras:
            for item in prod:
                if item in self.terminais and prod[0] in varAtingiveis:
                    terAtingiveis.append(item)
        #remove as variaveis que nao sao atingiveis
        self.regras = [prod for prod in self.regras if prod[0] in varAtingiveis]
        self.variaveis = [var for var in self.variaveis if var in varAtingiveis]
        self.terminais = [ter for ter in self.terminais if ter in terAtingiveis]


    def simplifica(self):
        self.removeVazios()
        self.removeUnit()
        self.removeInuteis()


    def djowsky(self):
        #simplifica
        self.simplifica()
        #remove producao vazia a partir da variavel inidial
        for prod in self.regras:
            if prod[0] == self.inicial:
                for item in prod:
                    if item == 'V':
                        self.regras.remove(prod)
        #gera variaveis novas e producoes unitarias para os terminais
        ind = 0
        while ind < len(self.regras):
            if len(self.regras[ind]) >= 3:
                for s in range(1,len(self.regras[ind])):
                    if self.regras[ind][s] in self.terminais:
                        troca = "C" + self.regras[ind][s]
                        if troca not in self.variaveis:
                            self.variaveis.append(troca)
                            novaProd = [troca, self.regras[ind][s]]
                            self.regras.append(novaProd)
                        self.regras[ind][s] = troca
            ind+=1
        #transforma producoes em equivalentes com no maximo 2 variaveis
        i = 0
        while i < len(self.regras):
            if len(self.regras[i]) >= 4:
                novaVar = str(self.regras[i][2]) + "".join(self.regras[i][3:]).lower()
                novaProd = [novaVar] + self.regras[i][2:]
                if novaProd not in self.regras:
                    self.regras.append(novaProd)
                if novaVar not in self.variaveis:
                    self.variaveis.append(novaVar)
                self.regras[i] = self.regras[i][:2]
                self.regras[i].append(novaVar)
            i+=1


    def geraArvoreDerivacao(self, tabela, base):

        def encontraTerminais(arvore, i, terminais):
            #retorna a lista com o terminal encontrado adicionado
            if len(arvore[i]) == 2:
                return terminais + [arvore[i][1]]
           #no caso de nao haver nodo na posicao apenas ignora o conteudo
            elif arvore[i] == []:
                return terminais
            else:
                if ((i+1)*2) < len(arvore):
                    #dada a existencia das novas posicoes, chama recursao com filhos
                    return encontraTerminais(arvore, ((i+1)*2)-1, terminais) + encontraTerminais(arvore, ((i+1)*2), terminais)


        def verificaFim(arvore):
            #geração da lista de folhas
            folhas = encontraTerminais(arvore, 0, [])
            #ja elimina caso numero de terminais seja diferente
            if len(folhas) != len(base):
                    return False
            else:
                for i in range(len(base)):
                    if folhas[i] != base[i]:
                        return False
            #encontra arvore funcional quando todos elementos das listas sao iguais
            return True

        def numeroFolhas(arvore):
            folhas = 0
            ultimoInd = 0
            naoVazios = 0
            #gera numero de nodos nao vazios e indice do ultimo nodo
            for i in range(len(arvore)):
                if len(arvore[i]) > 0:
                    ultimoInd = i
                if arvore[i] != []:
                    naoVazios += 1
            for i in range(ultimoInd+1):
                if len(arvore[i]) == 3:
                    if (i+1)*2-1 >= len(arvore):
                       #se ambos filhos estariam fora da arvore, é folha
                        folhas += 1
                    elif (i+1)*2 >= len(arvore) and (i+1)*2-1 < len(arvore):
                        #se apenas um dos filhos se encontra fora da arvore, é folha se o outro for nulo
                        if arvore[(i+1)*2-1] == []:
                            folhas += 1
                    elif (i+1)*2 < len(arvore):
                        #quando ambos filhos estao dentro da arvore
                        #é folha ao ter ao menos um dos filhos vazio
                        if arvore[(i+1)*2-1] == [] and not arvore[(i+1)*2] == []:
                            folhas += 1
                        elif not arvore[(i+1)*2-1] == [] and arvore[(i+1)*2] == []:
                            folhas += 1
                        elif arvore[(i+1)*2-1] == [] and arvore[(i+1)*2] == []:
                            folhas += 1
                elif len(arvore[i]) == 2:
                    #todas producao de terminal sao folha
                    folhas+=1
            return folhas

        def pa(arvore):
            i = 0
            b = 0
            for j in range(len(arvore)):
                if arvore[j] == []:
                    print('-', end='   ')
                else:
                    print(arvore[j][0], end='   ')
                b+=1
                if b == 2**i:
                    print('\n')
                    i+=1
                    b=0

        def pt(arvores):
            for arvore in arvores:
                print(arvore)
                print('\n')

        def jaFalhou(arvore):
            #eh possivel elimitar arvores prematuramente ao verificar que elas possuem terminais que diferem do esperado
            finais = []
            for i in range(len(arvore)):
                if arvore[1] in self.terminais:
                    finais.append(arvore[1])
            for i in range(len(finais)):
                if finais[i] != base[i]:
                    return False
            return True

        posProds = []
        #junta todas producoes de variaveis possivelmente utilizadas na arvore
        for i in range(len(tabela)-1):
            for j in range(len(tabela[i])):
                pProds = [] #possiveis producoes a serem selecionadas
                k = len(tabela)-2
                posDX = i+1
                posDY = j+1
                while k != i:
                    for var1 in tabela[k][j]:
                        for var2 in tabela[posDX][posDY]:
                            for prod in self.regras:
                                if prod[1] == var1 and prod[2] == var2: #and len(prod) == 2 nao precisa pois ja na forma normal
                                    if prod not in pProds:
                                        pProds.append(prod)
                    if pProds not in posProds:
                        posProds.append(pProds)
                    posDX+=1
                    posDY+=1
                    k-=1
        #adiciona todas producoes de terminais possivelmente utilizadas na arvore e limpa lista
        temp = []
        for pProd in posProds:
            for prod in pProd:
                if prod not in posProds and prod not in temp:
                    temp.append(prod)
        for prod in self.regras:
            for pProds in posProds:
                for posProd in pProds:
                    if prod[1] in base and prod[0] in posProd[1:]:
                        if prod not in posProds and prod not in temp:
                            temp.append(prod)
        posProds = temp[:]
        #inicializa lista de arvores com listas com o numero maximo de nodos
        arvores = [[[] for y in range(2**(len(base)+1))] for x in range(1500)]
        arvoresNice = []

        #inicializa primeiras arvores com todas producoes que partem do simbolo inicial
        indAr = 0
        for prod in posProds:
            if prod[0] == self.inicial:
                arvores[indAr][0] = prod
                indAr += 1
        indAr -=1

        i = 0
        #itera pelo vetor de arvores enquanto o indice da ultima arvore ocupada nao cresce
        while i <= indAr:
            j=0
            #itera por todas producoes de cada arvore
            while j < len(arvores[i]):
                #quando eh uma producao de variaveis
                if len(arvores[i][j]) == 3:
                    preenchido = 0   #flag para verificar se ja preencheu a arvore no inidice i
                    for prod in posProds:
                        if arvores[i][j][1] == prod[0] and preenchido == 0:
                            #quando encontra uma producao encabeceada pela variaveis na esquerda da prod atual na arvore
                            #se o indice do filho esta dentro da arvore
                            if ((j+1)*2)-1 < 2**len(base):
                                #se a producao atual e vazia, a fim de nao sobrescrever as arvoreds geradas pelas iteracoes anteriores
                                if arvores[i][((j+1)*2)-1] == []:
                                    #copia a arvore atual para uma variavel temporaria a fim de testar se deve incluir na arvore
                                    arTemp = arvores[i][:]
                                    arTemp[((j+1)*2)-1] = prod
                                    #dado que a arvore a ser incluida nao viola o limite de folhas, nao se encontra na arvore nem teve problema na geracao de terminais
                                    if arTemp not in arvores and numeroFolhas(arTemp) <= len(base) and jaFalhou(arTemp):
                                        arvores[i][((j+1)*2)-1] = prod
                                        preenchido = 1
                            #ignora arvore quando numero de folhas viola limite da entrada
                            if numeroFolhas(arvores[i]) > len(base):
                                break
                            #testa se a arvore atual ja se encontra completa e correta de acordo com a entrada
                            if verificaFim(arvores[i]):
                                if arvores[i] not in arvoresNice:
                                    arvoresNice.append(arvores[i])
                                    break
                        #quando a arvore do indice i ja esta preenchida entao vai para a primeira diposnivel a partir do incide da ultima arvore na lista
                        elif arvores[i][j][1] == prod[0] and preenchido == 1:
                            if ((j+1)*2)-1 < 2**len(base):
                                tempAr = arvores[i][:]
                                tempAr[((j+1)*2)-1] = prod
                                if tempAr not in arvores and numeroFolhas(tempAr) <= len(base) and jaFalhou(tempAr):
                                    indAr += 1
                                    arvores[indAr] = arvores[i][:]
                                    arvores[indAr][((j+1)*2)-1] = prod
                            if numeroFolhas(arvores[indAr]) > len(base):
                                break
                            if verificaFim(arvores[i]):
                                if arvores[i] not in arvoresNice:
                                    arvoresNice.append(arvores[i])
                                    break
                    preenchido = 0
                    #repete o processo anterior mas para a derivacao a direita
                    for prod in posProds:
                        if arvores[i][j][2] == prod[0] and preenchido == 0:
                            if ((j+1)*2) < 2**(len(base)+1):
                                if arvores[i][((j+1)*2)] == []:
                                    arTemp = arvores[i][:]
                                    arTemp[((j+1)*2)] = prod
                                    if arTemp not in arvores and numeroFolhas(arTemp) <= len(base) and jaFalhou(arTemp):
                                        arvores[i][((j+1)*2)] = prod
                                        preenchido = 1
                            if numeroFolhas(arvores[i]) > len(base):
                                break
                            if verificaFim(arvores[i]):
                                if arvores[i] not in arvoresNice:
                                    arvoresNice.append(arvores[i])
                                    break
                        elif arvores[i][j][2] == prod[0] and preenchido == 1:
                            if ((j+1)*2) < 2**(len(base)+1):
                                tempAr = arvores[i][:]
                                tempAr[((j+1)*2)] = prod
                                if tempAr not in arvores and numeroFolhas(tempAr) <= len(base) and jaFalhou(tempAr):
                                    indAr += 1
                                    arvores[indAr] = arvores[i][:]
                                    arvores[indAr][((j+1)*2)] = prod
                            if numeroFolhas(arvores[indAr]) > len(base):
                                break
                            if verificaFim(arvores[i]):
                                if arvores[i] not in arvoresNice:
                                    arvoresNice.append(arvores[i])
                                    break
                elif len(arvores[i][j]) == 2:
                    if ((j+1)*2)-1 < 2**(len(base)+1):
                        if arvores[i][((j+1)*2)-1] == []:
                            arvores[i][((j+1)*2)-1] = [arvores[i][j][1]]
                    
                    
                    
                j=j+1
            i=i+1
        if arvoresNice != []:
            print("UHULESUCESSO")
            print("gastaste!")
            for arvore in arvoresNice:
                print("AQUI TEM SUCESSO")
                pa(arvore)
                print('\n')
        else:
            print("deu ruim")



    def parserCYK(self, entrada):
        aceita = 0
        def pt(tabela):
            for linha in tabela:
                print(linha)
        #separa terminais da entrada
        if ' ' in entrada:
            base = entrada.split(' ')
        else:
            base = entrada.split()
        #gera tabela com as proporçoes da entrada
        tabela = [[x for x in range(len(base))] for x in range(len(base)+1)]
        #remove matriz triangular superior por não ser necessária
        for i in range(len(tabela)-1):
            for j in range(len(tabela)-2,-1,-1):
                if j > i:
                    tabela[i].remove(tabela[i][j])
        #passa para a base da tabela o conteudo da entrada
        for i in range(len(base)):
            tabela[len(base)][i] = base[i]
        #preenche penultima linha da tabela com variaveis que levam ao item na
        # mesma coluna da linha abaixo
        for j in range(len(tabela)-1):
            i = len(tabela)-2
            if j <= i:
                novaCelula = []
                for prod in self.regras:
                    if tabela[len(tabela)-1][j] in prod[1:]:
                        novaCelula.append(prod[0])
                tabela[i][j] = novaCelula
        #preenche o resto da tabela com os geradores das linhas abaixo
        for i in reversed(range(len(base)-1)):
            for j in range(len(tabela[i])):
               prods = []
               k = len(tabela)-2
               posDX = i+1
               posDY = j+1
               while k != i:
                   for var1 in tabela[k][j]:
                       for var2 in tabela[posDX][posDY]:
                           for prod in self.regras:
                               if prod[1] == var1 and prod[2] == var2: #and len(prod) == 2 nao precisa pois ja na forma normal
                                   if prod[0] not in prods:
                                       prods.append(prod[0])
                   tabela[i][j] = prods
                   posDX+=1
                   posDY+=1
                   k-=1
        #muda var de aceita/rejeita de acordo com matriz resultante
        if self.inicial in tabela[0][0]:
            aceita = 1
        #embeleza matriz resultante
 #       printavel = np.matrix(tabela)
 #       print(pd.DataFrame(printavel))
        #imprime resultado e chama criacao da arvore de derivacao
        if aceita:
            print("Entrada aceita")
            pt(tabela)
            print('\n')
            #print(pt.DataFrame(tabela))
            self.geraArvoreDerivacao(tabela, base)
        else:
            pt(tabela)
            print("Entrada rejeitada")

if __name__ == "__main__":
    blabla = gramatica()
#    blabla.leGramatica("gramatica_exemplo6.txt")
    blabla.leGramatica("gramatica_exemplo5.txt")
#    blabla.leGramatica("gramatica_exemplo2.txt")
#    blabla.leGramatica("gramatica_exemplo1.txt")
#    blabla.defFormal()
    blabla.djowsky()
#    blabla.parserCYK("x o x")
    blabla.parserCYK("x + x * x")
#    blabla.parserCYK("dog runs in the park")
#    blabla.parserCYK("a a b a")
