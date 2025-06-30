import csv
import statistics

class LeitorCET (object):
    def __init__(self):
        self.nomeArquivo = "/home/re/2025/doutorado/MAC6931 Estudos Avançados em Sistemas de Software/dados/lentidaotrechos2017AvMercurio_normalizado.csv"
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

    def agregarCET_2017(self):
        ano = 2017
        for mes in range(1,13):
            for dia in range(1,32):
                for hora in range(0,24):
                    chave = "{}-{:0>2} {:0>2}:00".format(ano, mes, hora)
                    chaveAgregado = "{:0>2}:00".format(hora)
                    consulta = float(self.consultaLentidao(ano, mes, dia, hora, 0))
                    if consulta == 0.0:
                        continue
                    try:
                        self.agregado[chaveAgregado]["lentidao"] += consulta
                        self.agregado[chaveAgregado]["contagem"] += 1
                        self.agregado[chaveAgregado]["pontos"].append(consulta)
                    except KeyError:
                        self.agregado[chaveAgregado] = { "lentidao": consulta, "contagem": 1, "pontos": [ consulta ] }

                    chave = "{}-{:0>2} {:0>2}:30".format(ano, mes, hora)
                    chaveAgregado = "{:0>2}:30".format(hora)
                    consulta = float(self.consultaLentidao(ano, mes, dia, hora, 30))
                    if consulta == 0.0:
                        continue
                    try:
                        self.agregado[chaveAgregado]["lentidao"] += consulta
                        self.agregado[chaveAgregado]["contagem"] += 1
                        self.agregado[chaveAgregado]["pontos"].append(consulta)
                    except KeyError:
                        self.agregado[chaveAgregado] = { "lentidao": consulta, "contagem": 1, "pontos": [ consulta ] }

    def relatarAgregado_2017(self):
        for hora in range(0,24):
            chave = "{:0>2}:00".format(hora)
            try:
                print("{}; {}; {}; {}".format(chave, self.agregado[chave]["lentidao"], self.agregado[chave]["contagem"], statistics.stdev(self.agregado[chave]["pontos"])))
            except Exception as e:
                pass
            chave = "{:0>2}:30".format(hora)
            try:
                print("{}; {}; {}; {}".format(chave, self.agregado[chave]["lentidao"], self.agregado[chave]["contagem"], statistics.stdev(self.agregado[chave]["pontos"])))
            except Exception as e:
                pass
                
if __name__ == '__main__':
    leitor = LeitorCET()
    leitor.carregarDoDisco()
    leitor.agregarCET_2017()
    #print(leitor.agregado)
    leitor.relatarAgregado_2017()
