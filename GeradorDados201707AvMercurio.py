import csv

class LeitorCET (object):
    def __init__(self):
        self.nomeArquivo = "/home/re/2025/doutorado/MAC6931 Estudos Avançados em Sistemas de Software/dados/lentidaotrechos2017AvMercurio.csv"
        self.leitor = None
        self.dados = { }

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

    def relatar(self, ano, mes, dia, hora, minuto):
        data = "{}/{:0>2}/{} {}:{:0>2}".format(dia, mes, ano, hora, minuto)
        #print(data)
        if data not in self.dados.keys():
            #print("{} não é chave de self.data".format(data))
            return
        print("{}-{:0>2}-{:0>2} {:0>2}:{}:00; {}".format(ano, mes, dia, hora, minuto, self.dados[data]))

    def relatarCET(self):
        ano = 2017
        for mes in range(1,13):
            for dia in range(1,32):
                for hora in range(0,24):
                    #print("20{}-{:0>2}-{:0>2} {:0>2}:".format(ano, mes, dia, hora))
                    self.relatar(ano, mes, dia, hora, 0)
                    self.relatar(ano, mes, dia, hora, 30)
                
if __name__ == '__main__':
    leitor = LeitorCET()
    leitor.carregarDoDisco()
    leitor.relatarCET()
    #print(leitor.dados)
