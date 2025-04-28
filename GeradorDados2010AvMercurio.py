import csv

class Leitor2010 (object):
    def __init__(self):
        self.nomeArquivo = "/home/re/lentidaotrechos2010AvMercurio.csv"
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
        data = "{}/{}/{} {}:{}".format(dia, mes, ano, hora, minuto)
        if data not in self.dados.keys():
            #print("Dado inexistente.")
            return
        print("20{}-{:0>2}-{:0>2} {:0>2}:{}:00; {}".format(ano, mes,dia, hora, minuto, self.dados[data]))

    def relatar2010(self):
        for mes in range(1,12):
            for dia in range(1,31):
                for hora in range(0,23):
                    #self.relatar("{}/{}/10".format(dia, mes), "{}:00".format(hora))
                    #self.relatar("{}/{}/10".format(dia, mes), "{}:30".format(hora))
                    self.relatar(10, mes, dia, hora, 0)
                    self.relatar(10, mes, dia, hora, 30)
                
if __name__ == '__main__':
    leitor2010 = Leitor2010()
    leitor2010.carregarDoDisco()
    #print("Digite a data a consultar, no formato DD/MM/AA HH:MM.")
    #data = input()
    leitor2010.relatar2010()
