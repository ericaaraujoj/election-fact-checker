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

def salvar_consulta(texto, origem, resultado, link_fonte="#", data_publicacao=None):
    import os
    import pandas as pd
    from datetime import datetime

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        pasta = os.path.abspath(os.path.join(BASE_DIR, "..", "dataset"))
        os.makedirs(pasta, exist_ok=True)
        caminho = os.path.join(pasta, "dataset_final_limpo.csv")

        print("🔥 PROCESSANDO SALVAMENTO EM:", caminho)

        # Trata a data de publicação (se não for enviada, usa a data atual)
        if not data_publicacao:
            data_publicacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Limpa quebras de linha e aspas para a checagem e salvamento
        texto_limpo = str(texto).replace("\n", " ").strip()
        resultado_limpo = str(resultado).strip()
        origem_limpa = str(origem).strip()

        # ==========================================
        # VERIFICAÇÃO DE DUPLICADOS COM PANDAS
        # ==========================================
        if os.path.exists(caminho):
            try:
                # Lê o CSV existente
                df_existente = pd.read_csv(caminho)
                
                # Verifica se o texto já existe na coluna 'Claim'
                # Usamos .astype(str).str.strip() para garantir que espaços extras não driblem a checagem
                if texto_limpo in df_existente['Claim'].astype(str).str.strip().values:
                    print(f"⚠️ CONSULTA IGNORADA: O texto já existe no dataset.")
                    return  # Interrompe a função e não salva
            except Exception as e:
                print(f"⚠️ Erro ao ler CSV para checagem de duplicados (computando como arquivo vazio): {e}")

        # Se passou pela checagem (ou o arquivo não existe), prepara a linha
        # Escapa as aspas duplas internas para manter o padrão CSV válido
        texto_csv = texto_limpo.replace('"', '""')
        resultado_csv = resultado_limpo.replace('"', '""')
        origem_csv = origem_limpa.replace('"', '""')

        linha = f'"{texto_csv}","{origem_csv}","{link_fonte}","{resultado_csv}","{data_publicacao}","",""\n'
        arquivo_existe = os.path.exists(caminho)

        with open(caminho, "a", encoding="utf-8") as f:
            if not arquivo_existe:
                f.write("Claim,Source Name,Source URL,Verdict,Review Publication Date,Image URL,Tags\n")
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

        # Garante que "claims" existe e não está vazio
        if "claims" in data and data["claims"]:

            claims = data["claims"]
            resultados = []

            for claim in claims[:2]:

                if "claimReview" not in claim or not claim["claimReview"]:
                    continue

                review = claim["claimReview"][0]
                print("TÍTULO:", review.get("title", "SEM TÍTULO"))

                classificacao_original = review.get("textualRating", "")
                classificacao = classificacao_original.lower().replace("_", " ")

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
                    "link": review.get("url", "#"),
                    "data_publicacao": review.get("reviewDate", None) 
                })

            # Processa o salvamento se houver checagens extraídas com sucesso
            if resultados:
                primeiro_resultado = resultados[0]
                
                print("🔥 ENTROU NO SALVAR API")
                salvar_consulta(
                    texto=primeiro_resultado["afirmacao"],
                    origem=primeiro_resultado["fonte"],           # Source Name
                    resultado=primeiro_resultado["classificacao"], # Verdict
                    link_fonte=primeiro_resultado["link"],         # Source URL
                    data_publicacao=primeiro_resultado["data_publicacao"] # Review Publication Date
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
        print("💥 ERRO NA ROTA FACTCHECK:", str(e))
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