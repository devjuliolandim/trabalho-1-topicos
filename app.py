# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="UNODC: Análise de Homicídios",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("UNODC: Análise de Homicídios")

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    url = "https://docs.google.com/spreadsheets/d/1OmnQ7Yut5YDj-7n4LpLtceW8NGWWp3UW/export?format=csv"

    url2 = "https://docs.google.com/spreadsheets/d/1-RGrWWvZf7u58g9tO0Ev2kBQZq1VMhRi/export?format=csv"

    df = pd.read_csv(url)

    return df

df = load_data()
df = df[
    (df["Dimension"] == "Total") &
    (df["Sex"] == "Total") &
    (df["Age"] == "Total") &
    (df["Category"] == "Total") &
    (df['Unit of measurement'] == 'Rate per 100,000 population')
]

df_original = load_data()
# =========================================================
# SHOW COLUMNS
# =========================================================

# st.sidebar.header("Dataset Information")

# st.sidebar.write(df.columns.tolist())

# =========================================================
# COLUMN CONFIG
# =========================================================
# IMPORTANT:
# CHANGE THESE NAMES IF NECESSARY

COUNTRY_COL = "Country"
YEAR_COL = "Year"
VALUE_COL = "VALUE"

# =========================================================
# DATA CLEANING
# =========================================================

# MENSAGEM PRO JULIO: OS DADOS NÃO PRECISAM DE LIMPEZA, NÃO TEM VALORES NEGATIVOS OU NÃO NUMÉRICOS
# NO PIOR DOS CASOS O VALOR É ZERO
# O "TRATAMENTO" ANTERIOR TAVA COMENDO VÁRIAS LINHAS COM DADOS NORMAIS, PRINCIPALMENTE AS QUE TINHAM NUMEROS QUEBRADOS
# O DATASET FILTRADO TAVA PRATICAMENTE SEM NENHUMA TAXA POR 100K HABITANTES POR CAUSA DISSO

df_original['VALUE'] = df_original['VALUE'].astype(str).str.replace(',', '.')
df_original['VALUE'] = pd.to_numeric(df_original['VALUE'], errors='coerce')

# df["VALUE"] = pd.to_numeric(
#     df["VALUE"],
#     errors="coerce"
# )

# df[YEAR_COL] = pd.to_numeric(
#     df[YEAR_COL],
#     errors="coerce"
# )

# df = df.dropna(
#     subset=[COUNTRY_COL, YEAR_COL, VALUE_COL]
# )

# df[YEAR_COL] = df[YEAR_COL].astype(int)

# =========================================================
# REMOVE INVALID VALUES
# =========================================================

# ISSO TA REMOVENDO LINHA QUE NÃO ERA PRA REMOVER
# df = df[
#     (df["VALUE"] >= 0)
# ]

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Filtros")

st.sidebar.subheader("Localização")

regions = sorted(df_original["Region"].unique())
selected_region = st.sidebar.selectbox(
    "Região:",
    regions
)

df_region = df_original[df_original["Region"] == selected_region]

subregions = sorted(df_region["Subregion"].unique())
selected_subregion = st.sidebar.selectbox(
    "Subregião:",
    subregions
)

df_subregion = df_region[df_region["Subregion"] == selected_subregion]

paises = sorted(df_subregion["Country"].unique())
selected_country = st.sidebar.selectbox(
    "País:",
    paises
)

df_countries = df_subregion[df_subregion["Country"] == selected_country]

st.sidebar.subheader("Tipo de dado")

indicators = sorted(df_countries["Indicator"].unique())
selected_indicator = st.sidebar.selectbox(
    "Indicador:",
    indicators
)

df_indicators = df_countries[df_countries["Indicator"] == selected_indicator]

dimensions = sorted(df_indicators["Dimension"].unique())
selected_dimension = st.sidebar.selectbox(
    "Dimensão:",
    dimensions
)

df_dimensions = df_indicators[df_indicators["Dimension"] == selected_dimension]

categories = sorted(df_dimensions["Category"].unique())
selected_category = st.sidebar.selectbox(
    "Categoria:",
    categories
)

df_categories = df_dimensions[df_dimensions["Category"] == selected_category]

sexes = sorted(df_dimensions["Sex"].unique())
selected_sex = st.sidebar.selectbox(
    "Sexo:",
    sexes
)

df_sexes = df_categories[df_categories["Sex"] == selected_sex]

ages = sorted(df_sexes["Age"].unique())
selected_age = st.sidebar.selectbox(
    "Idade:",
    ages
)

df_ages = df_sexes[df_sexes["Age"] == selected_age]

units = sorted(df_ages["Unit of measurement"].unique())
selected_unit = st.sidebar.selectbox(
    "Unidade de medida:",
    units
)

df_units = df_ages[df_ages["Unit of measurement"] == selected_unit]

st.sidebar.subheader("Datas")

selected_range = st.sidebar.slider(
    "Intervalo de anos:",
    min_value=int(df[YEAR_COL].min()),
    max_value=int(df[YEAR_COL].max()),
    value=(2013, 2022)
)

future_years = [2023, 2024, 2025, 2026]

# =========================================================
# CUSTOM CSS - REDUZIR PADDING DA SIDEBAR
# =========================================================

st.markdown(
    """
    <style>
        /* 1. Reduz o espaçamento geral (gap) entre todos os blocos da sidebar */
        [data-testid="stSidebarUserContent"] .stElementContainer {
            margin-bottom: -0.5rem; /* Ajuste este valor para mais ou para menos */
            margin-top: -0.2rem;
        }

        /* 2. Reduz o espaço interno (padding) do container principal da sidebar */
        [data-testid="stSidebarUserContent"] {
            padding-top: 0.8rem;
            padding-bottom: 0.8rem;
        }
        
        /* 3. Se quiser aproximar ainda mais os títulos dos selectboxes */
        div[data-testid="stWidgetLabel"] p {
            margin-bottom: -0.2rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# FILTER DATA
# =========================================================

# filtered_df = df_units[
#     (df_units["Year"] >= selected_range[0]) &
#     (df_units["Year"] <= selected_range[1])
# ]

filtered_df = df_original[
    (df_original["Year"] >= selected_range[0]) &
    (df_original["Year"] <= selected_range[1]) &
    (df_original['Region'] == selected_region) &
    (df_original['Subregion'] == selected_subregion) &
    (df_original['Country'] == selected_country) &
    (df_original['Indicator'] == selected_indicator) &
    (df_original['Dimension'] == selected_dimension) &
    (df_original['Category'] == selected_category) &
    (df_original['Sex'] == selected_sex) &
    (df_original['Age'] == selected_age) &
    (df_original['Unit of measurement'] == selected_unit)
]

filtered_df = filtered_df.sort_values(YEAR_COL)

# =========================================================
# GLOBAL DATASET FOR RANGE
# =========================================================

global_range_df = df[
    (df[YEAR_COL] >= selected_range[0]) &
    (df[YEAR_COL] <= selected_range[1])
]

# =========================================================
# COUNTRY DATA
# =========================================================

st.header(f"Análise de {selected_country}")

st.subheader("Dados Filtrados")

st.dataframe(filtered_df)

# =========================================================
# TIME SERIES GRAPH
# =========================================================

if selected_unit == "Counts":
    st.subheader(f"Quantidade de homicídios ao longo dos anos")
else:
    st.subheader(f"Taxa de homicídios ao longo dos anos")

fig = px.scatter(
    filtered_df,
    x="Year",
    y="VALUE",
    trendline="ols",
    title=f"{selected_unit} - {selected_country}",
    labels={
        "Year": "Ano",
        "VALUE": f"{selected_unit}"
    }
)

fig.update_xaxes(dtick=1)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# MAPA INTERATIVO GLOBAL ANIMAÇÃO POR ANO
# =========================================================

st.header("Homícidios no Mundo")

selected_unit2 = st.selectbox(
    "Unidade de medida:",
    ["Counts", "Rate per 100,000 population"]
)

# Filtramos os dados mantendo todos os países, mas ordenando por ano para a animação funcionar
map_df = df_original[
    (df_original['Year'] >= df_original["Year"].min()) &
    (df_original['Year'] <= df_original["Year"].max()) &
    (df_original['Indicator'] == 'Victims of intentional homicide') &
    (df_original['Dimension'] == 'Total') &
    (df_original['Category'] == 'Total') &
    (df_original['Sex'] == 'Total') &
    (df_original['Age'] == 'Total') &
    (df_original['Unit of measurement'] == selected_unit2)
]

v_min = map_df['VALUE'].min()
v_max = map_df['VALUE'].max()

# Garantir que os anos estejam ordenados cronologicamente (essencial para a animação)
map_df = map_df.sort_values(by="Year")

# Criando o mapa choropleth animado
fig_map = px.choropleth(
    map_df,
    locations="Iso3_code",          # Coluna com os nomes dos países
    locationmode="ISO-3",   # Identificar por nome do país
    color="VALUE",                # Coluna que define o gradiente de cor
    hover_name="Country",         # Título no card ao passar o mouse
    animation_frame="Year",       # Cria o slider e o botão Play por Ano
    color_continuous_scale=px.colors.sequential.Reds, # Gradiente de cores (tons de vermelho)
    range_color=[v_min, v_max],
    labels={
        "VALUE": f"{selected_unit2}",
        "Year": "Ano"
    },
    title="Mapa Mundi: Homicídio"
)

# Customizações de layout do mapa para ficar mais limpo e fluido
fig_map.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular' # Formato do mapa múndi
    ),
    height=600, # Altura do gráfico
)

# Ajustar a velocidade da animação (1 segundo = 1000 milissegundos)
fig_map.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
fig_map.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 500

# Exibir o mapa no Streamlit
st.plotly_chart(fig_map, use_container_width=True)


# =========================================================
# STATISTICS
# =========================================================

st.header("Statistical Analysis")

# =========================================================
# COUNTRY STATS
# =========================================================

country_mean = filtered_df[VALUE_COL].mean()
country_std = filtered_df[VALUE_COL].std()
country_median = filtered_df[VALUE_COL].median()
country_min = filtered_df[VALUE_COL].min()
country_max = filtered_df[VALUE_COL].max()

# =========================================================
# PEARSON COUNTRY
# =========================================================

country_pearson = filtered_df[[YEAR_COL, VALUE_COL]].corr(
    method="pearson"
).iloc[0,1]

# =========================================================
# GLOBAL PEARSON
# =========================================================

global_pearson = global_range_df[[YEAR_COL, VALUE_COL]].corr(
    method="pearson"
).iloc[0,1]

# =========================================================
# LAYOUT
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Mean", round(country_mean, 3))
    st.metric("STD", round(country_std, 3))

with col2:
    st.metric("Median", round(country_median, 3))
    st.metric("Min", round(country_min, 3))

with col3:
    st.metric("Max", round(country_max, 3))
    st.metric("Pearson", round(country_pearson, 3))

# =========================================================
# PEARSON EXPLANATION
# =========================================================

st.subheader("Pearson Correlation")

st.markdown(f"""
### Selected Country Pearson
Correlation between Year and Homicide Rate for **{selected_country}**:

**Pearson = {country_pearson:.4f}**

### Global Pearson
Correlation considering ALL countries in the selected range:

**Pearson = {global_pearson:.4f}**
""")

# =========================================================
# PEARSON INTERPRETATION
# =========================================================

if abs(country_pearson) > 0.7:
    st.success("Strong linear correlation detected.")
elif abs(country_pearson) > 0.4:
    st.warning("Moderate linear correlation detected.")
else:
    st.error("Weak linear correlation detected.")

# =========================================================
# REGRESSION
# =========================================================

st.header("Regression and Forecast")

X = filtered_df[[YEAR_COL]]
y = filtered_df[VALUE_COL]

model = LinearRegression()

model.fit(X, y)

# =========================================================
# CURRENT PREDICTIONS
# =========================================================

predictions = model.predict(X)

r2 = r2_score(y, predictions)

# =========================================================
# FUTURE PREDICTIONS
# =========================================================

future_df = pd.DataFrame({
    YEAR_COL: future_years
})

future_predictions = model.predict(future_df)

# =========================================================
# REGRESSION PLOT
# =========================================================

fig2 = go.Figure()

# Real points
fig2.add_trace(
    go.Scatter(
        x=filtered_df[YEAR_COL],
        y=filtered_df[VALUE_COL],
        mode="markers+lines",
        name="Real Data"
    )
)

# Regression line
fig2.add_trace(
    go.Scatter(
        x=filtered_df[YEAR_COL],
        y=predictions,
        mode="lines",
        name="Regression"
    )
)

# Future predictions
fig2.add_trace(
    go.Scatter(
        x=future_years,
        y=future_predictions,
        mode="markers+lines",
        name="Forecast"
    )
)

fig2.update_layout(
    title=f"Forecast for {selected_country}",
    xaxis_title="Year",
    yaxis_title="Homicide Rate"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================================================
# REGRESSION METRICS
# =========================================================

st.subheader("Regression Metrics")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Slope",
        round(model.coef_[0], 4)
    )

with col5:
    st.metric(
        "Intercept",
        round(model.intercept_, 4)
    )

with col6:
    st.metric(
        "R²",
        round(r2, 4)
    )

# =========================================================
# REGRESSION EQUATION
# =========================================================

st.latex(
    rf"y = {model.coef_[0]:.4f}x + {model.intercept_:.4f}"
)

# =========================================================
# FUTURE TABLE
# =========================================================

st.subheader(f"Future Predictions for {selected_country}")

future_results = pd.DataFrame({
    "Year": future_years,
    "Predicted Homicide Rate": np.round(
        future_predictions,
        3
    )
})

st.dataframe(future_results)

# =========================================================
# ALL COUNTRIES PREDICTIONS
# =========================================================

st.header("Forecast Table - All Countries")

all_predictions = []

for country in countries:

    temp_df = df[
        (df[COUNTRY_COL] == country) &
        (df[YEAR_COL] >= selected_range[0]) &
        (df[YEAR_COL] <= selected_range[1])
    ]

    temp_df = temp_df.dropna(
        subset=[YEAR_COL, VALUE_COL]
    )

    if len(temp_df) < 2:
        continue

    X_temp = temp_df[[YEAR_COL]]
    y_temp = temp_df[VALUE_COL]

    temp_model = LinearRegression()

    temp_model.fit(X_temp, y_temp)

    future_temp = pd.DataFrame({
        YEAR_COL: future_years
    })

    preds = temp_model.predict(future_temp)

    all_predictions.append({
        "Country": country,
        "2023": round(preds[0], 3),
        "2024": round(preds[1], 3),
        "2025": round(preds[2], 3),
        "2026": round(preds[3], 3)
    })

forecast_df = pd.DataFrame(all_predictions)

st.dataframe(forecast_df)

# =========================================================
# DOWNLOAD BUTTON
# =========================================================

csv = forecast_df.to_csv(index=False)

st.download_button(
    label="Download Forecast Table CSV",
    data=csv,
    file_name="forecast_table.csv",
    mime="text/csv"
)

