from factcheckexplorer.factcheckexplorer import FactCheckLib

queries = [
    'eleição',
    'bolsonaro',
    'lula',
    'pt',
    'campanha',
    'urna',
    'voto',
    'fraude',
    'urna eletrônica',
    'TSE',
    'fraude eleitoral'
]

for q in queries:

    print(f'Buscando: {q}')

    fact_check = FactCheckLib(
        query=q,
        language='pt',
        num_results=200,
        csv_filename=f'dados_brutos/{q}.csv'
    )

    fact_check.process()

print('Finalizado!')