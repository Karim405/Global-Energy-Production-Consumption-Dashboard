"""
comparison_B_kpi.py
===================
Person 2 — Comparison Module B + KPI Cards
Global Energy Production & Consumption Dashboard

Contains:
    - function_chart4() : Stacked Bar Chart — Fossil vs Renewable by Continent
    - function_chart5() : Clustered Column Chart — Oil vs Gas vs Coal across top countries
    - function_chart6() : Clustered Column Chart — Solar vs Wind vs Hydro generation comparison
    - get_kpi_values()  : KPI calculations

All chart functions return Plotly figures.
"""

import pandas as pd
import plotly.graph_objects as go

try:
    from shared_ids import DATA_PATH
except ImportError:
    DATA_PATH = "data/cleaned_data.csv"


# ==================================================
# CONTINENT MAPPING
# ==================================================

CONTINENT_MAP = {
    # Africa
    "Egypt": "Africa",
    "Nigeria": "Africa",
    "South Africa": "Africa",
    "Algeria": "Africa",
    "Morocco": "Africa",
    "Kenya": "Africa",

    # Asia
    "China": "Asia",
    "India": "Asia",
    "Japan": "Asia",
    "Saudi Arabia": "Asia",
    "Indonesia": "Asia",
    "South Korea": "Asia",

    # Europe
    "Germany": "Europe",
    "France": "Europe",
    "United Kingdom": "Europe",
    "Italy": "Europe",
    "Spain": "Europe",
    "Netherlands": "Europe",

    # North America
    "United States": "North America",
    "Canada": "North America",
    "Mexico": "North America",

    # South America
    "Brazil": "South America",
    "Argentina": "South America",
    "Chile": "South America",

    # Oceania
    "Australia": "Oceania",
    "New Zealand": "Oceania",
}


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def _safe_numeric(df, columns):
    """
    Convert selected columns to numeric and replace missing values with 0.
    """
    df = df.copy()

    for col in columns:
        if col not in df.columns:
            df[col] = 0

        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def _add_continent(df):
    """
    Add continent column using the continent map.
    Rows without mapped continents are removed.
    """
    df = df.copy()
    df["continent"] = df["country"].map(CONTINENT_MAP)
    df = df.dropna(subset=["continent"])
    return df


def _empty_figure(title):
    """
    Return an empty figure if no data is available.
    """
    fig = go.Figure()
    fig.update_layout(
        title=title,
        template="plotly_white",
        xaxis_title="No data",
        yaxis_title="No data",
    )
    return fig


# ==================================================
# CHART 4
# Stacked Bar Chart:
# Fossil vs Renewable Consumption by Continent
# ==================================================

def function_chart4(df):
    """
    Stacked Bar Chart:
    Fossil vs Renewable Consumption by Continent.
    """

    df = _add_continent(df)

    energy_cols = [
        "coal_production",
        "gas_production",
        "oil_production",
        "renewables_electricity",
    ]

    df = _safe_numeric(df, energy_cols)

    grouped = (
        df.groupby("continent")
        .agg(
            coal=("coal_production", "sum"),
            gas=("gas_production", "sum"),
            oil=("oil_production", "sum"),
            renewable=("renewables_electricity", "sum"),
        )
        .reset_index()
    )

    grouped["fossil"] = grouped["coal"] + grouped["gas"] + grouped["oil"]
    grouped["total"] = grouped["fossil"] + grouped["renewable"]

    grouped = grouped.sort_values("total", ascending=True).reset_index(drop=True)

    if grouped.empty:
        return _empty_figure("Fossil vs Renewable Consumption by Continent — No Data")

    max_idx = grouped["total"].idxmax()

    fossil_standard = "#c6dbef"
    fossil_highest = "#b7e4c7"
    renewable_standard = "#4a90c2"
    renewable_highest = "#2e7d32"

    fossil_colors = [fossil_standard] * len(grouped)
    renewable_colors = [renewable_standard] * len(grouped)

    fossil_colors[max_idx] = fossil_highest
    renewable_colors[max_idx] = renewable_highest

    fig = go.Figure()

    fig.add_bar(
        y=grouped["continent"],
        x=grouped["fossil"],
        name="Fossil",
        orientation="h",
        marker=dict(color=fossil_colors),
        text=grouped["fossil"].round(0),
        textposition="inside",
        insidetextanchor="middle",
        hovertemplate="<b>%{y}</b><br>Fossil: %{x:,.0f} TWh<extra></extra>",
        showlegend=False,
    )

    fig.add_bar(
        y=grouped["continent"],
        x=grouped["renewable"],
        name="Renewable",
        orientation="h",
        marker=dict(color=renewable_colors),
        text=grouped["renewable"].round(0),
        textposition="inside",
        insidetextanchor="middle",
        hovertemplate="<b>%{y}</b><br>Renewable: %{x:,.0f} TWh<extra></extra>",
        showlegend=False,
    )

    legend_items = [
        ("Fossil (Standard)", fossil_standard),
        ("Fossil (Highest Total)", fossil_highest),
        ("Renewable (Standard)", renewable_standard),
        ("Renewable (Highest Total)", renewable_highest),
    ]

    for name, color in legend_items:
        fig.add_bar(
            y=[None],
            x=[None],
            name=name,
            orientation="h",
            marker=dict(color=color),
            showlegend=True,
        )

    for _, row in grouped.iterrows():
        fig.add_annotation(
            x=row["total"],
            y=row["continent"],
            text=f"<b>Total: {int(row['total'])}</b>",
            showarrow=False,
            xshift=55,
            font=dict(color="black", size=11),
        )

    fig.update_layout(
        barmode="stack",
        title={
            "text": "Fossil vs Renewable Consumption by Continent",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(size=18, color="black"),
        },
        xaxis_title="Energy (TWh)",
        yaxis_title="Continent",
        template="plotly_white",
        height=620,
        margin=dict(l=90, r=280, t=90, b=70),

        legend=dict(
            title="Legend",
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="black",
            borderwidth=1,
            font=dict(size=10),
        ),

        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="black", width=1),
            )
        ],
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(0,0,0,0.15)",
        range=[0, grouped["total"].max() * 1.30],
        tickfont=dict(size=11),
        title_font=dict(size=13),
    )

    fig.update_yaxes(
        showgrid=False,
        tickfont=dict(size=12),
        title_font=dict(size=13),
    )

    return fig


# ==================================================
# CHART 5
# Clustered Column Chart:
# Oil vs Gas vs Coal across Top Countries
# ==================================================

def function_chart5(df):
    """
    Clustered Column Chart:
    Oil vs Gas vs Coal across top 10 countries.
    """

    df = _add_continent(df)

    fossil_cols = [
        "oil_production",
        "gas_production",
        "coal_production",
    ]

    df = _safe_numeric(df, fossil_cols)

    grouped = (
        df.groupby("country")[fossil_cols]
        .sum()
        .reset_index()
    )

    grouped["total_fossil"] = (
        grouped["oil_production"]
        + grouped["gas_production"]
        + grouped["coal_production"]
    )

    top = (
        grouped[grouped["total_fossil"] > 0]
        .sort_values("total_fossil", ascending=False)
        .head(10)
        .copy()
    )

    if top.empty:
        return _empty_figure("Oil vs Gas vs Coal — No Data")

    max_oil = top["oil_production"].max()
    max_gas = top["gas_production"].max()
    max_coal = top["coal_production"].max()

    oil_blue = "#9ecae1"
    gas_blue = "#6baed6"
    coal_blue = "#4292c6"

    oil_green = "#b2f2bb"
    gas_green = "#a3e4a9"
    coal_green = "#8fd19e"

    oil_colors = [
        oil_green if value == max_oil else oil_blue
        for value in top["oil_production"]
    ]

    gas_colors = [
        gas_green if value == max_gas else gas_blue
        for value in top["gas_production"]
    ]

    coal_colors = [
        coal_green if value == max_coal else coal_blue
        for value in top["coal_production"]
    ]

    fig = go.Figure()

    fig.add_bar(
        x=top["country"],
        y=top["oil_production"],
        name="Oil",
        marker=dict(color=oil_colors),
        text=top["oil_production"].round(0),
        textposition="outside",
        textfont=dict(size=10, color="black"),
        offsetgroup=0,
        hovertemplate="<b>%{x}</b><br>Oil: %{y:,.0f} TWh<extra></extra>",
        showlegend=False,
    )

    fig.add_bar(
        x=top["country"],
        y=top["gas_production"],
        name="Gas",
        marker=dict(color=gas_colors),
        text=top["gas_production"].round(0),
        textposition="outside",
        textfont=dict(size=10, color="black"),
        offsetgroup=1,
        hovertemplate="<b>%{x}</b><br>Gas: %{y:,.0f} TWh<extra></extra>",
        showlegend=False,
    )

    fig.add_bar(
        x=top["country"],
        y=top["coal_production"],
        name="Coal",
        marker=dict(color=coal_colors),
        text=top["coal_production"].round(0),
        textposition="outside",
        textfont=dict(size=10, color="black"),
        offsetgroup=2,
        hovertemplate="<b>%{x}</b><br>Coal: %{y:,.0f} TWh<extra></extra>",
        showlegend=False,
    )

    # Legend outside the plot area, on the right
    legend_items = [
        ("Oil (Standard)", oil_blue),
        ("Oil (Highest)", oil_green),
        ("Gas (Standard)", gas_blue),
        ("Gas (Highest)", gas_green),
        ("Coal (Standard)", coal_blue),
        ("Coal (Highest)", coal_green),
    ]

    for name, color in legend_items:
        fig.add_bar(
            x=[None],
            y=[None],
            name=name,
            marker=dict(color=color),
            showlegend=True,
        )

    fig.update_layout(
        barmode="group",
        bargap=0.08,
        bargroupgap=0.02,
        title={
            "text": "Oil vs Gas vs Coal — Top 10 Countries",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(size=18, color="black"),
        },
        xaxis_title="Country",
        yaxis_title="Energy Production (TWh)",
        template="plotly_white",

        # Important: extra right margin for the legend
        height=620,
        margin=dict(l=70, r=260, t=90, b=90),

        # Important: vertical legend outside the chart
        legend=dict(
            title="Legend",
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="black",
            borderwidth=1,
            font=dict(size=10),
        ),

        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="black", width=2),
            )
        ],
    )

    fig.update_xaxes(
        tickangle=0,
        automargin=True,
        tickfont=dict(size=11),
        title_font=dict(size=13),
    )

    fig.update_yaxes(
        rangemode="tozero",
        gridcolor="lightgray",
        tickfont=dict(size=11),
        title_font=dict(size=13),
    )

    return fig


# ==================================================
# CHART 6
# Clustered Column Chart:
# Solar vs Wind vs Hydro generation comparison
# ==================================================

def function_chart6(df):
    """
    Clustered Column Chart:
    Solar vs Wind vs Hydro generation comparison for top 10 countries.
    """

    df = _add_continent(df)

    renewable_cols = [
        "solar_electricity",
        "wind_electricity",
        "hydro_electricity",
    ]

    df = _safe_numeric(df, renewable_cols)

    grouped = (
        df.groupby("country")[renewable_cols]
        .sum()
        .reset_index()
    )

    grouped["total_renewables"] = (
        grouped["solar_electricity"]
        + grouped["wind_electricity"]
        + grouped["hydro_electricity"]
    )

    top = (
        grouped[grouped["total_renewables"] > 0]
        .sort_values("total_renewables", ascending=False)
        .head(10)
        .copy()
    )

    if top.empty:
        return _empty_figure("Solar vs Wind vs Hydro — No Data")

    max_solar = top["solar_electricity"].max()
    max_wind = top["wind_electricity"].max()
    max_hydro = top["hydro_electricity"].max()

    solar_blue = "#9ecae1"
    wind_blue = "#6baed6"
    hydro_blue = "#4292c6"

    solar_green = "#b2f2bb"
    wind_green = "#a3e4a9"
    hydro_green = "#8fd19e"

    solar_colors = [
        solar_green if value == max_solar else solar_blue
        for value in top["solar_electricity"]
    ]

    wind_colors = [
        wind_green if value == max_wind else wind_blue
        for value in top["wind_electricity"]
    ]

    hydro_colors = [
        hydro_green if value == max_hydro else hydro_blue
        for value in top["hydro_electricity"]
    ]

    fig = go.Figure()

    fig.add_bar(
        x=top["country"],
        y=top["solar_electricity"],
        name="Solar",
        marker=dict(color=solar_colors),
        text=top["solar_electricity"].round(0),
        textposition="outside",
        textfont=dict(size=10, color="black"),
        offsetgroup=0,
        hovertemplate="<b>%{x}</b><br>Solar: %{y:,.0f} TWh<extra></extra>",
        showlegend=False,
    )

    fig.add_bar(
        x=top["country"],
        y=top["wind_electricity"],
        name="Wind",
        marker=dict(color=wind_colors),
        text=top["wind_electricity"].round(0),
        textposition="outside",
        textfont=dict(size=10, color="black"),
        offsetgroup=1,
        hovertemplate="<b>%{x}</b><br>Wind: %{y:,.0f} TWh<extra></extra>",
        showlegend=False,
    )

    fig.add_bar(
        x=top["country"],
        y=top["hydro_electricity"],
        name="Hydro",
        marker=dict(color=hydro_colors),
        text=top["hydro_electricity"].round(0),
        textposition="outside",
        textfont=dict(size=10, color="black"),
        offsetgroup=2,
        hovertemplate="<b>%{x}</b><br>Hydro: %{y:,.0f} TWh<extra></extra>",
        showlegend=False,
    )

    # Legend outside the plot area, on the right
    legend_items = [
        ("Solar (Standard)", solar_blue),
        ("Solar (Highest)", solar_green),
        ("Wind (Standard)", wind_blue),
        ("Wind (Highest)", wind_green),
        ("Hydro (Standard)", hydro_blue),
        ("Hydro (Highest)", hydro_green),
    ]

    for name, color in legend_items:
        fig.add_bar(
            x=[None],
            y=[None],
            name=name,
            marker=dict(color=color),
            showlegend=True,
        )

    fig.update_layout(
        barmode="group",
        bargap=0.08,
        bargroupgap=0.02,
        title={
            "text": "Solar vs Wind vs Hydro — Top 10 Countries",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(size=18, color="black"),
        },
        xaxis_title="Country",
        yaxis_title="Electricity Generation (TWh)",
        template="plotly_white",

        # Important: extra right margin for the legend
        height=620,
        margin=dict(l=70, r=260, t=90, b=90),

        # Important: vertical legend outside the chart
        legend=dict(
            title="Legend",
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="black",
            borderwidth=1,
            font=dict(size=10),
        ),

        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="black", width=2),
            )
        ],
    )

    fig.update_xaxes(
        tickangle=0,
        automargin=True,
        tickfont=dict(size=11),
        title_font=dict(size=13),
    )

    fig.update_yaxes(
        rangemode="tozero",
        gridcolor="lightgray",
        tickfont=dict(size=11),
        title_font=dict(size=13),
    )

    return fig


# ==================================================
# KPI VALUES
# ==================================================

def get_kpi_values(df):
    """
    Calculate KPI metrics:
        - total global consumption
        - average renewable share
        - top producer
        - average carbon intensity
    """

    df = _add_continent(df)

    required_cols = [
        "primary_energy_consumption",
        "solar_electricity",
        "wind_electricity",
        "hydro_electricity",
        "oil_production",
        "gas_production",
        "coal_production",
        "energy_per_gdp",
    ]

    df = _safe_numeric(df, required_cols)

    total_consumption = df["primary_energy_consumption"].sum()

    df["renewable_total"] = (
        df["solar_electricity"]
        + df["wind_electricity"]
        + df["hydro_electricity"]
    )

    df["renewable_share"] = df.apply(
        lambda row: (
            row["renewable_total"] / row["primary_energy_consumption"] * 100
        )
        if row["primary_energy_consumption"] != 0
        else 0,
        axis=1,
    )

    avg_renewable_share = df["renewable_share"].mean()

    df["total_production"] = (
        df["oil_production"]
        + df["gas_production"]
        + df["coal_production"]
    )

    if not df.empty and df["total_production"].sum() > 0:
        top_producer = df.groupby("country")["total_production"].sum().idxmax()
    else:
        top_producer = "N/A"

    avg_carbon_intensity = df["energy_per_gdp"].mean()

    return {
        "total": total_consumption,
        "avg_renew": avg_renewable_share,
        "top_prod": top_producer,
        "avg_carbon": avg_carbon_intensity,
    }


# ==================================================
# QUICK TEST
# Run: python comparison_B_kpi.py
# ==================================================

if __name__ == "__main__":
    df_test = pd.read_csv(DATA_PATH)

    print("Testing function_chart4() ...")
    fig4 = function_chart4(df_test)
    print("Chart 4 OK")
    fig4.show()

    print("Testing function_chart5() ...")
    fig5 = function_chart5(df_test)
    print("Chart 5 OK")
    fig5.show()

    print("Testing function_chart6() ...")
    fig6 = function_chart6(df_test)
    print("Chart 6 OK")
    fig6.show()

    print("Testing get_kpi_values() ...")
    print(get_kpi_values(df_test))
    print("KPI OK")