import csv

class Leitor2010 (object):
    def __init__(self):
        self.nomeArquivo = "/home/re/lentidaotrechos2010.csv"
        self.leitor = None

    def carregarDoDisco(self):
        with open(self.nomeArquivo, newline='', encoding='latin-1') as arquivoCSV:
            self.leitor = csv.reader(arquivoCSV, delimiter=";")
            for row in self.leitor:
                #print(row)
                pass

if __name__ == '__main__':
    leitor2010 = Leitor2010()
    leitor2010.carregarDoDisco()
