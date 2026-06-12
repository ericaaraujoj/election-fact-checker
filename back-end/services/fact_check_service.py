import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


def buscar_fact_check(texto):

    url = 'https://factchecktools.googleapis.com/v1alpha1/claims:search'

    params = {
        'query': texto,
        'key': API_KEY,
        'languageCode': 'pt-BR'
    }

    resposta = requests.get(url, params=params)

    dados = resposta.json()

    claims = dados.get('claims')

    if claims:

        claim = claims[0]

        review = claim['claimReview'][0]

        return {
            'titulo': claim.get('text'),
            'classificacao': review.get('textualRating'),
            'autor': review.get('publisher', {}).get('name')
        }

    return None