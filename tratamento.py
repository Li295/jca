import pandas as pd
from google.colab import files
import datetime
import numpy as np
from google.colab import drive
drive.mount('/content/drive')

# Encoding e delimitador específicos para ler CSVs brasileiros

df = pd.read_csv('/content/drive/MyDrive/acidentes-2025.csv',index_col=['id'], encoding="latin1", sep=";",)

#Correção de dados nulos

df['uop'] = df['uop'].fillna("NÃO ESPECIFICADA")

df['delegacia'] = df['delegacia'].fillna("NÃO INFORMADA")

df['regional'] = df['regional'].fillna("NÃO INFORMADA")

df['sexo'] = df['sexo'].fillna("Não Informado")

df['tipo_veiculo'] = df['tipo_veiculo'].fillna("Não Especificado")

df['classificacao_acidente'] = df['classificacao_acidente'].fillna("Não Classificado")

df['tipo_envolvido'] = df['tipo_envolvido'].fillna("Não Especificado")

df['estado_fisico'] = df['estado_fisico'].fillna("Desconhecido")

#Correção de formato do horário

df['horario'] = df['horario'].astype('string')

#Corrção de nome da coluna

df.rename(columns={'horario': 'hora'}, inplace=True)

df.rename(columns={'data_inversa': 'data'}, inplace=True)

#Remoção de colunas

df.drop('pesid', axis=1, inplace=True)

df.drop('id_veiculo', axis=1, inplace=True)

df.drop('uso_solo', axis=1, inplace=True)

#Correção da coluna idade

df.loc[df['idade'] > 120, 'idade'] = 0

#df['idade'].idxmax()

#indice_maximo = df['idade'].max()
#print(f"O índice do valor máximo é: {indice_maximo}")

#indice_maximo = df['idade'].idxmax()
#linha_maxima = df.loc[indice_maximo]
#print("idade")
#print(linha_maxima)

#CORREÇÃO VARIAÇÕES DE SEXO NÃO INFORMADO PARA APENAS 1 PADRÃO

df.sexo = df.sexo.replace({'Ignorado': 'Não Informado'})

#CORREÇÃO VARIAÇÕES PARA PADRANIZAÇÃO

df.marca = df.marca.replace({'Não Informado/Não Informado': 'NÃO INFORMADO'})

df.tipo_envolvido = df.tipo_envolvido.replace({'Cavaleiro': 'Não Especificado'})

df.estado_fisico = df.estado_fisico.replace({'Não Informado': 'Desconhecido'})

#df.isnull().sum()
#df.info()
#df['delegacia'].unique()
#df.head() #Visualização Tabela

