"""
comparison_A.py
===============
Person 1 — Comparison Module A
Global Energy Production & Consumption Dashboard

Contains:
    - function_chart1() : Dynamic Column Chart — Top 10 Countries by Selected Energy Metric
    - function_chart2() : Bar Chart — Top 10 Countries by Renewable Energy Share
    - function_chart3() : Stacked Bar Chart — Energy Mix Composition for Selected Countries

All functions return Plotly figures.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

try:
    from shared_ids import DATA_PATH
except ImportError:
    DATA_PATH = "data/cleaned_data.csv"


# ==================================================
# HELPERS
# ==================================================

AGGREGATE_KEYWORDS = (
    "World|Asia|Europe|Africa|America|OECD|OPEC|CIS|Ember|"
    "income|ASEAN|Middle East|Non-OECD|G20|G7|European Union|"
    "High-income|Low-income|Upper-middle-income|Lower-middle-income|"
    "North America|South America|Oceania"
)


METRIC_LABELS = {
    "renewables_electricity": "Renewable Electricity",
    "solar_electricity": "Solar Electricity",
    "wind_electricity": "Wind Electricity",
    "hydro_electricity": "Hydro Electricity",
    "nuclear_electricity": "Nuclear Electricity",
    "coal_production": "Coal Production",
    "gas_production": "Gas Production",
    "oil_production": "Oil Production",
    "primary_energy_consumption": "Total Energy Consumption",
}


def _clean_column_names(df):
    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
        .str.replace("__", "_", regex=False)
    )

    if "country" not in df.columns:
        for possible_col in ["entity", "location", "name", "country_name"]:
            if possible_col in df.columns:
                df = df.rename(columns={possible_col: "country"})
                break

    return df


def _clean_year_column(df):
    df = df.copy()

    if "year" not in df.columns:
        return pd.DataFrame()

    year_text = df["year"].astype(str)
    extracted_year = year_text.str.extract(r"(\d{4})", expand=False)

    df["year"] = pd.to_numeric(extracted_year, errors="coerce")
    df = df.dropna(subset=["year"])

    if df.empty:
        return df

    df["year"] = df["year"].astype(int)

    return df


def _filter_real_countries(df):
    df = df.copy()

    if "country" not in df.columns:
        return pd.DataFrame()

    df = df[
        ~df["country"].astype(str).str.contains(
            AGGREGATE_KEYWORDS,
            case=False,
            na=False,
            regex=True,
        )
    ].copy()

    return df


def _prepare_latest_real_countries(df):
    df = df.copy()
    df = _clean_column_names(df)
    df = _clean_year_column(df)
    df = _filter_real_countries(df)

    if df.empty or df["year"].dropna().empty:
        return pd.DataFrame(), None

    latest_year = int(df["year"].max())
    df_latest = df[df["year"] == latest_year].copy()

    return df_latest, latest_year


def _safe_numeric(df, columns):
    df = df.copy()

    for col in columns:
        if col not in df.columns:
            df[col] = 0

        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    return df


def _shorten_country_names(df):
    name_map = {
        "United States": "USA",
        "South Korea": "S. Korea",
        "United Kingdom": "UK",
        "United Arab Emirates": "UAE",
    }

    df = df.copy()
    df["country"] = df["country"].replace(name_map)

    return df


def _empty_figure(title):
    fig = go.Figure()

    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
        },
        template="plotly_white",
        height=520,
        xaxis_title="No data",
        yaxis_title="No data",
    )

    return fig


def _standard_layout(fig, title, x_title, y_title, height=560):
    fig.update_layout(
        template="plotly_white",
        title={
            "text": title,
            "x": 0.5,
            "xanchor": "center",
            "font": dict(size=20, color="black"),
        },
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=height,
        margin=dict(l=90, r=230, t=90, b=90),
        font=dict(color="black"),
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
            font=dict(size=12),
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
        showgrid=True,
        gridcolor="lightgray",
        rangemode="tozero",
        tickfont=dict(size=12),
        title_font=dict(size=14),
        automargin=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="lightgray",
        rangemode="tozero",
        tickfont=dict(size=12),
        title_font=dict(size=14),
        automargin=True,
    )

    return fig


# ==================================================
# CHART 1
# Dynamic Column Chart:
# Top 10 Countries by Selected Energy Metric
# ==================================================

def function_chart1(df, metric_col="primary_energy_consumption"):
    """
    Dynamic Column Chart:
    Top 10 Countries by selected energy metric.
    """

    df_latest, latest_year = _prepare_latest_real_countries(df)

    if df_latest.empty or latest_year is None:
        return _empty_figure("Top 10 Countries — No Data")

    if metric_col not in METRIC_LABELS:
        metric_col = "primary_energy_consumption"

    metric_label = METRIC_LABELS.get(metric_col, metric_col)

    df_latest = _safe_numeric(df_latest, [metric_col])
    df_latest = df_latest[df_latest[metric_col] > 0].copy()

    top_10 = (
        df_latest
        .sort_values(metric_col, ascending=False)
        .head(10)
        .copy()
    )

    if top_10.empty:
        return _empty_figure(f"Top 10 Countries by {metric_label} — No Data")

    top_10 = _shorten_country_names(top_10)

    max_value = top_10[metric_col].max()

    top_color = "#8BE88B"
    other_color = "#ADD8E6"

    colors = [
        top_color if value == max_value else other_color
        for value in top_10[metric_col]
    ]

    fig = go.Figure()

    fig.add_bar(
        x=top_10["country"],
        y=top_10[metric_col],
        marker=dict(color=colors),
        text=top_10[metric_col].round(0),
        textposition="outside",
        hovertemplate=f"<b>%{{x}}</b><br>{metric_label}: %{{y:,.0f}} TWh<extra></extra>",
        showlegend=False,
    )

    fig.add_bar(
        x=[None],
        y=[None],
        name="Maximum Performer",
        marker=dict(color=top_color),
        showlegend=True,
    )

    fig.add_bar(
        x=[None],
        y=[None],
        name="Standard Performance",
        marker=dict(color=other_color),
        showlegend=True,
    )

    fig = _standard_layout(
        fig,
        title=f"Top 10 Countries by {metric_label} ({latest_year})",
        x_title="Country",
        y_title=f"{metric_label} (TWh)",
        height=600,
    )

    fig.update_xaxes(tickangle=0)
    fig.update_yaxes(range=[0, max_value * 1.18])

    return fig


# ==================================================
# CHART 2
# Bar Chart:
# Top 10 Countries by Renewable Energy Share
# ==================================================

def function_chart2(df):
    df_latest, latest_year = _prepare_latest_real_countries(df)

    if df_latest.empty or latest_year is None:
        return _empty_figure("Top 10 Countries by Renewable Energy Share — No Data")

    possible_cols = [
        "renewables_share_energy",
        "renewables_consumption",
        "primary_energy_consumption",
        "renewables_electricity",
        "electricity_generation",
    ]

    df_latest = _safe_numeric(df_latest, possible_cols)

    if (
        "renewables_share_energy" in df_latest.columns
        and df_latest["renewables_share_energy"].sum() > 0
    ):
        df_latest["renewable_share"] = df_latest["renewables_share_energy"]

    elif (
        "renewables_consumption" in df_latest.columns
        and df_latest["renewables_consumption"].sum() > 0
    ):
        df_latest["renewable_share"] = (
            df_latest["renewables_consumption"]
            / df_latest["primary_energy_consumption"].replace(0, np.nan)
            * 100
        )

    else:
        df_latest["renewable_share"] = (
            df_latest["renewables_electricity"]
            / df_latest["electricity_generation"].replace(0, np.nan)
            * 100
        )

    df_latest["renewable_share"] = pd.to_numeric(
        df_latest["renewable_share"],
        errors="coerce"
    )

    df_latest = df_latest[
        df_latest["renewable_share"].notna()
        & (df_latest["renewable_share"] > 0)
    ].copy()

    df_latest["renewable_share"] = df_latest["renewable_share"].clip(upper=100)

    top_10 = (
        df_latest
        .sort_values("renewable_share", ascending=False)
        .head(10)
        .copy()
    )

    if top_10.empty:
        return _empty_figure("Top 10 Countries by Renewable Energy Share — No Data")

    top_10 = _shorten_country_names(top_10)
    top_10 = top_10.sort_values("renewable_share", ascending=True)

    max_value = top_10["renewable_share"].max()

    top_color = "#8BE88B"
    other_color = "#ADD8E6"

    colors = [
        top_color if value == max_value else other_color
        for value in top_10["renewable_share"]
    ]

    fig = go.Figure()

    fig.add_bar(
        y=top_10["country"],
        x=top_10["renewable_share"],
        orientation="h",
        marker=dict(color=colors),
        text=top_10["renewable_share"].round(1).astype(str) + "%",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Renewable Share: %{x:.1f}%<extra></extra>",
        showlegend=False,
    )

    fig.add_bar(
        x=[None],
        y=[None],
        orientation="h",
        name="Standard Performance",
        marker=dict(color=other_color),
        showlegend=True,
    )

    fig.add_bar(
        x=[None],
        y=[None],
        orientation="h",
        name="Maximum Performer",
        marker=dict(color=top_color),
        showlegend=True,
    )

    fig = _standard_layout(
        fig,
        title=f"Top 10 Countries by Renewable Energy Share ({latest_year})",
        x_title="Renewable Energy Share (%)",
        y_title="Country",
        height=650,
    )

    fig.update_xaxes(range=[0, min(110, max_value * 1.20)])
    fig.update_yaxes(showgrid=False)

    fig.update_layout(
        margin=dict(l=150, r=240, t=90, b=90),
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
            font=dict(size=12),
        ),
    )

    return fig


# ==================================================
# CHART 3
# Stacked Bar Chart:
# Energy Mix Composition for Selected Countries
# ==================================================

def function_chart3(df):
    df_latest, latest_year = _prepare_latest_real_countries(df)

    if df_latest.empty or latest_year is None:
        return _empty_figure("Energy Mix Composition — No Data")

    source_cols = [
        "coal_production",
        "oil_production",
        "gas_production",
        "renewables_electricity",
    ]

    df_latest = _safe_numeric(df_latest, source_cols)

    df_latest["Coal"] = df_latest["coal_production"]
    df_latest["Oil"] = df_latest["oil_production"]
    df_latest["Gas"] = df_latest["gas_production"]
    df_latest["Renewables"] = df_latest["renewables_electricity"]

    df_latest["total"] = (
        df_latest["Coal"]
        + df_latest["Oil"]
        + df_latest["Gas"]
        + df_latest["Renewables"]
    )

    top = (
        df_latest[df_latest["total"] > 0]
        .sort_values("total", ascending=False)
        .head(5)
        .copy()
    )

    if top.empty:
        return _empty_figure("Energy Mix Composition — No Data")

    top = _shorten_country_names(top)
    top = top.sort_values("total", ascending=True)

    max_total = top["total"].max()
    highest_country = top.loc[top["total"].idxmax(), "country"]

    colors = {
        "Coal": "#BFD7EA",
        "Oil": "#9BC4D9",
        "Gas": "#5DADE2",
        "Renewables": "#82E082",
    }

    fig = go.Figure()

    for source in ["Coal", "Oil", "Gas", "Renewables"]:
        fig.add_bar(
            y=top["country"],
            x=top[source],
            name=source,
            orientation="h",
            marker=dict(
                color=colors[source],
                line=dict(color="white", width=1),
            ),
            text=[
                f"{value:.0f}" if value > 0 else ""
                for value in top[source]
            ],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="black", size=11),
            hovertemplate=f"<b>%{{y}}</b><br>{source}: %{{x:.0f}} TWh<extra></extra>",
        )

    for _, row in top.iterrows():
        if row["country"] == highest_country:
            label = f"<b>Highest Total: {row['total']:.0f}</b>"
        else:
            label = f"<b>Total: {row['total']:.0f}</b>"

        fig.add_annotation(
            x=row["total"] + max_total * 0.03,
            y=row["country"],
            text=label,
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=12, color="black"),
        )

    fig.update_layout(
        title={
            "text": f"Energy Mix Composition for Selected Countries ({latest_year})",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(size=20, color="black"),
        },
        xaxis_title="Total Energy (TWh)",
        yaxis_title="Country",
        barmode="stack",
        template="plotly_white",
        height=650,
        font=dict(color="black"),
        margin=dict(l=130, r=260, t=90, b=80),

        legend=dict(
            title="Energy Source",
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="black",
            borderwidth=1,
            font=dict(size=12),
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
        gridcolor="lightgray",
        rangemode="tozero",
        range=[0, max_total * 1.45],
        title_font=dict(size=14),
        tickfont=dict(size=12),
    )

    fig.update_yaxes(
        showgrid=False,
        title_font=dict(size=14),
        tickfont=dict(size=13),
    )

    return fig


# ==================================================
# QUICK TEST
# Run: python comparison_A.py
# ==================================================

if __name__ == "__main__":
    df_test = pd.read_csv(DATA_PATH)

    print("Testing function_chart1() ...")
    function_chart1(df_test).show()
    print("Chart 1 OK")

    print("Testing function_chart2() ...")
    function_chart2(df_test).show()
    print("Chart 2 OK")

    print("Testing function_chart3() ...")
    function_chart3(df_test).show()
    print("Chart 3 OK")