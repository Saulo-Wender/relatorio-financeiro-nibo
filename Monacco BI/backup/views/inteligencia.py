import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render(df):
    layout_padrao = dict(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Helvetica Neue", color="#334155"),
        margin=dict(t=30, b=0, l=0, r=0)
    )

    st.subheader("Inteligência de Fornecedores e Clientes")
    st.markdown("Identificação de concentrações e ofensores (Princípio de Pareto - Curva ABC).")
    
    col_av1, col_av2 = st.columns(2)
    
    with col_av1:
        st.markdown("<h4 style='color: #0F172A;'>Curva ABC - Fornecedores (Saídas)</h4>", unsafe_allow_html=True)
        df_desp = df[df['Tipo'] == 'Despesa']
        
        if not df_desp.empty:
            # Agrupamento e cálculo do acumulado
            df_forn = df_desp.groupby('Pessoa')['Valor'].sum().reset_index().sort_values('Valor', ascending=False)
            df_forn['% Acumulado'] = (df_forn['Valor'].cumsum() / df_forn['Valor'].sum()) * 100
            
            # Pegando os Top 10 para o gráfico não ficar ilegível
            df_forn_top = df_forn.head(10)
            
            fig_forn = go.Figure()
            fig_forn.add_trace(go.Bar(
                x=df_forn_top['Pessoa'], y=df_forn_top['Valor'],
                name='Valor Gasto', marker_color='#E11D48',
                text=df_forn_top['Valor'].apply(lambda x: f"R$ {x:,.0f}".replace(',','.')), textposition='auto'
            ))
            fig_forn.add_trace(go.Scatter(
                x=df_forn_top['Pessoa'], y=df_forn_top['% Acumulado'],
                name='% Acumulado', yaxis='y2', mode='lines+markers',
                marker=dict(color='#0F172A', size=8), line=dict(width=3)
            ))
            
            fig_forn.update_layout(
                **layout_padrao,
                yaxis=dict(title="Volume (R$)", showgrid=False),
                yaxis2=dict(title="% Acumulado", overlaying='y', side='right', range=[0, 110], showgrid=False),
                showlegend=False
            )
            st.plotly_chart(fig_forn, use_container_width=True)
        else:
             st.info("Sem dados de despesas processados para esta análise.")

    with col_av2:
        st.markdown("<h4 style='color: #0F172A;'>Curva ABC - Clientes (Entradas)</h4>", unsafe_allow_html=True)
        df_rec = df[df['Tipo'] == 'Receita']
        
        if not df_rec.empty:
            df_cli = df_rec.groupby('Pessoa')['Valor'].sum().reset_index().sort_values('Valor', ascending=False)
            df_cli['% Acumulado'] = (df_cli['Valor'].cumsum() / df_cli['Valor'].sum()) * 100
            
            df_cli_top = df_cli.head(10)
            
            fig_cli = go.Figure()
            fig_cli.add_trace(go.Bar(
                x=df_cli_top['Pessoa'], y=df_cli_top['Valor'],
                name='Faturamento', marker_color='#059669',
                text=df_cli_top['Valor'].apply(lambda x: f"R$ {x:,.0f}".replace(',','.')), textposition='auto'
            ))
            fig_cli.add_trace(go.Scatter(
                x=df_cli_top['Pessoa'], y=df_cli_top['% Acumulado'],
                name='% Acumulado', yaxis='y2', mode='lines+markers',
                marker=dict(color='#0F172A', size=8), line=dict(width=3)
            ))
            
            fig_cli.update_layout(
                **layout_padrao,
                yaxis=dict(title="Volume (R$)", showgrid=False),
                yaxis2=dict(title="% Acumulado", overlaying='y', side='right', range=[0, 110], showgrid=False),
                showlegend=False
            )
            st.plotly_chart(fig_cli, use_container_width=True)
        else:
             st.info("Sem dados de faturamento para análise de clientes.")