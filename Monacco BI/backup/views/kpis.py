import streamlit as st
from utils.formatters import formatar_moeda

def render(metricas):
    st.subheader("Finanças Corporativas & Indicadores de Performance (KPIs)")
    st.markdown("Métricas essenciais para avaliar o modelo de negócio e a escalabilidade.")
    
    receitas = metricas.get('receitas', 0)
    
    if receitas > 0:
        mg_contrib = (metricas.get('dre_margem_contribuicao', 0) / receitas) * 100
        
        # Ponto de Equilíbrio (Break-even Point)
        if mg_contrib > 0:
            break_even = metricas.get('dre_despesas_fixas', 0) / (mg_contrib / 100)
            alcançado = "✅ Ultrapassado" if receitas >= break_even else "⚠️ Não Atingido"
        else:
            break_even = 0
            alcançado = "Inválido (Margem Negativa)"
            
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""
            <div class='kpi-box'>
                <div class='kpi-title'>Margem de Contribuição</div>
                <div class='kpi-value'>{mg_contrib:.1f}%</div>
                <div class='kpi-desc'>Representa o que sobra das vendas após pagar custos e impostos diretos.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
            <div class='kpi-box'>
                <div class='kpi-title'>Ponto de Equilíbrio (Break-Even)</div>
                <div class='kpi-value'>{formatar_moeda(break_even)}</div>
                <div class='kpi-desc'>Valor exato que precisa faturar para cobrir todos os custos. ({alcançado})</div>
            </div>
            """, unsafe_allow_html=True)
            
        with c3:
            resultado = metricas.get('dre_resultado', 0)
            gao = (metricas.get('dre_margem_contribuicao', 0) / resultado) if resultado > 0 else 0
            st.markdown(f"""
            <div class='kpi-box'>
                <div class='kpi-title'>Alavancagem Operacional (GAO)</div>
                <div class='kpi-value'>{gao:.2f}x</div>
                <div class='kpi-desc'>Indica que um aumento de 10% nas vendas gera {gao*10:.1f}% de aumento no lucro.</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ O arquivo importado não contém receitas (entradas) no período filtrado. Indicadores corporativos exigem faturamento.")