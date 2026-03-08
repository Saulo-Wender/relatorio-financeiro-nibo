import streamlit as st
import plotly.graph_objects as go
from utils.formatters import formatar_moeda

def render(metricas):
    layout_padrao = dict(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(family="Helvetica Neue", color="#334155")
    )

    st.markdown("""
    <div class="board-container">
        <div class="board-title">Comitê Executivo de Resultados</div>
        <div class="board-subtitle">Síntese de Performance Operacional e Financeira</div>
    """, unsafe_allow_html=True)
    
    b_col1, b_col2, b_col3 = st.columns(3)
    
    with b_col1:
        st.markdown(f"""
        <div class="board-metric-box">
            <div class="board-label">Faturamento</div>
            <div class="board-value board-value-fat">{formatar_moeda(metricas.get('receitas', 0))}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with b_col2:
        st.markdown(f"""
        <div class="board-metric-box">
            <div class="board-label">Gastos Globais</div>
            <div class="board-value board-value-neg">-{formatar_moeda(metricas.get('despesas', 0))}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with b_col3:
        saldo = metricas.get('saldo', 0)
        cor_classe = "board-value-pos" if saldo >= 0 else "board-value-neg"
        sinal = "+" if saldo >= 0 else ""
        st.markdown(f"""
        <div class="board-metric-box">
            <div class="board-label">Caixa Gerado</div>
            <div class="board-value {cor_classe}">{sinal}{formatar_moeda(saldo)}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)

    col_gauge, col_water = st.columns([3, 7])
    
    with col_gauge:
        st.markdown("<h4 style='text-align: center; color: #0F172A;'>Saúde Financeira</h4>", unsafe_allow_html=True)
        if metricas.get('receitas', 0) > 0:
            marg_ebitda = (metricas.get('dre_resultado', 0) / metricas.get('receitas', 1)) * 100
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = marg_ebitda,
                number = {'suffix': "%"},
                title = {'text': "Margem EBITDA", 'font': {'size': 18}},
                gauge = {
                    'axis': {'range': [-20, 50]},
                    'bar': {'color': "#1E3A8A"},
                    'steps': [
                        {'range': [-20, 0], 'color': "#FEE2E2"},
                        {'range': [0, 15], 'color': "#FEF3C7"},
                        {'range': [15, 50], 'color': "#D1FAE5"}],
                    'threshold': {'line': {'color': "#E11D48", 'width': 4}, 'thickness': 0.75, 'value': 15}
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(t=40, b=0, l=10, r=10))
            st.plotly_chart(fig_gauge, use_container_width=True)
            st.info("💡 A zona verde indica margens acima de 15% (Alvo).")
        else:
            st.warning("Sem faturamento para calcular margens de rentabilidade.")

    with col_water:
        receitas = metricas.get('receitas', 0)
        impostos_custos = metricas.get('dre_impostos', 0) + metricas.get('dre_custos', 0)
        fixas = metricas.get('dre_despesas_fixas', 0)
        resultado = metricas.get('dre_resultado', 0)

        fig_waterfall = go.Figure(go.Waterfall(
            name="Resultado", orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Faturamento Bruto", "Impostos/Custos Var.", "Despesas Fixas", "Resultado (EBITDA)"],
            textposition="outside",
            text=[formatar_moeda(receitas), f"-{formatar_moeda(impostos_custos)}", f"-{formatar_moeda(fixas)}", formatar_moeda(resultado)],
            y=[receitas, -impostos_custos, -fixas, resultado],
            connector={"line":{"color":"#94A3B8", "width": 2, "dash": "dot"}},
            decreasing={"marker":{"color":"#E11D48"}},
            increasing={"marker":{"color":"#059669"}},
            totals={"marker":{"color":"#1E3A8A"}}
        ))
        fig_waterfall.update_layout(**layout_padrao, title="Formação de Resultado Monetário", title_x=0.5, margin=dict(t=40, b=30))
        st.plotly_chart(fig_waterfall, use_container_width=True)