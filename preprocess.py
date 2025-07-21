# preprocess.py
import json
import pandas as pd

def carregar_e_salvar_dados(vagas_path, prospects_path, applicants_path):
    """
    Lê os arquivos JSON originais, processa-os em DataFrames limpos
    e os salva no formato Parquet para uso eficiente pela API.
    Este script é o nosso passo de "treinamento" ou "salvamento do modelo".
    """
    print("Iniciando pré-processamento dos dados...")

    def carregar_json(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar {filepath}: {e}")
            return None

    # Carregar todos os dados
    dados_vagas = carregar_json("content/vagas.json")
    dados_prospects = carregar_json("content/prospects.json")
    dados_applicants = carregar_json("content/applicants.json")

    if not all([dados_vagas, dados_prospects, dados_applicants]):
        print("Processamento falhou: um ou mais arquivos JSON não foram encontrados ou estão vazios.")
        return

    # Processar Vagas
    vagas_list = [ {'id_vaga': id_vaga, **detalhes.get('informacoes_basicas', {}), **detalhes.get('perfil_vaga', {})} for id_vaga, detalhes in dados_vagas.items() ]
    df_vagas = pd.DataFrame(vagas_list)
    
    # Processar Prospects
    prospects_list = [ {'id_vaga': id_vaga, **prospect} for id_vaga, detalhes in dados_prospects.items() for prospect in detalhes.get('prospects', []) ]
    df_prospects = pd.DataFrame(prospects_list)
    df_prospects['codigo'] = df_prospects['codigo'].astype(str)

    # Processar Applicants
    applicants_list = []
    for id_candidato, informacoes in dados_applicants.items():
        registro = {'id_candidato': str(id_candidato)}
        for secao, valores in informacoes.items():
            if isinstance(valores, dict): registro.update(valores)
            else: registro[secao] = valores
        applicants_list.append(registro)
    df_applicants = pd.DataFrame(applicants_list)
    
    # Salvar os DataFrames processados como arquivos Parquet
    df_vagas.to_parquet('vagas.parquet')
    df_prospects.to_parquet('prospects.parquet')
    df_applicants.to_parquet('applicants.parquet')

    print("\nDados pré-processados e salvos com sucesso como:")
    print("- vagas.parquet")
    print("- prospects.parquet")
    print("- applicants.parquet")

if __name__ == "__main__":
    carregar_e_salvar_dados(
        vagas_path='/content/vagas.json',
        prospects_path='/content/prospects.json',
        applicants_path='/content/applicants.json'
    )