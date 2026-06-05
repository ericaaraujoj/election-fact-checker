import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.pipeline import Pipeline

# Carregar dataset
df = pd.read_csv("../dataset/dataset_final_limpo.csv")

# Remover valores vazios
df = df.dropna(subset=["Claim", "Verdict"])

# Texto e classes
X = df["Claim"]
y = df["Verdict"]

# Dividir treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Pipeline ML
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Treinar
model.fit(X_train, y_train)

# Previsões
y_pred = model.predict(X_test)

# Métricas
print("\nAccuracy:")
print(accuracy_score(y_test, y_pred))

print("\nRelatório:")
print(classification_report(y_test, y_pred))

# Salvar modelo
joblib.dump(model, "model/modelo_fake_news.pkl")

print("Modelo treinado e salvo com sucesso!")