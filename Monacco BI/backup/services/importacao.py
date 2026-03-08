import pandas as pd
import numpy as np
import streamlit as st
from services.tratamento import gerar_dados_teste

def ler_e_padronizar(arquivo_upload, natureza_conta: str) -> pd.DataFrame:
    """Lê o arquivo individual e força a natureza da conta (Receita ou Despesa)."""
    try:
        if arquivo_upload.name.upper().endswith('.CSV'):
            try:
                df_bruto = pd.read_csv(arquivo_upload, sep=';', decimal=',', encoding='utf-8')
            except UnicodeDecodeError:
                arquivo_upload.seek(0)
                df_bruto = pd.read_csv(arquivo_upload, sep=';', decimal=',', encoding='latin1')
        else:
            df_bruto = pd.read_excel(arquivo_upload)
        
        df = pd.DataFrame()
        
        # Tenta extrair a data padrão (Nibo usa 'Data de pagamento' ou 'Vencimento')
        col_data = 'Data de pagamento' if 'Data de pagamento' in df_bruto.columns else 'Vencimento'
        if col_data in df_bruto.columns:
            df['Data'] = pd.to_datetime(df_bruto[col_data], format='%d/%m/%Y', errors='coerce')
        else:
            # Fallback se não achar a coluna de data padrão
            df['Data'] = pd.NaT
            
        # Extração de valores (Garante que tudo fique positivo absoluto, pois a natureza define a entrada/saída)
        col_valor = 'Valor categoria/centro de custo' if 'Valor categoria/centro de custo' in df_bruto.columns else 'Valor'
        if col_valor in df_bruto.columns:
            valores = pd.to_numeric(df_bruto[col_valor].astype(str).str.replace(',', '.'), errors='coerce').fillna(0)
            df['Valor'] = valores.abs()
        else:
            df['Valor'] = 0.0

        # Preenchimento do restante da estrutura Monacco
        df['Tipo'] = natureza_conta
        df['Categoria'] = df_bruto.get('Categoria', 'Diversos').fillna('Sem Categoria')
        df['Descrição'] = df_bruto.get('Descrição', '').fillna('-')
        df['Pessoa'] = df_bruto.get('Nome', 'Não informado').fillna('Não informado')
        df['Status'] = np.where(df_bruto.get(col_data).notna(), 'Pago/Recebido', 'Pendente')
        df['Empresa'] = 'Dados Importados (Nibo)'

        return df
    except Exception as e:
        st.sidebar.error(f"Erro ao processar {arquivo_upload.name}: {e}")
        return pd.DataFrame()

def processar_arquivos_duplos(arq_receitas, arq_despesas):
    """Gerencia o upload duplo. Se ambos faltarem, gera dados de teste."""
    
    if arq_receitas is None and arq_despesas is None:
        return gerar_dados_teste(), False

    frames = []
    
    if arq_receitas is not None:
        df_rec = ler_e_padronizar(arq_receitas, "Receita")
        if not df_rec.empty:
            frames.append(df_rec)
            
    if arq_despesas is not None:
        df_desp = ler_e_padronizar(arq_despesas, "Despesa")
        if not df_desp.empty:
            frames.append(df_desp)
            
    if frames:
        df_consolidado = pd.concat(frames, ignore_index=True)
        st.sidebar.success("✅ Bases consolidadas com sucesso.")
        return df_consolidado, True
    else:
        st.sidebar.warning("⚠️ Os arquivos foram enviados, mas não puderam ser lidos. Usando dados de demonstração.")
        return gerar_dados_teste(), False