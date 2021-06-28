import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd 
from pathlib import Path
import os
from funcoes import *

### PUXAR AS INFORMAÇÕES DA PLANILHA ###

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

caminho = r"C:\Users\Claudio\GitHub\Google_Sheets_API\creds.json" ##-- Diretorio onde se encontra a suas Credenciais para acessar a Planilha no Sheets
creds = ServiceAccountCredentials.from_json_keyfile_name(caminho, scope)
client = gspread.authorize(creds)
sheet = client.open('Vendas (respostas)') ##-- Nome da Planilha
sh1 = sheet.sheet1 ##-- Aba Selecionada para leitura
tabela = sh1.get_all_records()
df = pd.DataFrame(tabela) ##-- Transoformando em um DataFrame do Pandas
df = df.dropna()


# Remover Espaços ('\n') nas células, remover Coluans Inuteis.
remover_espacos(df)
try:
    df = df.drop(['Endereço de e-mail','ADESÃO'], axis=1)
except:
    df = df.drop(['ADESÃO'], axis=1)

# Transofrmar a coluna de Data/Hora em uma Coluna de Data/Hora reconhecida pelo Python
df['Carimbo de data/hora']= pd.to_datetime(df['Carimbo de data/hora'],format='%d/%m/%Y %H:%M:%S')


### TRATAR INFORMAÇÕES CONTENDO ERROS DENTRO DA MINHA TABELA ###

for i, item in enumerate(df['TELEFONE']):
    df['TELEFONE'][i] = str(df['TELEFONE'][i])

for i, cpf in enumerate(df['CPF']):
    df['CPF'][i] = arrumar_cpf(cpf) ##-- Padronizando os CPF's e tratando possíveis erros de digitação

for i , telefone in enumerate(df['TELEFONE']):
    df['TELEFONE'][i] = padronizar_telefones(telefone) ##-- Padronizando os Telefones e tratando possíveis erros de digitação

for i , texto in enumerate(df['NOME DO CLIENTE']):
    df['NOME DO CLIENTE'][i] = padronizar_texto(texto) ##-- Padronizando O Nome dos Clientes

for i, valor in enumerate(df['VALOR LIBERADO']): ##-- Padronizando Os valores, e tratando possíveis erros de digitação (Sem perder a informação do REAL valor digitado)
    if valor == 0:
        df['VALOR LIBERADO'][i] = float(valor)
    elif type(valor) != str:
        valor = str(valor)
    if type(valor) == str:
        valor.strip()
        if valor.count(',') >= 2:
            s = list(valor)
            s[-3] = s[-3].replace(',',':')
            valor = "".join(s).replace(',','').replace(':','.')
        else:
            valor = valor.replace('R$','').replace('.','').replace(',','.')
        df['VALOR LIBERADO'][i] = float(valor) 

for i, valor in enumerate(df['VALOR DA PARCELA']): ##-- Padronizando Os valores, e tratando possíveis erros de digitação (Sem perder a informação do REAL valor digitado)
    if valor == 0:
        df['VALOR DA PARCELA'][i] = float(valor)
    elif type(valor) != str:
        valor = str(valor)
    if type(valor) == str:
        valor.strip()
        valor = valor.replace('R$','')
        valor = valor.replace('.','').replace(',','.')
        df['VALOR DA PARCELA'][i] = float(valor)




### CALCULAR PORCENTAGEM PRÉ DETERMINADA E CRIAR UMA NOVA COLUNA ###

porcentagem = 0.04
df['Porcentagem calculada'] = df['VALOR LIBERADO'] * porcentagem
for i, valor in enumerate(df['Porcentagem calculada']):
    novo_valor = '{:.2f}'.format(df['Porcentagem calculada'][i])
    df['Porcentagem calculada'][i] = float(novo_valor)


### CRIAR UM DF FILTRO PARA CADA VENDEDOR | CRIAR UMA COLUNA COM O FATURAMENTO TOTAL E PORCENTAGEM TOTAL###

dict_aux = {}
for vendedor in df['VENDEDOR']:
    dict_aux[vendedor] = df.loc[df['VENDEDOR']==vendedor,:]
for loja in dict_aux:
    data = dict_aux[loja]
    data['Faturamento Total'] = ''
    data.iloc[0,14] = dict_aux[loja]["VALOR LIBERADO"].sum()
    data['Porcentagem Total'] = ''
    data.iloc[0,15] = dict_aux[loja]["Porcentagem calculada"].sum()


### ENCONTRAR O DESKTOP DO USUARIO ONDE FICARÁ A TABELA CONTROLE ###

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
path_desktop = Path(desktop)

### CRIAR A PLANILHA CONTROLE DE VENDAS NO DESKTOP ###

nome_arquivo = Path(path_desktop/'Controle Vendas.xlsx')
while True:
    if nome_arquivo.exists() == False:
        break
    else:
        os.remove(nome_arquivo)
while True:
    if nome_arquivo.exists() == False:
        df.to_excel(Path(path_desktop/'Controle Vendas.xlsx'),sheet_name='Controle', index = False)
    else:
        break
for nome in dict_aux:
    tabela = dict_aux[nome]
    with pd.ExcelWriter(nome_arquivo, engine='openpyxl', mode='a') as writer:  
        tabela.to_excel(writer, sheet_name=nome, index=False)