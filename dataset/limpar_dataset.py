import pandas as pd

# carregar dataset
df = pd.read_csv("dataset_final.csv")

# remover duplicados
df = df.drop_duplicates()

# remover linhas vazias
df = df.dropna()

# salvar novo dataset
df.to_csv("dataset_final_limpo.csv", index=False)

print("Dataset limpo criado com sucesso!")