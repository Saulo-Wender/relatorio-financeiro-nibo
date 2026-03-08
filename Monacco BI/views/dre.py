import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.formatters import formatar_moeda

def render(df, metricas):
    st.subheader("Demonstração do Resultado do Exercício (Visão Monacco)")
    st.markdown("Acompanhamento contábil-gerencial estruturado. Configure os grupos de contas no painel lateral.")
    
    # Montagem da estrutura de dados da DRE
    linhas_dre = [
        {"Estrutura": "1. RECEITA OPERACIONAL BRUTA", "Valor": metricas.get('receitas', 0), "Bg": "#F8FAFC", "Color": "#1E3A8A", "Bold": True},
        {"Estrutura": "(-) Deduções e Impostos", "Valor": -metricas.get('dre_impostos', 0), "Bg": "#FFFFFF", "Color": "#E11D48", "Bold": False},
        {"Estrutura": "2. RECEITA OPERACIONAL LÍQUIDA", "Valor": metricas.get('dre_receita_liquida', 0), "Bg": "#F1F5F9", "Color": "#059669", "Bold": True},
        {"Estrutura": "(-) Custos Variáveis / Insumos", "Valor": -metricas.get('dre_custos', 0), "Bg": "#FFFFFF", "Color": "#E11D48", "Bold": False},
        {"Estrutura": "3. MARGEM DE CONTRIBUIÇÃO", "Valor": metricas.get('dre_margem_contribuicao', 0), "Bg": "#EFF6FF", "Color": "#2563EB", "Bold": True},
        {"Estrutura": "(-) Despesas Fixas Operacionais", "Valor": -metricas.get('dre_despesas_fixas', 0), "Bg": "#FFFFFF", "Color": "#E11D48", "Bold": False},
        {"Estrutura": "4. RESULTADO OPERACIONAL (EBITDA)", "Valor": metricas.get('dre_resultado', 0), "Bg": "#0F172A" if metricas.get('dre_resultado', 0) >= 0 else "#9F1239", "Color": "white", "Bold": True}
    ]
    
    # Processamento para o Gráfico de Tabela do Plotly
    col_estrutura, col_valor, col_av, cor_fundo, cor_texto = [], [], [], [], []
    receitas_totais = metricas.get('receitas', 0)
    
    for row in linhas_dre:
        av = ((abs(row['Valor']) / receitas_totais) * 100) if receitas_totais > 0 else 0
        texto_str = f"<b>{row['Estrutura']}</b>" if row['Bold'] else row['Estrutura']
        val_str = f"<b>{formatar_moeda(row['Valor']).replace('R$ -', '- R$ ')}</b>" if row['Bold'] else formatar_moeda(row['Valor']).replace('R$ -', '- R$ ')
        av_str = f"<b>{av:.1f}%</b>" if row['Bold'] else f"{av:.1f}%"
        
        col_estrutura.append(texto_str)
        col_valor.append(val_str)
        col_av.append(av_str)
        cor_fundo.append(row['Bg'])
        cor_texto.append(row['Color'])
    
    # Geração da Tabela Indestrutível
    fig_dre_table = go.Figure(data=[go.Table(
        columnwidth=[50, 25, 25],
        header=dict(
            values=['<b>Descrição da Rubrica</b>', '<b>Valor (R$)</b>', '<b>Análise Vertical (%)</b>'],
            fill_color='#1E3A8A', align=['left', 'right', 'right'], 
            font=dict(color='white', size=14), height=40
        ),
        cells=dict(
            values=[col_estrutura, col_valor, col_av],
            fill_color=[cor_fundo]*3, align=['left', 'right', 'right'],
            font=dict(color=[cor_texto]*3, size=14), height=35
        )
    )])
    
    fig_dre_table.update_layout(margin=dict(l=0, r=0, t=10, b=10), height=350)
    st.plotly_chart(fig_dre_table, use_container_width=True)
    
    # Salva no session_state para a aba de exportação conseguir acessar depois
    df_dre_export = pd.DataFrame(linhas_dre)[['Estrutura', 'Valor']]
    df_dre_export['Análise Vertical (%)'] = df_dre_export['Valor'].apply(lambda x: f"{((abs(x) / receitas_totais) * 100):.1f}%" if receitas_totais > 0 else "0.0%")
    st.session_state['dre_export'] = df_dre_export