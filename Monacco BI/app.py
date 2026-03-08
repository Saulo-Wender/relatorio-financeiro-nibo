import streamlit as st
from assets.styles import aplicar_estilos
from components.sidebar import render_sidebar
from services.calculos import calcular_metricas_dre

# Importação atualizada para a pasta 'views'
from views import dashboard, boardroom, kpis, dre, inteligencia, explorador

# 1. Configuração Inicial da Página
st.set_page_config(
    page_title="Monacco BI | Executive Finance",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # 2. Injeção do CSS Customizado
    aplicar_estilos()

    # 3. Cabeçalho Principal
    col_logo, col_title = st.columns([1, 8])
    with col_title:
        st.markdown("<h1>Monacco BI <span style='color: #64748B; font-weight: 300;'>| Executive Finance</span></h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748B; font-size: 18px;'>Plataforma de Inteligência Analítica para Gestão de Resultados</p>", unsafe_allow_html=True)

    # 4. Renderização da Sidebar (Agora processando duplo upload)
    df, cat_impostos, cat_custos, empresa_selecionada, data_inicio, data_fim = render_sidebar()

    if df is None or df.empty:
        st.warning("⚠️ Não há dados disponíveis para os filtros selecionados. Ajuste os parâmetros na barra lateral ou faça o upload dos arquivos.")
        st.stop()

    # 5. Processamento Global (O Motor Financeiro)
    metricas = calcular_metricas_dre(df, cat_impostos, cat_custos)

    # Adicionando o contexto de filtros ao dicionário para uso nas views
    metricas['data_inicio'] = data_inicio
    metricas['data_fim'] = data_fim
    metricas['empresa'] = empresa_selecionada

    # 6. Estrutura de Navegação em Abas Centrais
    tab_dash, tab_board, tab_kpi, tab_dre, tab_intel, tab_explorador, tab_export = st.tabs([
        "📈 Dashboard Principal", 
        "🖥️ Boardroom", 
        "📊 Finanças Corporativas",
        "📑 DRE Estruturada", 
        "🔍 Inteligência ABC", 
        "🔎 Explorador",
        "📤 Central de Exportação"
    ])

    # 7. Renderização das Views (Injetando os dados processados)
    with tab_dash:
        dashboard.render(df, metricas)
        
    with tab_board:
        boardroom.render(metricas)
        
    with tab_kpi:
        kpis.render(metricas)
        
    with tab_dre:
        dre.render(df, metricas)
        
    with tab_intel:
        inteligencia.render(df)
        
    with tab_explorador:
        explorador.render(df)
        
    with tab_export:
        from utils.exportacao import convert_df_to_csv
        
        st.subheader("Central de Descargas")
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.markdown("#### 1. DRE Gerencial")
            if 'dre_export' in st.session_state:
                csv_dre = convert_df_to_csv(st.session_state['dre_export'])
                st.download_button("📥 Baixar DRE (.csv)", data=csv_dre, file_name=f"DRE_Monacco_{empresa_selecionada}.csv", mime='text/csv')
                
        with col_exp2:
            st.markdown("#### 2. Base Tratada Consolidada")
            csv_raw = convert_df_to_csv(df)
            st.download_button("📥 Baixar Transações (.csv)", data=csv_raw, file_name=f"Transacoes_Limpo_{empresa_selecionada}.csv", mime='text/csv')

if __name__ == "__main__":
    main()