import os
import json
import pandas as pd
from tqdm import tqdm  # Importa a classe tqdm

# Pasta de entrada contendo os arquivos JSON
pasta_json = './v1'

# Pasta de saída onde os arquivos CSV serão armazenados
pasta_saida = './arquivoscsvCEPopencep'

# Certifique-se de que a pasta de saída existe
if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

# Dicionário para armazenar todos os dados por UF
dados_por_uf = {}

# Lista de arquivos JSON na pasta de entrada
arquivos_json = [arquivo for arquivo in os.listdir(pasta_json) if arquivo.endswith('.json')]

# Cria uma barra de progresso para acompanhar o loop
with tqdm(total=len(arquivos_json)) as progresso:
    for arquivo_json in arquivos_json:
        caminho_json = os.path.join(pasta_json, arquivo_json)

        # Abre o arquivo JSON
        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados_json = json.load(f)

        # Obtém a unidade federativa (UF) do JSON
        uf = dados_json['uf']

        # Adiciona os dados ao dicionário da UF correspondente
        if uf not in dados_por_uf:
            dados_por_uf[uf] = []
        dados_por_uf[uf].append(dados_json)

        # Atualiza a barra de progresso
        progresso.update(1)

# Loop pelas UFs e cria um único arquivo CSV para cada estado
for uf, dados_uf in dados_por_uf.items():
    # Define o nome do arquivo CSV com base na UF
    nome_arquivo_csv = f'{uf}_dados.csv'

    # Cria um DataFrame a partir de todos os dados da UF
    df = pd.DataFrame(dados_uf)

    # Salva o DataFrame como um arquivo CSV na pasta de saída
    caminho_saida_csv = os.path.join(pasta_saida, nome_arquivo_csv)
    df.to_csv(caminho_saida_csv, index=False)

print('Processo concluído.')
