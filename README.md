# Election Fact Checker

# Equipe

- Érica Araujo de Jesus
- Mickael Cedraz Alencar
- Monyc Luísa Almeida de Cerqueira
- Nalbert de Souza Santana
- Pedro César Paixão de Jesus
- Tiago Sângil Palmeira Lima

---

## Descrição

O Election Fact Checker é uma aplicação acadêmica desenvolvida na disciplina de Inteligência Artificial para auxiliar na verificação de informações relacionadas ao contexto eleitoral brasileiro.

O sistema utiliza:

- Google Fact Check API
- Processamento de Linguagem Natural (PLN)
- Machine Learning
- Dataset de verificações de fatos

Quando o usuário envia uma afirmação, o sistema:

1. Consulta a API do Google Fact Check
2. Caso exista uma verificação oficial:
   - retorna o resultado ao usuário
   - armazena a informação no dataset local
3. Caso não exista:
   - utiliza um modelo de Machine Learning
   - estima se a informação é verdadeira ou falsa
   - armazena a informação no dataset local

---

# Objetivo do Projeto

Desenvolver um sistema capaz de classificar notícias e afirmações relacionadas ao contexto eleitoral brasileiro como:

- Verdadeiras
- Falsas

---

# Arquitetura da Solução

## Frontend

Interface responsável por:

- receber perguntas do usuário
- exibir resultados da análise
- permitir interação com o sistema

Tecnologias utilizadas:

- HTML
- CSS
- JavaScript
- Progressive Web App (PWA)

---

## Backend

Responsável por:

- receber requisições da interface
- consultar APIs externas
- executar o modelo de Machine Learning
- gerenciar o dataset

Tecnologias utilizadas:

- Python
- Flask

---

## Machine Learning

O sistema utiliza técnicas de Processamento de Linguagem Natural para classificação textual.

Tecnologias utilizadas:

- Scikit-learn
- TF-IDF
- Logistic Regression

---

# Estrutura do Projeto

```bash
election-fact-checker/
│
├── back-end/
│   ├── app.py
│   ├── train_model.py
│   ├── predict.py
│   ├── requirements.txt
│   │
│   ├── model/
│   │   ├── modelo_fake_news.pkl
│   │   └── vectorizer.pkl
│   │
│   └── services/
│       ├── fact_check_service.py
│       └── ml_service.py
│
├── dataset/
│   ├── raw_data/
│   ├── dataset_final.csv
│   ├── dataset_final_limpo.csv
│   ├── gerar_dataset.py
│   ├── limpar_dataset.py
│   └── unificar_dataset.py
│
├── front-end/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   ├── manifest.json
│   └── service-worker.js
│
└── README.md
```

---

# Como Executar o Projeto

## 1. Clonar o repositório

```bash
git clone https://github.com/ericaaraujoj/election-fact-checker.git
```

---

## 2. Instalar dependências

Entrar na pasta do backend:

```bash
cd back-end
```

Instalar as dependências:

```bash
pip install -r requirements.txt
```

---

## 3. Gerar dataset inicial

Entrar na pasta dataset:

```bash
cd ../dataset
```

Executar:

```bash
python gerar_dataset.py
```

---

## 4. Limpar dataset

```bash
python limpar_dataset.py
```

---

## 5. Treinar modelo

Entrar novamente na pasta backend:

```bash
cd ../back-end
```

Executar:

```bash
python train_model.py
```

---

## 6. Executar backend

```bash
python app.py
```

O servidor será iniciado em:

```bash
http://localhost:5000
```

---

## 7. Executar frontend

Abrir o arquivo:

```bash
front-end/index.html
```

---

# Observação Importante

O sistema desenvolvido possui caráter acadêmico e experimental.

A classificação realizada pelo modelo de Machine Learning não garante a veracidade absoluta das informações, sendo apenas uma ferramenta de apoio à análise.