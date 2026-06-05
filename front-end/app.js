const button = document.getElementById('btnVerificar')

button.addEventListener('click', async () => {

    const texto = document.getElementById('inputText').value.trim();

    const resultadoDiv = document.getElementById('resultado');

    if (!texto) {
        resultadoDiv.classList.remove('hidden');
        resultadoDiv.innerHTML = `
            <div class="card">
                <h3>⚠️ Digite algo primeiro</h3>
                <p>Você precisa escrever uma informação antes de verificar.</p>
            </div>
        `;
        return;
    }

    resultadoDiv.classList.remove('hidden');
    resultadoDiv.innerHTML = `<p>🔎 Analisando informação...</p>`;

    try {
        const resposta = await fetch('http://localhost:5000/factcheck', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texto })
        });

        const dados = await resposta.json();

        console.log("RESPOSTA:", dados);


        if (dados.resultado && Array.isArray(dados.resultado)) {

            let cards = `

                <div class="total-resultados">
                    Mostrando os 2 resultados mais relevantes de ${dados.quantidade} encontrados.
                </div>

                <div class="descricao-resultados">
                    Verificações encontradas com base na sua pesquisa:
                </div>
            `

            dados.resultado.forEach(item => {

                let classeBadge = "falso";

                if (item.classificacao === "Verdadeiro") {
                    classeBadge = "verdadeiro";
                }
                else if (item.classificacao === "Parcialmente verdadeiro") {
                    classeBadge = "parcial";
                }

                cards += `
        <div class="card">

            <span class="badge ${classeBadge}">
                ${item.classificacao}
            </span>

            <h3>${item.afirmacao}</h3>

            <p>
                <strong>Fonte:</strong>
                ${item.fonte}
            </p>

            <p>
                <p class="titulo-noticia">
                    ${item.titulo || ""}
                </p>
            </p>

            <a href="${item.link}" target="_blank">
                Ler verificação completa
            </a>

        </div>
    `
            })

            cards += `

                <div class="ia-box">

                    <h3>🤖 Não encontrou exatamente o que procurava?</h3>

                    <p>
                        Utilize a Inteligência Artificial para realizar
                        uma análise estimada da afirmação enviada.
                    </p>

                    <button type="button" id="btnIA">
                         Analisar com IA
                    </button>

                </div>
            `

            resultadoDiv.innerHTML = cards

            document.getElementById('btnIA').addEventListener('click', async (event) => {

                event.preventDefault()

                const loading = document.createElement("p")

                loading.className = "loading-ia"

                loading.innerHTML = "🤖 IA analisando afirmação..."

                resultadoDiv.appendChild(loading)

                const respostaIA = await fetch('http://localhost:5000/ml', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ texto })
                })

                if (!respostaIA.ok) {
                    throw new Error("Erro ao consultar IA")
                }

                const dadosIA = await respostaIA.json()

                console.log(dadosIA)

                loading.remove()

                document.querySelector('.ia-box').style.display = 'none'

                resultadoDiv.innerHTML += `

                    <div class="card ia-card">

                        <span class="badge ia">
                            Inteligência Artificial
                        </span>

                        <h3>Resultado da IA</h3>

                        <p>
                            <strong>Classificação:</strong>
                            ${dadosIA.classificacao}
                        </p>

                        <p>
                            <strong>Confiança:</strong>
                            ${dadosIA.confianca}%
                        </p>

                        <div class="aviso-ia">

                        ⚠️ Esta análise é uma estimativa produzida por um modelo de Machine Learning treinado com verificações públicas. <br> O resultado não substitui a consulta a fontes jornalísticas e verificadores de fatos especializados.

                        </div>

                    </div>
                `
            })

        } else {

            resultadoDiv.innerHTML = `

                <div class="card ia-card">

                    <span class="badge ia">
                        Inteligência Artificial
                    </span>

                    <h3>Resultado da análise</h3>

                    <p>
                        ${dados.resultado}
                    </p>

                </div>
            `
        }

    } catch (erro) {

        resultadoDiv.innerHTML = `
            <div class="card">
                <h3>Erro</h3>
                <p>Não foi possível realizar a análise.</p>
            </div>
        `
    }
})