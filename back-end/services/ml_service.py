import joblib

modelo = joblib.load('model/modelo_fake_news.pkl')
vectorizer = joblib.load('model/vectorizer.pkl')


def prever_fake_news(texto):

    texto_vetorizado = vectorizer.transform([texto])

    predicao = modelo.predict(texto_vetorizado)

    return predicao[0]