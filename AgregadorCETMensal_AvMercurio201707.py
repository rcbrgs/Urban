import csv

class LeitorCET (object):
    def __init__(self):
        self.nomeArquivo = "/home/re/2025/doutorado/MAC6931 Estudos Avançados em Sistemas de Software/dados/lentidaotrechos2017AvMercurio.csv"
        self.leitor = None
        self.dados = { }
        self.agregado = { }

    def carregarDoDisco(self):
        with open(self.nomeArquivo, newline='', encoding='latin-1') as arquivoCSV:
            self.leitor = csv.reader(arquivoCSV, delimiter=";")
            next(self.leitor)
            for linha in self.leitor:
                self.processar(linha)
                #pass

    def processar(self, linha):
        if linha[0] in self.dados.keys():
            self.dados[linha[0]] += float(linha[5])
        else:
            self.dados[linha[0]] = float(linha[5])

    def consultaLentidao(self, ano, mes, dia, hora, minuto):
        data = "{}/{:0>2}/{} {}:{:0>2}".format(dia, mes, ano, hora, minuto)
        if data not in self.dados.keys():
            return 0
        return self.dados[data]

    def agregarCET_201707(self):
        ano = 2017
        mes = 7
        for mes in [ mes ]:
            for dia in range(1,32):
                for hora in range(0,24):
                    chave = "{}-{:0>2} {:0>2}:00".format(ano, mes, hora)
                    consulta = float(self.consultaLentidao(ano, mes, dia, hora, 0))
                    if consulta == 0.0:
                        continue
                    try:
                        self.agregado[chave]["lentidao"] += consulta
                        self.agregado[chave]["contagem"] += 1
                    except KeyError:
                        self.agregado[chave] = { "lentidao": consulta, "contagem": 1 }

                    chave = "{}-{:0>2} {:0>2}:30".format(ano, mes, hora)
                    consulta = float(self.consultaLentidao(ano, mes, dia, hora, 30))
                    if consulta == 0.0:
                        continue
                    try:
                        self.agregado[chave]["lentidao"] += consulta
                        self.agregado[chave]["contagem"] += 1
                    except KeyError:
                        self.agregado[chave] = { "lentidao": consulta, "contagem": 1 }

    def relatarAgregado_201707(self):
        ano = 2017
        mes = 7
        for mes in [ mes ]:
            for hora in range(0,24):
                chave = "{}-{:0>2} {:0>2}:00".format(ano, mes, hora)
                try:
                    print("{}; {}; {}".format(chave, self.agregado[chave]["lentidao"], self.agregado[chave]["contagem"]))
                except KeyError:
                    pass
                chave = "{}-{:0>2} {:0>2}:30".format(ano, mes, hora)
                try:
                    print("{}; {}; {}".format(chave, self.agregado[chave]["lentidao"], self.agregado[chave]["contagem"]))
                except KeyError:
                    pass
                
if __name__ == '__main__':
    leitor = LeitorCET()
    leitor.carregarDoDisco()
    leitor.agregarCET_201707()
    #print(leitor.agregado)
    leitor.relatarAgregado_201707()
