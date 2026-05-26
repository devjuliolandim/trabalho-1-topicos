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
    page_title="UNODC Homicides Analysis",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("UNODC Intentional Homicides Analysis")

st.markdown("""
Interactive statistical and regression analysis of intentional homicide rates using the UNODC dataset.
""")

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    url = "https://docs.google.com/spreadsheets/d/1OmnQ7Yut5YDj-7n4LpLtceW8NGWWp3UW/export?format=csv"

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
# =========================================================
# SHOW COLUMNS
# =========================================================

st.sidebar.header("Dataset Information")

st.sidebar.write(df.columns.tolist())

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

df[VALUE_COL] = pd.to_numeric(
    df[VALUE_COL],
    errors="coerce"
)

df[YEAR_COL] = pd.to_numeric(
    df[YEAR_COL],
    errors="coerce"
)

df = df.dropna(
    subset=[COUNTRY_COL, YEAR_COL, VALUE_COL]
)

df[YEAR_COL] = df[YEAR_COL].astype(int)

# =========================================================
# REMOVE INVALID VALUES
# =========================================================

df = df[
    (df[VALUE_COL] >= 0)
]

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Filters")

countries = sorted(df[COUNTRY_COL].unique())

selected_country = st.sidebar.selectbox(
    "Select a Country",
    countries
)

selected_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df[YEAR_COL].min()),
    max_value=int(df[YEAR_COL].max()),
    value=(2013, 2022)
)

future_years = [2023, 2024, 2025, 2026]

# =========================================================
# FILTER DATA
# =========================================================

filtered_df = df[
    (df[COUNTRY_COL] == selected_country) &
    (df[YEAR_COL] >= selected_range[0]) &
    (df[YEAR_COL] <= selected_range[1])
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

st.header(f"{selected_country} Analysis")

st.subheader("Filtered Data")

st.dataframe(filtered_df)

# =========================================================
# TIME SERIES GRAPH
# =========================================================

st.subheader("Homicide Rate Over Time")

fig = px.scatter(
    filtered_df,
    x=YEAR_COL,
    y=VALUE_COL,
    trendline="ols",
    title=f"Homicide Rates - {selected_country}"
)

st.plotly_chart(fig, use_container_width=True)

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