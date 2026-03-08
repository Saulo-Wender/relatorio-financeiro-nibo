import streamlit as st

def render(df):
    st.subheader("Explorador de Movimentos Financeiros")
    st.markdown("Faça um *Drill-down* para auditar as transações detalhadas.")
    
    if df is None or df.empty:
        st.warning("Não há transações para explorar.")
        return

    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        tipo_detalhe = st.radio("1. Direção do Fluxo:", ["Receita (Entradas)", "Despesa (Saídas)"], horizontal=True)
        tipo_real = "Receita" if "Receita" in tipo_detalhe else "Despesa"
        df_filtrado_tipo = df[df['Tipo'] == tipo_real]
        
    with col_filtro2:
        if not df_filtrado_tipo.empty:
            cat_disp = sorted(df_filtrado_tipo['Categoria'].unique().tolist())
            cat_detalhe = st.selectbox("2. Filtrar Categoria:", ["Todas as Categorias"] + cat_disp)
        else:
            cat_detalhe = "Todas as Categorias"
            st.selectbox("2. Filtrar Categoria:", ["Sem dados disponíveis"])

    if not df_filtrado_tipo.empty:
        df_final_detalhe = df_filtrado_tipo[df_filtrado_tipo['Categoria'] == cat_detalhe] if cat_detalhe != "Todas as Categorias" else df_filtrado_tipo
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Copia para não afetar o DataFrame original e formata a data visualmente
        df_display = df_final_detalhe[['Data', 'Pessoa', 'Descrição', 'Valor', 'Status']].copy()
        df_display['Data'] = df_display['Data'].dt.strftime('%d/%m/%Y')
        
        st.dataframe(
            df_display.sort_values('Valor', ascending=False).style.format({'Valor': 'R$ {:,.2f}'}),
            use_container_width=True, hide_index=True, height=350
        )
    else:
        st.warning(f"Sem movimentos de {tipo_real} registrados.")