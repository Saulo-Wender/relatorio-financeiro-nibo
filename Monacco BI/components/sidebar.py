import streamlit as st
import pandas as pd
from services.importacao import processar_arquivos_duplos

def render_sidebar():
    """Renderiza a barra lateral com uploads duplos e retorna os dados filtrados."""
    with st.sidebar:
        st.markdown("<h2 style='color: white !important; text-align: center;'>MONACCO</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Melhoria: Usando expanser para manter a sidebar limpa
        with st.expander("📥 Importação de Arquivos Nibo", expanded=True):
            st.markdown("<small>Contas Recebidas (Entradas)</small>", unsafe_allow_html=True)
            arq_receitas = st.file_uploader("", type=["xlsx", "xls", "csv"], key="upload_rec")
            
            st.markdown("<small>Contas Pagas (Saídas)</small>", unsafe_allow_html=True)
            arq_despesas = st.file_uploader("", type=["xlsx", "xls", "csv"], key="upload_desp")
        
        # Processa os arquivos em um único DataFrame consolidado
        df, is_real_data = processar_arquivos_duplos(arq_receitas, arq_despesas)

        st.markdown("---")
        st.header("⚙️ Filtros Executivos")
        
        empresas = df['Empresa'].unique().tolist()
        empresa_selecionada = st.selectbox("Unidade de Negócio:", ["Todas as Unidades"] + empresas)
        if empresa_selecionada != "Todas as Unidades":
            df = df[df['Empresa'] == empresa_selecionada]

        # Tratamento de Datas
        df = df.dropna(subset=['Data']) 
        if df.empty:
            return df, [], [], empresa_selecionada, None, None

        min_date = df['Data'].min().date()
        max_date = df['Data'].max().date()
        
        data_inicio, data_fim = st.date_input(
            "Horizonte de Análise:", 
            [min_date, max_date], 
            min_value=min_date, 
            max_value=max_date
        )
        
        # Filtros de Data e Status
        df = df[(df['Data'].dt.date >= data_inicio) & (df['Data'].dt.date <= data_fim)]
        status_selecionado = st.multiselect("Estado (Caixa):", df['Status'].unique(), default=['Pago/Recebido'])
        df = df[df['Status'].isin(status_selecionado)]

        # Configuração da DRE
        st.markdown("---")
        with st.expander("⚙️ Configuração da DRE Estruturada", expanded=False):
            todas_categorias = df['Categoria'].unique().tolist()
            
            cat_impostos_auto = [c for c in todas_categorias if any(x in c.lower() for x in ['imposto', 'simples', 'iss', 'irpj', 'csll', 'iva', 'das'])]
            cat_custos_auto = [c for c in todas_categorias if any(x in c.lower() for x in ['insumo', 'mercadoria', 'fornecedor', 'produto', 'deslocamento', 'comiss'])]
            
            cat_impostos = st.multiselect("Mapear Impostos/Deduções", todas_categorias, default=cat_impostos_auto)
            cat_custos = st.multiselect("Mapear Custos Variáveis", todas_categorias, default=cat_custos_auto)

    return df, cat_impostos, cat_custos, empresa_selecionada, data_inicio, data_fim
