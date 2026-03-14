import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px

st.set_page_config(page_title="Vendas de Chocolates")



df = pd.read_csv("chocolate_sales_2025_dataset.csv")

df['Date'] = pd.to_datetime(df['Date'])

st.sidebar.header("Filtros")

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Selecione o período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if st.sidebar.button("Resetar filtro"):
    date_range = (min_date, max_date)

df_filtrado = df[
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

vendas_marcas = df_filtrado.groupby('Brand')['Units_Sold'].sum().reset_index()
vendas_marcas = vendas_marcas.sort_values(by='Units_Sold', ascending=False)


vendas_registradas = len(df_filtrado)
qtd_total_vendida = df_filtrado['Units_Sold'].sum()
faturamento_total = df_filtrado['Revenue_USD'].sum()
faturamento_formatado = f"{faturamento_total/1000:.1f}K"
preco_medio = df_filtrado['Price_USD'].mean()

st.title("🍫 Vendas de Chocolate 2025")

st.caption(
"Dashboard interativo desenvolvido em Python para análise exploratória de vendas de chocolate "
"utilizando Pandas, Altair e Streamlit."
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Vendas Registradas", f" {vendas_registradas}", delta=None)
with col2:
    st.metric("Quantidade Vendida", f" {qtd_total_vendida:,}", delta=None)
with col3:
    st.metric("Preço Médio", f"$ {preco_medio:,.2f}", delta=None)
with col4:
    st.metric("Faturamento Total", f"$ {faturamento_formatado}", delta=None)

st.divider()

##### GRAFICO 1 Univades Vendidas por Marca ############

st.subheader('🍫 Unidades Vendidas', )
st.write("*Objetivo: identificar qual marca possui o maior volume de unidades vendidas.*")

bar_chart1 = alt.Chart(vendas_marcas).mark_bar(size=20).encode(
        x=alt.X('Units_Sold', title='',axis=alt.Axis(grid=False,labels=False)),
        y=alt.Y('Brand', title='',sort="-x"),
        color=alt.Color('Units_Sold', scale=alt.Scale(scheme='browns'), legend=None),
        tooltip=[alt.Tooltip('Brand:N', title='Marca'),
    alt.Tooltip('Units_Sold:Q', title='Unidades', format=',')]
    ).properties(width=700,
    height=250,title='').interactive()

text_chart1 = bar_chart1.mark_text(align='left', dx=5).encode(
        text=alt.Text('Units_Sold', format=''),
        color=alt.value('white')
    )
final_chart_clientes = bar_chart1 + text_chart1

st.altair_chart(final_chart_clientes, use_container_width=True)


st.divider()

st.write("*Objetivo: identificar qual marca possui o maior receita.*")

extra = df_filtrado.groupby('Brand')['Revenue_USD'].sum().reset_index()
extra = extra.sort_values(by='Revenue_USD', ascending=False)

bar_chartextra = alt.Chart(extra).mark_bar(size=20).encode(
        x=alt.X('Revenue_USD', title='',axis=alt.Axis(grid=False,labels=False)),
        y=alt.Y('Brand', title='',sort="-x"),
        color=alt.Color('Revenue_USD', scale=alt.Scale(scheme='browns'), legend=None),
        tooltip=[alt.Tooltip('Brand:N', title='Marca'),
    alt.Tooltip('Revenue_USD:Q', title='Unidades', format=',')]
    ).properties(width=700,
    height=250,title='').interactive()

text_charte = bar_chartextra.mark_text(align='left', dx=-50).encode(
        text=alt.Text('Revenue_USD', format='$,.0f'),
        color=alt.value('Black')
    )
final_chart_clientes2 = bar_chartextra + text_charte

st.altair_chart(final_chart_clientes2, use_container_width=True)


st.divider()



tipo_chocolate = df_filtrado.groupby('Product_Type')['Units_Sold'].sum().reset_index()
tipo_chocolate = tipo_chocolate.sort_values(by='Units_Sold', ascending=False)

st.write("*Objetivo: identificar qual tipo de cholatate é mais vendido.*")

bar_chart_tipo = alt.Chart(tipo_chocolate).mark_bar(size=20).encode(
        x=alt.X('Units_Sold', title='',axis=alt.Axis(grid=False,labels=False)),
        y=alt.Y('Product_Type', title='',sort="-x"),
        color=alt.Color('Units_Sold', scale=alt.Scale(scheme='browns'), legend=None),
        tooltip=[alt.Tooltip('Product_Type:N', title='Tipo'),
    alt.Tooltip('Units_Sold:Q', title='Unidades', format=',')]
    ).properties(width=700,
    height=250,title='').interactive()

text_chart_tipo = bar_chart_tipo.mark_text(align='left', dx=5).encode(
        text=alt.Text('Units_Sold', format=''),
        color=alt.value('white')
    )
final_chart_tipo = bar_chart_tipo + text_chart_tipo

st.altair_chart(final_chart_tipo, use_container_width=True)


st.divider()

##### GRAFICO 2 Preço Medio ############

preco_medioG = df_filtrado.groupby('Brand')['Price_USD'].mean().reset_index()

st.subheader('💲 Preço Médio por Marca', )
st.write("*Objetivo: identificar o preço médio de cada venda por marca.*")

linha = alt.Chart(preco_medioG).mark_rule(size=1,color="gray").encode(
    x=alt.X('Price_USD:Q',title='',axis=alt.Axis(grid=False,labels=False)),
    y=alt.Y('Brand:N', sort='-x',title='')
)

ponto = alt.Chart(preco_medioG).mark_circle(size=120).encode(
    x='Price_USD:Q',
    y=alt.Y('Brand:N', sort='-x'),
    color=alt.Color('Price_USD:Q', scale=alt.Scale(scheme='browns'), legend=None)
)

text_chart2 = ponto.mark_text(align='left', dx=5).encode(
        text=alt.Text('Price_USD:Q', format='.2f'),
        color=alt.value('white')
    )

lollipop_chart = (linha + ponto + text_chart2).properties(
    width=700,
    height=250, title=''
)

st.altair_chart(lollipop_chart, use_container_width=True)

st.divider()

##### GRAFICO 3 Vendas por pais ############

Receita_por_pais = df_filtrado.groupby('Country')['Revenue_USD'].sum().reset_index()

st.subheader('🗺  Analise por País')
st.write("*Objetivo: identificar qual país gerou maior receita.*")

bar_chart3 = alt.Chart(Receita_por_pais).mark_bar(size=18).encode(
        x=alt.X('Revenue_USD', title='',axis=alt.Axis(grid=False,labels=False)),
        y=alt.Y('Country', title='',sort="-x"),
        color=alt.Color('Revenue_USD', scale=alt.Scale(scheme='browns'), legend=None),
        tooltip=[alt.Tooltip('Country:N', title='País'),
    alt.Tooltip('Revenue_USD:Q', title='Receita', format=',')]
    ).properties(width=600,
    height=300,title='').interactive()

text_chart3 = bar_chart3.mark_text(align='center', dx=-25).encode(
        text=alt.Text('Revenue_USD:Q', format='$,.0f'),
        color=alt.value('black')
    )

final_chart_clientes3 = bar_chart3 + text_chart3

st.altair_chart(final_chart_clientes3, use_container_width=True)


st.divider()

##### GRAFICO 5 HEATMAP ############

qtd_pais = df_filtrado.groupby('Country')['Units_Sold'].sum().reset_index()
qtd_pais = qtd_pais.sort_values(by='Units_Sold', ascending=False)

st.write("*Objetivo: Identificar qual país consumiu mais chocolate.*")
st.write('\n')

bar_chart4 = alt.Chart(qtd_pais).mark_bar(size=18).encode(
        x=alt.X('Units_Sold', title='',axis=alt.Axis(grid=False,labels=False)),
        y=alt.Y('Country', title='',sort="-x"),
        color=alt.Color('Units_Sold', scale=alt.Scale(scheme='browns'), legend=None),
        tooltip=[alt.Tooltip('Country:N', title='País'),
    alt.Tooltip('Units_Sold:Q', title='QTD', format=',')]
    ).properties(width=500,
    height=300,title='').interactive()

text_chart4 = bar_chart4.mark_text(align='center', dx=-20).encode(
        text=alt.Text('Units_Sold:Q', format=''),
        color=alt.value('black')
    )

final_chart_clientes4 = bar_chart4 + text_chart4

st.altair_chart(final_chart_clientes4, use_container_width=True)

st.divider()

##### GRAFICO 5 HEATMAP ############

st.write("*Objetivo: Heatmap para identificar qual marca gera mais receita por país.*")
st.write('\n')

Receita_por_pais_marca = df_filtrado.groupby(['Country','Brand'])['Revenue_USD'].sum().reset_index()

treemap = alt.Chart(Receita_por_pais_marca).mark_rect().encode(
    x=alt.X('Brand:N', title=''),
    y=alt.Y('Country:N', title=''),
    color=alt.Color(
        'Revenue_USD:Q',
        scale=alt.Scale(scheme='browns'),
        title='Faturamento'
    ),
    tooltip=[
        alt.Tooltip('Country:N', title='País'),
        alt.Tooltip('Brand:N', title='Marca'),
        alt.Tooltip('Revenue_USD:Q', title='Receita', format='$,.0f')
    ]
).properties(
    width=700,
    height=400, title=''
)

st.altair_chart(treemap, use_container_width=True)

st.divider()

##### GRAFICO MAPA ############
st.write("*Objetivo: Identificar a receita por país.*")

mapa = df_filtrado.groupby('Country')['Revenue_USD'].sum().reset_index()

fig = px.choropleth(
    mapa,
    locations="Country",
    locationmode="country names",
    color="Revenue_USD",
    color_continuous_scale="YlOrBr",
    hover_name="Country",
    hover_data={"Revenue_USD": ":$,.0f"},
)

fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        coastlinecolor="gray",
        bgcolor="rgba(0,0,0,0)"
    )
)

fig.update_geos(
    projection_type="natural earth"
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

##### GRAFICO 6 SCATTERPLOT ############

st.subheader('📈 Relação entre Preço e Receita')
st.write("*Objetivo: Analisar se produtos com preços mais altos tendem a gerar maior receita.*")

scatter = alt.Chart(df_filtrado).mark_circle(size=80, opacity=0.7).encode(
    x=alt.X('Price_USD:Q', title='Preço'),
    y=alt.Y('Revenue_USD:Q', title='Receita'),
    color=alt.Color('Brand:N', scale=alt.Scale(scheme='tableau10'),legend=alt.Legend(title="Marca")),
    tooltip=[
        alt.Tooltip('Brand:N', title='Marca'),
        alt.Tooltip('Country:N', title='País'),
        alt.Tooltip('Price_USD:Q', title='Preço', format='$,.2f'),
        alt.Tooltip('Revenue_USD:Q', title='Receita', format='$,.0f')
    ]
).properties(
    width=700,
    height=400,
    title=''
).interactive()



st.altair_chart(scatter, use_container_width=True)

st.divider()

#####  GRAFICO 7  ############



vendas_tempo = df_filtrado.groupby('Date')['Revenue_USD'].sum().reset_index()


st.subheader("📅 Evolução das Vendas ao Longo do Tempo")

st.caption(
"Objetivo: analisar a tendência da receita ao longo do período e identificar possíveis picos ou quedas nas vendas."
)

line_chart = alt.Chart(vendas_tempo).mark_line(
    color="#5C3A21",
    strokeWidth=3
).encode(
    x=alt.X(
        'Date:T',
        title=''
    ),
    y=alt.Y(
        'Revenue_USD:Q',
        title=''
    ),
    tooltip=[
        alt.Tooltip('Date:T', title='Data'),
        alt.Tooltip('Revenue_USD:Q', title='Receita', format='$,.0f')
    ]
).properties(
    width=700,
    height=350
).interactive()

pontos1 = alt.Chart(vendas_tempo).mark_circle(
    size=60,
    color="#8B694A"
).encode(
    x='Date:T',
    y='Revenue_USD:Q'
)

line_chart_final = line_chart + pontos1
st.altair_chart(line_chart_final, use_container_width=True)

st.divider()

#####  GRAFICO 8  ############

pagamento = df_filtrado.groupby('Payment_Method')['Revenue_USD'].sum().reset_index()
pagamento['Percent'] = pagamento['Revenue_USD'] / pagamento['Revenue_USD'].sum()


st.subheader("💳 Receita por Método de Pagamento")

st.caption(
"Objetivo: identificar quais métodos de pagamento geram maior receita nas vendas."
)

donut = alt.Chart(pagamento).mark_arc(innerRadius=80).encode(
    theta=alt.Theta("Revenue_USD:Q"),
    color=alt.Color(
        "Payment_Method:N",
        scale=alt.Scale(scheme="blueorange"),
        legend=alt.Legend(title="Método")
    ),
    tooltip=[
        alt.Tooltip("Payment_Method:N", title="Pagamento"),
        alt.Tooltip("Revenue_USD:Q", title="Receita", format="$,.0f")
    ]
).properties(
    width=300,
    height=350
)

text = alt.Chart(pagamento).mark_text(
    radius=120,
    size=14,
    color="black"
).encode(
    theta=alt.Theta("Revenue_USD:Q", stack=True),
    text=alt.Text("Percent:Q", format=".0%")
)

st.altair_chart(donut + text, use_container_width=True)




st.divider()

st.subheader("📂 Fonte dos Dados")

st.markdown(
"Dataset disponível no Kaggle: "
"https://www.kaggle.com/datasets/syedaeman2212/chocolate-sales-dataset-in-2025/data"
)

with st.expander("Visualizar dataset"):
    st.dataframe(df)

st.markdown("---")
st.markdown('🔗 Desenvolvido por [Richard Silva](https://www.linkedin.com/in/richard-silva-555887195/)')