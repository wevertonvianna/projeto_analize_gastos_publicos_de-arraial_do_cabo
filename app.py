import streamlit as st

st.title("Análise de Gastos Públicos da prefeitura de Arraial do Cabo de 2025")
st.write("Este aplicativo permite analisar os gastos públicos da prefeitura de Arraial do Cabo.")
import pandas as pd
import matplotlib.pyplot as plt
import requests

@st.cache_data
def load_data():
    url = "https://transparencia.arraial.modernizacao.com.br/sincronia/apidados.rule?sys=LAI"

    payload = {
        "api": "despesas_todas",
        "ano": 2025
    }
    response = requests.post(url, json=payload)
    data = response.json()
    df = pd.DataFrame(data["dados"])
    return df


df = load_data()

df['valor_despesa']= df['valor_despesa'].astype(float)
df['Valor_Estornado'] =df['Valor_Estornado'].astype(float)
df['valor_despesa_total']= df['valor_despesa_total'].astype(float)
df['data_despesa'] = pd.to_datetime(df['data_despesa'])
df['valor_liquidado'] = df['valor_liquidado'].astype(float)
df['valor_estorno_liquidacao']= df['valor_estorno_liquidacao'].astype(float)
df['valor_retido']= df['valor_retido'].astype(float)
df['valor_estorno_pagamento']= df['valor_estorno_pagamento'].astype(float)
df['valor_pago_liquido']= df['valor_pago_liquido'].astype(float)

st.subheader("Gastos por mês da prefeitura de Arraial do Cabo")
st.bar_chart(df['valor_despesa'].groupby(df['data_despesa'].dt.month).sum(),x_label='Mês',y_label='Valor',sort=False)

st.subheader("Top 10 Gastos por órgão da prefeitura de Arraial do Cabo")
st.bar_chart(df['valor_despesa'].groupby(df['orgao']).sum().sort_values(ascending=False).head(10),x_label='Órgão',y_label='Valor',horizontal=True,sort=False)

st.subheader("Top 10 Gastos por secretaria da prefeitura de Arraial do Cabo")
st.bar_chart(df['valor_despesa'].groupby(df['nome_secretria']).sum().sort_values(ascending=False).head(10),x_label='Secretaria',y_label='Valor',horizontal=True,sort=False)

st.subheader("Top 10 Gastos por fornecedor da prefeitura de Arraial do Cabo")
st.bar_chart(df['valor_despesa'].groupby(df['descricao_favorecido']).sum().sort_values(ascending=False).head(10),x_label='Fornecedor',y_label='Valor',horizontal=True,sort=False)

