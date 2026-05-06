"""
time_filters.py
---------------
Person 4 — Time Series Module + Interactive Filters
Global Energy Production & Consumption Dashboard
"""

import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

try:
    from shared_ids import Filters
except ImportError:
    class Filters:
        COUNTRY_DROPDOWN = "country-dropdown"
        CONTINENT_CHECKLIST = "continent-checklist"
        YEAR_SLIDER = "year-slider"
        RESET_BTN = "reset-filters-btn"


# ==================================================
# DATA HELPERS
# ==================================================

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

    return df


def _load_data(filepath="data/cleaned_data.csv"):
    df = pd.read_csv(filepath)
    df = _clean_column_names(df)

    possible_country_cols = [
        "country",
        "entity",
        "location",
        "name",
        "countries",
        "country_name",
    ]

    found_country_col = None

    for col in possible_country_cols:
        if col in df.columns:
            found_country_col = col
            break

    if found_country_col is None:
        print("\nAVAILABLE COLUMNS IN DATASET:")
        print(df.columns.tolist())
        raise KeyError("No country column found.")

    if found_country_col != "country":
        df = df.rename(columns={found_country_col: "country"})

    possible_year_cols = ["year", "date", "time"]

    found_year_col = None

    for col in possible_year_cols:
        if col in df.columns:
            found_year_col = col
            break

    if found_year_col is None:
        print("\nAVAILABLE COLUMNS IN DATASET:")
        print(df.columns.tolist())
        raise KeyError("No year column found.")

    if found_year_col != "year":
        df = df.rename(columns={found_year_col: "year"})

    year_text = df["year"].astype(str)
    extracted_year = year_text.str.extract(r"(\d{4})", expand=False)

    df["year"] = pd.to_numeric(extracted_year, errors="coerce")

    if df["year"].dropna().empty:
        print("\nYEAR COLUMN SAMPLE VALUES:")
        print(year_text.head(20).tolist())
        raise ValueError("Could not extract valid years.")

    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    return df


def _get_global_trend(df):
    df = df.copy()

    exclude = [
        "Ember",
        "(EI)",
        "(Shift)",
        "(BP)",
        "(EIA)",
        "OECD",
        "income",
        "G20",
        "ASEAN",
        "World",
        "Africa",
        "Asia",
        "Europe",
        "North America",
        "South America",
        "Oceania",
    ]

    mask = df["country"].astype(str).apply(
        lambda country: not any(
            keyword.lower() in country.lower()
            for keyword in exclude
        )
    )

    individual = df[mask].copy()

    cols = [
        "renewables_electricity",
        "solar_electricity",
        "wind_electricity",
        "hydro_electricity",
        "nuclear_electricity",
        "low_carbon_electricity",
        "coal_production",
        "gas_production",
        "oil_production",
        "primary_energy_consumption",
    ]

    for col in cols:
        if col not in individual.columns:
            individual[col] = 0

        individual[col] = pd.to_numeric(
            individual[col],
            errors="coerce"
        ).fillna(0)

    trend = individual.groupby("year")[cols].sum().reset_index()
    return trend


def _get_individual_countries(df):
    df = df.copy()

    exclude = [
        "Ember",
        "(EI)",
        "(Shift)",
        "(BP)",
        "(EIA)",
        "OECD",
        "income",
        "G20",
        "ASEAN",
        "World",
        "Africa",
        "Asia",
        "Europe",
        "North America",
        "South America",
        "Oceania",
    ]

    mask = df["country"].astype(str).apply(
        lambda country: not any(
            keyword.lower() in country.lower()
            for keyword in exclude
        )
    )

    countries = sorted(
        df.loc[mask, "country"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    return countries


# ==================================================
# COLOR PALETTE
# ==================================================

COLORS = {
    "renewables": "#1D9E75",
    "solar": "#EF9F27",
    "wind": "#378ADD",
    "hydro": "#534AB7",
    "nuclear": "#D4537E",
    "coal": "#888780",
    "gas": "#D85A30",
    "oil": "#2C2C2A",
}

LAYOUT_DEFAULTS = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(
        family="Arial, sans-serif",
        size=13,
        color="#2C2C2A",
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#D3D1C7",
        borderwidth=0.5,
    ),
    hovermode="x unified",
    margin=dict(l=60, r=30, t=70, b=60),
)


# ==================================================
# LINE CHART
# ==================================================

def function_line(filepath="data/cleaned_data.csv", year_range=None, selected_countries=None):
    df = _load_data(filepath)
    trend = _get_global_trend(df)

    if year_range:
        trend = trend[
            (trend["year"] >= int(year_range[0]))
            & (trend["year"] <= int(year_range[1]))
        ]
    else:
        trend = trend[trend["year"] >= 1990]

    if selected_countries and len(selected_countries) > 0:
        country_df = df[df["country"].isin(selected_countries)].copy()

        if year_range:
            country_df = country_df[
                (country_df["year"] >= int(year_range[0]))
                & (country_df["year"] <= int(year_range[1]))
            ]
        else:
            country_df = country_df[country_df["year"] >= 1990]

        cols = [
            "renewables_electricity",
            "solar_electricity",
            "wind_electricity",
            "hydro_electricity",
            "nuclear_electricity",
        ]

        for col in cols:
            if col not in country_df.columns:
                country_df[col] = 0

            country_df[col] = pd.to_numeric(
                country_df[col],
                errors="coerce"
            ).fillna(0)

        trend = country_df.groupby("year")[cols].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["renewables_electricity"].round(2),
            name="Total Renewables",
            mode="lines",
            line=dict(color=COLORS["renewables"], width=3),
            hovertemplate="%{y:.1f} TWh<extra>Total Renewables</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["solar_electricity"].round(2),
            name="Solar",
            mode="lines",
            line=dict(color=COLORS["solar"], width=2, dash="dot"),
            hovertemplate="%{y:.1f} TWh<extra>Solar</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["wind_electricity"].round(2),
            name="Wind",
            mode="lines",
            line=dict(color=COLORS["wind"], width=2, dash="dash"),
            hovertemplate="%{y:.1f} TWh<extra>Wind</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["hydro_electricity"].round(2),
            name="Hydro",
            mode="lines",
            line=dict(color=COLORS["hydro"], width=2, dash="dashdot"),
            hovertemplate="%{y:.1f} TWh<extra>Hydro</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["nuclear_electricity"].round(2),
            name="Nuclear",
            mode="lines",
            line=dict(color=COLORS["nuclear"], width=2, dash="longdash"),
            hovertemplate="%{y:.1f} TWh<extra>Nuclear</extra>",
        )
    )

    scope_label = (
        f"Selected Countries ({len(selected_countries)})"
        if selected_countries
        else "Global"
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(
            text=f"Global Renewable Energy Trend Over Years — {scope_label}",
            font=dict(size=16, color="#2C2C2A"),
            x=0,
            xanchor="left",
        ),
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=5,
            gridcolor="#F1EFE8",
            linecolor="#D3D1C7",
        ),
        yaxis=dict(
            title="Electricity Generation (TWh)",
            gridcolor="#F1EFE8",
            linecolor="#D3D1C7",
        ),
    )

    return fig


# ==================================================
# AREA CHART
# ==================================================

def function_area(filepath="data/cleaned_data.csv", year_range=None, selected_countries=None):
    df = _load_data(filepath)
    trend = _get_global_trend(df)

    if year_range:
        trend = trend[
            (trend["year"] >= int(year_range[0]))
            & (trend["year"] <= int(year_range[1]))
        ]
    else:
        trend = trend[trend["year"] >= 1990]

    if selected_countries and len(selected_countries) > 0:
        country_df = df[df["country"].isin(selected_countries)].copy()

        if year_range:
            country_df = country_df[
                (country_df["year"] >= int(year_range[0]))
                & (country_df["year"] <= int(year_range[1]))
            ]
        else:
            country_df = country_df[country_df["year"] >= 1990]

        cols = [
            "coal_production",
            "oil_production",
            "gas_production",
            "renewables_electricity",
            "nuclear_electricity",
        ]

        for col in cols:
            if col not in country_df.columns:
                country_df[col] = 0

            country_df[col] = pd.to_numeric(
                country_df[col],
                errors="coerce"
            ).fillna(0)

        trend = country_df.groupby("year")[cols].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["coal_production"].round(2),
            name="Coal",
            mode="lines",
            stackgroup="one",
            fillcolor="rgba(136, 135, 128, 0.7)",
            line=dict(color=COLORS["coal"], width=0.5),
            hovertemplate="%{y:.1f} TWh<extra>Coal</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["oil_production"].round(2),
            name="Oil",
            mode="lines",
            stackgroup="one",
            fillcolor="rgba(44, 44, 42, 0.65)",
            line=dict(color=COLORS["oil"], width=0.5),
            hovertemplate="%{y:.1f} TWh<extra>Oil</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["gas_production"].round(2),
            name="Gas",
            mode="lines",
            stackgroup="one",
            fillcolor="rgba(216, 90, 48, 0.65)",
            line=dict(color=COLORS["gas"], width=0.5),
            hovertemplate="%{y:.1f} TWh<extra>Gas</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["renewables_electricity"].round(2),
            name="Renewables",
            mode="lines",
            stackgroup="one",
            fillcolor="rgba(29, 158, 117, 0.7)",
            line=dict(color=COLORS["renewables"], width=0.5),
            hovertemplate="%{y:.1f} TWh<extra>Renewables</extra>",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=trend["year"],
            y=trend["nuclear_electricity"].round(2),
            name="Nuclear",
            mode="lines",
            stackgroup="one",
            fillcolor="rgba(212, 83, 126, 0.65)",
            line=dict(color=COLORS["nuclear"], width=0.5),
            hovertemplate="%{y:.1f} TWh<extra>Nuclear</extra>",
        )
    )

    scope_label = (
        f"Selected Countries ({len(selected_countries)})"
        if selected_countries
        else "Global"
    )

    fig.update_layout(
        **LAYOUT_DEFAULTS,
        title=dict(
            text=f"Fossil Fuel to Renewable Energy Transition — {scope_label}",
            font=dict(size=16, color="#2C2C2A"),
            x=0,
            xanchor="left",
        ),
        xaxis=dict(
            title="Year",
            tickmode="linear",
            dtick=5,
            gridcolor="#F1EFE8",
            linecolor="#D3D1C7",
        ),
        yaxis=dict(
            title="Energy Production / Generation (TWh)",
            gridcolor="#F1EFE8",
            linecolor="#D3D1C7",
        ),
    )

    return fig


# ==================================================
# FILTERS LAYOUT
# ==================================================

def create_filters_layout(filepath="data/cleaned_data.csv"):
    df = _load_data(filepath)

    countries = _get_individual_countries(df)
    years = sorted(df["year"].dropna().unique())

    if len(years) == 0:
        raise ValueError("No valid years found after loading the dataset.")

    min_year = int(min(years))
    max_year = int(max(years))

    default_start_year = 1990 if min_year <= 1990 <= max_year else min_year

    continents = [
        "Africa",
        "Asia",
        "Europe",
        "North America",
        "South America",
        "Oceania",
    ]

    slider_marks = {
        min_year: {
            "label": str(min_year),
            "style": {
                "fontSize": "10px",
                "whiteSpace": "nowrap",
            },
        },
        max_year: {
            "label": str(max_year),
            "style": {
                "fontSize": "10px",
                "whiteSpace": "nowrap",
            },
        },
    }

    if min_year <= 1990 <= max_year:
        slider_marks[1990] = {
            "label": "1990",
            "style": {
                "fontSize": "10px",
                "whiteSpace": "nowrap",
            },
        }

    slider_marks = dict(sorted(slider_marks.items()))

    label_style = {
        "display": "block",
        "fontSize": "13px",
        "fontWeight": "600",
        "color": "#5F5E5A",
        "marginBottom": "10px",
        "textTransform": "uppercase",
        "letterSpacing": "0.04em",
    }

    filter_card_style = {
        "background": "#FFFFFF",
        "border": "1px solid #D3D1C7",
        "borderRadius": "12px",
        "padding": "16px 18px",
        "marginBottom": "14px",
        "boxShadow": "0 1px 3px rgba(0,0,0,0.05)",
    }

    layout = html.Div(
        id="filters-panel",
        style={
            "width": "100%",
            "fontFamily": "Arial, sans-serif",
        },
        children=[
            html.H3(
                "Dashboard Filters",
                style={
                    "fontSize": "16px",
                    "fontWeight": "600",
                    "color": "#2C2C2A",
                    "marginBottom": "16px",
                    "marginTop": "0",
                },
            ),

            html.Div(
                style=filter_card_style,
                children=[
                    html.Label("Year Range", style=label_style),

                    dcc.RangeSlider(
                        id=Filters.YEAR_SLIDER,
                        min=min_year,
                        max=max_year,
                        step=1,
                        value=[default_start_year, max_year],
                        marks=slider_marks,
                        tooltip={
                            "placement": "bottom",
                            "always_visible": False,
                        },
                        allowCross=False,
                        updatemode="mouseup",
                    ),

                    html.Div(
                        id="year-slider-output",
                        children=f"Selected: {default_start_year} – {max_year}",
                        style={
                            "fontSize": "13px",
                            "color": "#777",
                            "marginTop": "14px",
                            "fontWeight": "500",
                        },
                    ),
                ],
            ),

            html.Div(
                style=filter_card_style,
                children=[
                    html.Label("Select Countries", style=label_style),

                    dcc.Dropdown(
                        id=Filters.COUNTRY_DROPDOWN,
                        options=[
                            {"label": country, "value": country}
                            for country in countries
                        ],
                        value=[],
                        multi=True,
                        placeholder="All countries (global aggregate)",
                        style={"fontSize": "13px"},
                        clearable=True,
                    ),
                ],
            ),

            html.Div(
                style=filter_card_style,
                children=[
                    html.Label("Filter by Continent", style=label_style),

                    dcc.Checklist(
                        id=Filters.CONTINENT_CHECKLIST,
                        options=[
                            {"label": f" {continent}", "value": continent}
                            for continent in continents
                        ],
                        value=continents,
                        inline=False,
                        inputStyle={
                            "marginRight": "8px",
                        },
                        labelStyle={
                            "display": "block",
                            "fontSize": "14px",
                            "color": "#2C2C2A",
                            "marginBottom": "8px",
                            "cursor": "pointer",
                        },
                    ),
                ],
            ),

            html.Div(
                style={
                    "textAlign": "center",
                    "marginTop": "10px",
                    "marginBottom": "20px",
                },
                children=[
                    html.Button(
                        "Reset Filters",
                        id=Filters.RESET_BTN,
                        n_clicks=0,
                        style={
                            "width": "100%",
                            "padding": "10px",
                            "fontSize": "14px",
                            "fontWeight": "600",
                            "cursor": "pointer",
                            "background": "#FFFFFF",
                            "border": "1px solid #D3D1C7",
                            "borderRadius": "10px",
                            "color": "#5F5E5A",
                        },
                    )
                ],
            ),
        ],
    )

    return layout