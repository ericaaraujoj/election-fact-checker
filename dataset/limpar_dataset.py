import pandas as pd


df = pd.read_csv('dataset_final.csv')


df.drop_duplicates(inplace=True)

df.dropna(inplace=True)


df.to_csv('dataset_final_limpo.csv', index=False)

print('Dataset limpo com sucesso!')