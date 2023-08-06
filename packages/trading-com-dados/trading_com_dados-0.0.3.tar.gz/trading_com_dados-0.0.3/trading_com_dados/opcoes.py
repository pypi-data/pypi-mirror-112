import pandas as pd
import requests
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

def todate(data): return datetime.strptime(data, "%d/%m/%Y").date()
# Lista opções de um papel pelo site opcoes.net
class Opcoes:
    def __init__(self, papel):
        self.papel = papel if type(papel)==list else [papel]

    # Gera os vencimentos
    def __vencimentos(self, papel):
        url = f'https://opcoes.net.br/listaopcoes/completa?au=False&uinhc=0&idLista=ML&idAcao={papel}&listarVencimentos=true&cotacoes=true'
        response = requests.get(url, verify=False).json()
        vctos = [[i['value'], i['text']] for i in response['data']['vencimentos']]
        return vctos

    # Gera as lista de opções
    def __lista_opcoes(self, papel):
        vctos = self.__vencimentos(papel)
        opc=[]
        for vcto in vctos:
            url=f'https://opcoes.net.br/listaopcoes/completa?au=False&uinhc=0&idLista=ML&idAcao={papel}&listarVencimentos=false&cotacoes=true&vencimentos={vcto[0]}'
            response = requests.get(url, verify=False).json()
            opc += ([[papel]+[i[0][:i[0].find('_')]] + i[2:4] + [todate(vcto[1])] + [i[5]] + [i[8]] for i in response['data']['cotacoesOpcoes']])
            
        return opc

    # Gera a lista de todos os papeis
    def listar(self):
        if 'opc' in self.__dict__: return self.opc
        colunas = ['ativo_obj','ativo', 'tipo', 'mod', 'vcto', 'strike', 'preco']
        opc = [pd.DataFrame(self.__lista_opcoes(i), columns=colunas) for i in self.papel]
        self.opc= pd.concat(opc)
        return self.opc

def listarOpcoes(tickers):
    return Opcoes(tickers).listar()

