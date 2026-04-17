from factcheckexplorer.factcheckexplorer import FactCheckLib

queries = ["eleição", "bolsonaro", "lula", "pt", "campanha", "urna", "voto", "fraude"]

for q in queries:
    print(f"🔎 Buscando: {q}")

    fact_check = FactCheckLib(
        query=q,
        language=None, 
        num_results=50
    )

    fact_check.process()

print("Finalizado!")