// Captura elementos do frontend
const btn = document.getElementById("btnVerificar");
const resultado = document.getElementById("resultado");
const listaHistorico = document.getElementById("historico");

// Simula um dataset local (temporário)
// FUTURO: será substituído por armazenamento real (banco de dados)
let historico = [];

// Evento de clique no botão
btn.addEventListener("click", () => {

  // Captura texto digitado pelo usuário
  const texto = document.getElementById("inputText").value.toLowerCase();

  // Validação: impede envio vazio
  if (!texto) {
    mostrarResultado("Digite uma dúvida.", "alerta");
    return;
  }

  // Simula tempo de processamento (API / IA)
  mostrarResultado("🔎 Analisando...", "alerta");

  setTimeout(() => {

    // será substituída por uma chamada ao backend (API em Python)
    const analise = analisarTexto(texto);

    // Exibe resultado na tela
    mostrarResultado(analise.mensagem, analise.tipo);

    // Salva no histórico (simulando dataset)
    // FUTURO: será salvo no backend/database
    salvarHistorico(texto, analise.mensagem);

  }, 1500);
});


// FUNÇÃO PRINCIPAL DE ANÁLISE (ATUALMENTE SIMULADA)
function analisarTexto(texto) {

  // SIMULAÇÃO ATUAL (TEMPORÁRIA)
  // Usa palavras-chave para decidir resultado
  const palavrasChave = ["urna", "fraude", "voto", "eleição","bolsonaro", "lula", "pt", "campanha"];

  // Verifica se alguma palavra está presente
  const encontrou = palavrasChave.some(p => texto.includes(p));

  // CASO 1 — Encontrou (simulação de fact-check)
  if (encontrou) {
    return {
      mensagem: "✔ Informação encontrada.",
      tipo: "sucesso"
    };
  }

  // CASO 2 — Não encontrou (simulação de IA)
  return {
    mensagem: "⚠ Nenhum registro encontrado. Classificação por IA: POSSÍVEL DESINFORMAÇÃO.",
    tipo: "alerta"
  };
}

// Função responsável por mostrar resultado na tela
function mostrarResultado(mensagem, tipo) {
  resultado.classList.remove("hidden", "sucesso", "alerta");
  resultado.classList.add(tipo);
  resultado.innerText = mensagem;
}


// Simula armazenamento de dados (dataset local)
function salvarHistorico(texto, resultadoTexto) {

  // Armazena no array
  historico.push({ texto, resultado: resultadoTexto });

  // Exibe na tela (histórico visual)
  const item = document.createElement("li");
  item.textContent = `${texto} → ${resultadoTexto}`;

  listaHistorico.appendChild(item);
}

// Registro do Service Worker (PWA)
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("service-worker.js");
}