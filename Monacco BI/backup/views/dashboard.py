import streamlit as st
import plotly.express as px
import pandas as pd
from utils.formatters import formatar_moeda

def render(df, metricas):
    # ATUALIZAÇÃO: Layout do Plotly adaptado para o Dark Mode
    layout_padrao = dict(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Helvetica Neue", color="#E2E8F0"), # Fonte clara
        title_font=dict(size=18, color="#C5A059", family="Helvetica Neue"), # Título dourado
        hoverlabel=dict(bgcolor="#1E293B", font_size=14, font_family="Helvetica Neue", font_color="#E2E8F0")
    )
    # Paleta de cores mais vibrante para contrastar no escuro
    plotly_colors = ['#C5A059', '#34D399', '#F87171', '#60A5FA', '#A78BFA', '#38BDF8']

    data_inicio_str = metricas.get('data_inicio').strftime('%d/%m/%Y') if metricas.get('data_inicio') else "N/A"
    data_fim_str = metricas.get('data_fim').strftime('%d/%m/%Y') if metricas.get('data_fim') else "N/A"

    st.markdown(f"### Visão Geral da Operação | <span style='color: #94A3B8; font-size: 0.8em;'>{data_inicio_str} a {data_fim_str}</span>", unsafe_allow_html=True)
    
    # Cards Superiores
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Faturamento Bruto", formatar_moeda(metricas.get('receitas', 0)), delta="Entradas")
    col2.metric("Custos e Despesas", formatar_moeda(metricas.get('despesas', 0)), delta="-Saídas", delta_color="inverse")
    
    if metricas.get('receitas', 0) == 0:
        col3.metric("Consumo de Caixa (Burn)", formatar_moeda(metricas.get('despesas', 0)), delta="Sem Receitas", delta_color="inverse")
        col4.metric("Margem EBITDA", "N/A", delta="Requer receita")
    else:
        saldo = metricas.get('saldo', 0)
        col3.metric("Fluxo de Caixa Livre", formatar_moeda(saldo), delta=f"{'Superávite' if saldo > 0 else 'Défice'}")
        margem_ebitda = (metricas.get('dre_resultado', 0) / metricas.get('receitas', 1)) * 100
        col4.metric("Margem EBITDA", f"{margem_ebitda:.1f}%", delta="Saudável" if margem_ebitda > 15 else "Atenção", delta_color="normal" if margem_ebitda > 15 else "inverse")

    st.markdown("<br>", unsafe_allow_html=True)
    col_graf1, col_graf2 = st.columns([6, 4])
    
    # Gráfico de Área (Evolução Diária)
    with col_graf1:
        if not df.empty:
            df_diario = df.groupby(['Data', 'Tipo'])['Valor'].sum().reset_index()
            fig_area = px.area(
                df_diario, x='Data', y='Valor', color='Tipo', 
                color_discrete_map={'Receita': 'rgba(52, 211, 153, 0.7)', 'Despesa': 'rgba(248, 113, 113, 0.7)'}, # Verde e Vermelho mais brilhantes
                title="Evolução Diária do Fluxo Financeiro"
            )
            fig_area.update_layout(**layout_padrao, yaxis_title="Reais (R$)", xaxis_title="", legend_title="")
            fig_area.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(148, 163, 184, 0.2)')
            fig_area.update_layout(margin=dict(t=50, b=10, l=10, r=10))
            st.plotly_chart(fig_area, use_container_width=True)

    # Gráfico de Rosca (Composição de Saídas)
    with col_graf2:
        df_despesas = df[df['Tipo'] == 'Despesa']
        if not df_despesas.empty:
            df_cat_despesas = df_despesas.groupby('Categoria')['Valor'].sum().reset_index().sort_values('Valor', ascending=False)
            
            if len(df_cat_despesas) > 5:
                top5 = df_cat_despesas.head(5)
                valor_outras = df_cat_despesas.iloc[5:]['Valor'].sum()
                outros = pd.DataFrame([{'Categoria': 'Outras', 'Valor': valor_outras}])
                df_cat_despesas = pd.concat([top5, outros], ignore_index=True)
                
            fig_rosca = px.pie(
                df_cat_despesas, values='Valor', names='Categoria', hole=0.6,
                color_discrete_sequence=plotly_colors, title="Composição de Saídas"
            )
            fig_rosca.update_traces(textposition='inside', textinfo='percent')
            fig_rosca.update_layout(
                **layout_padrao, 
                showlegend=True, 
                legend=dict(orientation="h", y=-0.2),
                margin=dict(t=50, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_rosca, use_container_width=True)