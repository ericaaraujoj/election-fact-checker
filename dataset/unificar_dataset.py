import pandas as pd
import glob

# pega todos os csv da pasta
arquivos = glob.glob("*.csv")

lista = []

for arquivo in arquivos:
    df = pd.read_csv(arquivo)
    lista.append(df)

# junta tudo
dataset_final = pd.concat(lista, ignore_index=True)

# salva
dataset_final.to_csv("dataset_final.csv", index=False)

print("Dataset unificado com sucesso!")