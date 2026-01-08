import pandas as pd
import re
import os

def extrair_marcas_do_sql(caminho_sql):
    marcas_encontradas = {}
    # Regex para capturar os valores do SQL
    padrao = re.compile(r"VALUES\s*\(\s*\d+\s*,\s*N'([^']+)'\s*,\s*\d+\s*,\s*N'([^']+)'", re.IGNORECASE)

    print(f"Lendo arquivo SQL: {caminho_sql} ...")
    
    try:
        with open(caminho_sql, 'r', encoding='utf-8', errors='replace') as arquivo:
            for linha in arquivo:
                match = padrao.search(linha)
                if match:
                    tipo_veiculo = match.group(1) 
                    nome_marca = match.group(2)   
                    
                    chave = nome_marca.lower().strip()
                    
                    if chave not in marcas_encontradas:
                        marcas_encontradas[chave] = {
                            'original': nome_marca,
                            'tipo': tipo_veiculo
                        }
    except Exception as e:
        print(f"Erro ao ler SQL: {e}")
        return {}

    return marcas_encontradas

def identificar_novas_marcas(caminho_csv_antigo, caminho_novo_sql, nome_arquivo_saida):
    print("--- INICIANDO PROCESSAMENTO (ARQUIVO ÚNICO) ---")
    
    # 1. Carrega base antiga
    if not os.path.exists(caminho_csv_antigo):
        print(f"ERRO: {caminho_csv_antigo} não encontrado.")
        return

    try:
        df_existing = pd.read_csv(caminho_csv_antigo, sep=None, engine='python', encoding='latin1')
        existing_names = set(df_existing['name'].astype(str).str.lower().str.strip())
        maior_id_atual = df_existing['id_veiculo_marca'].max()
    except Exception as e:
        print(f"Erro ao ler CSV antigo: {e}")
        return

    # 2. Extrai dados do SQL
    if not os.path.exists(caminho_novo_sql):
        print(f"ERRO: {caminho_novo_sql} não encontrado.")
        return
        
    novas_do_sql = extrair_marcas_do_sql(caminho_novo_sql)
    
    # 3. Preparação
    type_mapping = {
        'carros': 0, 'motos': 1, 'caminhoes': 2, 'micro-onibus': 2 
    }
    
    lista_geral = []
    
    for chave, dados in novas_do_sql.items():
        if chave not in existing_names:
            tipo_num = type_mapping.get(dados['tipo'], 0)
            
            lista_geral.append({
                'name': dados['original'],
                'status': 1,
                'type': tipo_num
            })

    # 4. Salvamento (Arquivo Único Corrigido)
    if lista_geral:
        df_total = pd.DataFrame(lista_geral)
        
        # Gera IDs sequenciais
        df_total['id_veiculo_marca'] = range(maior_id_atual + 1, maior_id_atual + 1 + len(df_total))
        
        # Organiza colunas
        df_total = df_total[['id_veiculo_marca', 'name', 'status', 'type']]

        print(f"\nTotal de novas marcas encontradas: {len(df_total)}")
        print("-" * 40)

        # SALVA COM PONTO E VÍRGULA (sep=';')
        df_total.to_csv(nome_arquivo_saida, index=False, sep=';', encoding='utf-8-sig')
        
        print(f"SUCESSO! Arquivo gerado: {nome_arquivo_saida}")
        print("Agora as colunas devem aparecer separadas corretamente no Excel.")
        print("-" * 40)
        
    else:
        print("Nenhuma marca nova encontrada.")

# --- CONFIGURAÇÃO ---
arquivo_antigo = 'veiculo_marca.csv' #planilha extraida do BD
arquivo_novo_sql = 'fipe-02122025-MSSQL.sql' # planilha nova 
arquivo_saida = 'veiculo_marca.csv' # Resultado do tratamento de dados

if __name__ == "__main__":
    identificar_novas_marcas(arquivo_antigo, arquivo_novo_sql, arquivo_saida)