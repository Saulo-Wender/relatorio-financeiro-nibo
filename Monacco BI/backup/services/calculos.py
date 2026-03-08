import pandas as pd

def calcular_metricas_dre(df: pd.DataFrame, cat_impostos: list, cat_custos: list) -> dict:
    """
    Processa todos os cálculos financeiros com base no DataFrame e nas categorias.
    Retorna um dicionário com os valores prontos para exibição.
    """
    # Proteção caso o DataFrame chegue vazio
    if df is None or df.empty:
        return {k: 0 for k in ["receitas", "despesas", "saldo", "margem", "dre_impostos", "dre_custos", "dre_receita_liquida", "dre_margem_contribuicao", "dre_despesas_fixas", "dre_resultado"]}

    # Os tipos 'Receita' e 'Despesa' já foram forçados e garantidos no importacao.py
    receitas = df[df['Tipo'] == 'Receita']['Valor'].sum()
    despesas = df[df['Tipo'] == 'Despesa']['Valor'].sum()
    saldo = receitas - despesas
    margem = (saldo / receitas * 100) if receitas > 0 else 0

    # Estruturação da DRE
    dre_impostos = df[(df['Categoria'].isin(cat_impostos)) & (df['Tipo'] == 'Despesa')]['Valor'].sum()
    dre_custos = df[(df['Categoria'].isin(cat_custos)) & (df['Tipo'] == 'Despesa')]['Valor'].sum()

    dre_receita_liquida = receitas - dre_impostos
    dre_margem_contribuicao = dre_receita_liquida - dre_custos

    # Despesas Fixas é tudo aquilo que é despesa e não foi mapeado como imposto ou custo variável
    dre_despesas_fixas = despesas - dre_impostos - dre_custos
    dre_resultado = dre_margem_contribuicao - dre_despesas_fixas

    return {
        "receitas": receitas,
        "despesas": despesas,
        "saldo": saldo,
        "margem": margem,
        "dre_impostos": dre_impostos,
        "dre_custos": dre_custos,
        "dre_receita_liquida": dre_receita_liquida,
        "dre_margem_contribuicao": dre_margem_contribuicao,
        "dre_despesas_fixas": dre_despesas_fixas,
        "dre_resultado": dre_resultado
    }