from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/factcheck", methods=["POST"])
def factcheck():
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

        # Se encontrou resultados
        if "claims" in data:
            return jsonify({
                "fonte": "Google Fact Check",
                "quantidade": len(data["claims"]),
                "resultado": data["claims"][:2]  # só 2 pra não ficar gigante
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


if __name__ == "__main__":
    app.run(debug=True)