     
        for prod in self.regras:
                if len(prod) == 2:
                    for fecho in fechos:
                        if fecho[0] == prod[0]  and prod[1] in self.variaveis and prod[1] not in fecho:
                            fecho.append(prod[1])

        tam = 0                
        while tam != :
            tam = len(fechos)
            for  in :
                if  :
                    for fecho in fechos:
                        if fecho[0] == prod[0]  and prod[1] in self.variaveis and prod[1] not in fecho:
                            fecho.append(prod[1])

        for prod in self.regras:
            for var in self.variaveis:
                if var not in prod[1:]:   
                    for terminal in self.terminais:
                            if terminal in prod and prod[0] not in uteis:
                                uteis.append(prod[0])





                                       for prod in self.regras:
            for item in prod[1:]:
                if item in self.terminais and prod[0] not in uteis:
                    uteis.append(prod[0])
        #elimina casos com variáveis do lado direito
        for var in uteis:
            for prod in self.regras:
                if prod[0] == var:
                    for v not in self.variaveis:
                        if v in prod[1:]
