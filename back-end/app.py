from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import joblib
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

API_KEY = os.getenv("API_KEY")

def salvar_consulta(texto, origem, resultado):
    import os
    from datetime import datetime

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        pasta = os.path.abspath(os.path.join(BASE_DIR, "..", "dataset", "historico"))
        os.makedirs(pasta, exist_ok=True)

        caminho = os.path.join(pasta, "historico_consultas.csv")

        print("🔥 SALVANDO EM:", caminho)

        linha = f'"{datetime.now()}","{texto}","{origem}","{resultado}"\n'

        arquivo_existe = os.path.exists(caminho)

        with open(caminho, "a", encoding="utf-8") as f:
            if not arquivo_existe:
                f.write("data_hora,texto_pesquisado,origem,resultado\n")
            f.write(linha)

        print("🔥 SALVO COM SUCESSO")

    except Exception as e:
        print("💥 ERRO AO SALVAR:", str(e))

# =========================
# CARREGAR MODELO E VETORIZADOR
# =========================

model = joblib.load("model/modelo_fake_news.pkl")


# =========================
# GOOGLE FACT CHECK
# =========================

@app.route("/factcheck", methods=["POST"])
def factcheck():

    print(request.json)

    texto = request.json.get("texto")

    if not texto:
        return jsonify({"erro": "Texto não enviado"}), 400

    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    params = {
        "query": texto,
        "key": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()


        if "claims" in data:

            claims = data["claims"]

            resultados = []

            for claim in claims[:2]:

                if "claimReview" not in claim or not claim["claimReview"]:
                    continue

                review = claim["claimReview"][0]
                print("TÍTULO:", review.get("title", "SEM TÍTULO"))

                classificacao_original = review.get("textualRating", "")

                classificacao = classificacao_original.lower()

                # transforma underline em espaço
                classificacao = classificacao.replace("_", " ")

                if (
                    "falso" in classificacao
                    or "false" in classificacao
                    or "fake" in classificacao
                    or "enganoso" in classificacao
                    or "misleading" in classificacao
                    or "distorcido" in classificacao
                ):
                    classificacao = "Falso"

                elif (
                    "não é bem assim" in classificacao
                    or "nao e bem assim" in classificacao
                    or "needs context" in classificacao
                    or "sem contexto" in classificacao
                ):
                    classificacao = "Parcialmente verdadeiro"

                elif (
                    "verdadeiro" in classificacao
                    or "verdadero" in classificacao
                    or "true" in classificacao
                ):
                    classificacao = "Verdadeiro"

                else:
                    classificacao = classificacao_original

                resultados.append({
                    "afirmacao": claim.get("text", ""),
                    "classificacao": classificacao,
                    "fonte": review["publisher"].get("name", "Fonte desconhecida"),
                    "titulo": review.get("title", ""),
                    "link": review.get("url", "#")
                })

            resultado_final = "Sem resultado"

            if resultados:
                resultado_final = f"{resultados[0]['classificacao']} ({len(claims)} resultados)"
            print("🔥 ENTROU NO SALVAR API")
            salvar_consulta(
                texto,
                "Google Fact Check",
                resultado_final
            )
            print("🔥 SALVOU COM SUCESSO API")
            return jsonify({
                "fonte": "Google Fact Check",
                "quantidade": len(claims),
                "resultado": resultados
            })

        return jsonify({
            "fonte": "Google Fact Check",
            "resultado": "Nenhum resultado encontrado"
        })

    except Exception as e:
        return jsonify({
            "erro": "Erro ao consultar API",
            "detalhe": str(e)
        }), 500

    


# =========================
# MACHINE LEARNING
# =========================

@app.route("/ml", methods=["POST"])
def ml():

    try:

        texto = request.json.get("texto")

        if not texto:
            return jsonify({"erro": "Texto não enviado"}), 400

        previsao = model.predict([texto])[0]

        probabilidades = model.predict_proba([texto])[0]

        confianca = round(max(probabilidades) * 100, 2)

        resultado_final = str(previsao) if previsao is not None else "Sem previsão"

        print("🔥 ENTROU NO SALVAR ML")
        salvar_consulta(
            texto,
            "Machine Learning",
            resultado_final
        )
        print("🔥 SALVOU COM SUCESSO ML")
        return jsonify({
            "fonte": "Machine Learning",
            "classificacao": str(previsao),
            "confianca": confianca
        })
    

    except Exception as e:

        print("ERRO ML:", str(e))

        return jsonify({
            "erro": str(e)
        }), 500

    


if __name__ == "__main__":
    app.run(debug=True)