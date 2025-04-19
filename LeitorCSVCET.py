import csv

class Leitor2010 (object):
    def __init__(self):
        self.nomeArquivo = "/home/re/lentidaotrechos2010.csv"
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

    def relatar(self, data):
        if data not in self.dados.keys():
            print("Dado inexistente.")
            return
        print(self.dados[data])
                
if __name__ == '__main__':
    leitor2010 = Leitor2010()
    leitor2010.carregarDoDisco()
    print("Digite a data a consultar, no formato DD/MM/AA HH:MM.")
    data = input()
    leitor2010.relatar(data)
