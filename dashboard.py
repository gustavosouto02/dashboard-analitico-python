import streamlit as st
import pandas as pd
import plotly.express as px 



st.set_page_config(layout="wide", page_title="Dashboard de Vendas", page_icon="💰")
COLOR_SEQUENCE = ["#004b7c", "#005691", "#0073b7", "#0089d0"]


df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df=df.sort_values("Date")

(df["Month"]) = (df["Date"]).apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]
df_filtered

st.markdown("# 🛒 Dashboard de Performance de Vendas")
st.divider()

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# 1. Faturamento por Dia
fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", 
                  title="Faturamento por Dia", 
                  color_discrete_sequence=COLOR_SEQUENCE, # Cores fixas para as cidades
                  template="plotly_white")
col1.plotly_chart(fig_date, width='stretch')


# 2. Faturamento por Tipo de Produto
prod_total = df_filtered.groupby("Product line")[["Total"]].sum().reset_index()
fig_prod = px.bar(prod_total, x="Total", y="Product line", 
                  color="Total", 
                  orientation="h", 
                  title="Faturamento por Tipo de Produto",
                  color_continuous_scale="Blues", # Escala elegante de azul
                  template="plotly_white")
                  fig_prod.update_layout(coloraxis_showscale=False)
                  col2.plotly_chart(fig_prod,  width='stretch')

# 3. Faturamento por Filial
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", 
                  title="Faturamento por Filial",
                  color_discrete_sequence=["#004b7c"], # Cor sólida elegante
                  template="plotly_white")col3.plotly_chart(fig_city,  width='stretch')

# 4. Faturamento por Tipo de Pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment", 
                  title="Distribuição de Pagamento", 
                  hole=0.5, 
                  color_discrete_sequence=["#002d4d", "#004b7c", "#0073b7"],
                  template="plotly_white")
                  col4.plotly_chart(fig_kind, width='stretch')

# 5. Avaliação Média por Filial
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()

fig_rating = px.bar(city_rating, x="City", y="Rating", 
                    range_y=[0, 10], 
                    color_discrete_sequence=["#2ca02c"], # Verde sóbrio para "Rating"
                    template="plotly_white", 
                    title="Avaliação Média")
                    col5.plotly_chart(fig_rating, width='stretch')