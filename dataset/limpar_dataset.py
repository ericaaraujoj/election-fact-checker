import pandas as pd

# ==========================================
# LIMPEZA E PADRONIZAÇÃO AVANÇADA
# ==========================================
df = pd.read_csv("dataset_final.csv")

# 1. Remove espaços em branco bobos nas pontas de todas as colunas de texto
for col in df.select_dtypes(include=['object']).columns:
    df[col] = df[col].astype(str).str.strip()

# 2. LIMPEZA DO VEREDITO
coluna_veredicto = 'Verdict'

if column_veredicto := coluna_veredicto in df.columns:
    # Passa tudo para minúsculo temporariamente para facilitar a busca
    df[coluna_veredicto] = df[coluna_veredicto].astype(str).str.lower()

    # Cria uma nova coluna vazia para armazenar o resultado limpo
    veredito_limpo = pd.Series(index=df.index, dtype='object')

    # Se a frase contiver "falso", "false", "fake" ou "enganoso", vira apenas "Falso"
    mascara_falso = df[coluna_veredicto].str.contains('falso|false|fake|enganoso|misleading|distorcido', na=False)
    veredito_limpo[mascara_falso] = 'Falso'

    # Se contiver "verdadeiro", "verdadero" ou "true", vira apenas "Verdadeiro"
    mascara_verdadeiro = df[coluna_veredicto].str.contains('verdadeiro|true|verdadero', na=False)
    veredito_limpo[mascara_verdadeiro] = 'Verdadeiro'

    # Se contiver termos de "meio termo"
    mascara_parcial = df[coluna_veredicto].str.contains('parcial|contexto|context|não é bem assim', na=False)
    veredito_limpo[mascara_parcial] = 'Parcialmente verdadeiro'

    # O que não se encaixar em nenhum dos acima, mantém o texto original (mas com a primeira letra maiúscula)
    df[coluna_veredicto] = veredito_limpo.fillna(df[coluna_veredicto].str.title())


# 3. Remove duplicatas 
df.drop_duplicates(inplace=True)

# 4. Remove linhas cuja coluna de texto principal esteja vazia
coluna_principal = 'Claim' # Ajuste para o nome da sua coluna de texto principal
if coluna_principal in df.columns:
    df.dropna(subset=[coluna_principal], inplace=True)
else:
    df.dropna(subset=[df.columns[0]], inplace=True)

# Salva o arquivo final limpo na pasta correta
df.to_csv("dataset_final_limpo.csv")

print(f"🧹 Dataset limpo e simplificado! Total de linhas finais: {len(df)}")