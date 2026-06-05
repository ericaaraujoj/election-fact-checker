import joblib

# Carrega modelo treinado
modelo = joblib.load('model/modelo_fake_news.pkl')

# Carrega vectorizer
vectorizer = joblib.load('model/vectorizer.pkl')


def prever(texto):

    texto_vetorizado = vectorizer.transform([texto])

    predicao = modelo.predict(texto_vetorizado)

    return predicao[0]


# Teste manual
if __name__ == '__main__':

    frase = input('Digite uma afirmação: ')

    resultado = prever(frase)

    print(f'Resultado: {resultado}')