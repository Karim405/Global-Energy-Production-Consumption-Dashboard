"""
time_filters.py
---------------
Person 4 — Time Series Module + Interactive Filters
Global Energy Production & Consumption Dashboard

Contains:
    - function_line()   : Line Chart  — Global Renewable Energy Trend Over Years
    - function_area()   : Area Chart  — Fossil Fuel vs Renewable Transition Over Time
    - create_filters_layout() : All interactive controls (dropdowns, sliders, etc.)

Filter component IDs (share with Person 5 for callbacks):
    - "country-dropdown"    : Multi-select country dropdown
    - "continent-checklist" : Continent multi-checklist
    - "year-slider"         : Year range slider  (returns [start, end])
    - "energy-source-radio" : Radio items for energy source selection
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dash import dcc, html

# ─────────────────────────────────────────────
# DATA HELPERS  (used internally by this module)
# ─────────────────────────────────────────────

def _load_data(filepath="data/cleaned_data.csv"):
    """Load and prepare the dataset."""
    df = pd.read_csv(filepath)
    df["year"] = pd.to_datetime(df["year"]).dt.year
    return df


def _get_global_trend(df):
    """
    Aggregate individual countries per year to get a global trend.
    Excludes regional aggregates (Ember, EI, Shift, etc.) to avoid double-counting.
    """
    exclude = ["Ember", "(EI)", "(Shift)", "(BP)", "(EIA)", "OECD",
               "income", "G20", "ASEAN", "World", "Africa", "Asia",
               "Europe", "North America", "South America", "Oceania"]
    mask = df["country"].apply(
        lambda c: not any(kw.lower() in c.lower() for kw in exclude)
    )
    individual = df[mask]
    cols = [
        "renewables_electricity", "solar_electricity", "wind_electricity",
        "hydro_electricity", "nuclear_electricity", "low_carbon_electricity",
        "coal_production", "gas_production", "oil_production",
        "primary_energy_consumption",
    ]
    trend = individual.groupby("year")[cols].sum().reset_index()
    return trend


def _get_individual_countries(df):
    """Return list of individual (non-aggregate) countries."""
    exclude = ["Ember", "(EI)", "(Shift)", "(BP)", "(EIA)", "OECD",
               "income", "G20", "ASEAN", "World", "Africa", "Asia",
               "Europe", "North America", "South America", "Oceania"]
    mask = df["country"].apply(
        lambda c: not any(kw.lower() in c.lower() for kw in exclude)
    )
    return sorted(df[mask]["country"].unique().tolist())


# Color palette — consistent across the dashboard
COLORS = {
    "renewables": "#1D9E75",   # teal-400
    "solar":      "#EF9F27",   # amber-400
    "wind":       "#378ADD",   # blue-400
    "hydro":      "#534AB7",   # purple-400
    "nuclear":    "#D4537E",   # pink-400
    "coal":       "#888780",   # gray-400
    "gas":        "#D85A30",   # coral-400
    "oil":        "#2C2C2A",   # gray-900
}

LAYOUT_DEFAULTS = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial, sans-serif", size=13, color="#2C2C2A"),
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


# ─────────────────────────────────────────────
# CHART 1 — LINE CHART
# Global Renewable Energy Trend Over Years
# ─────────────────────────────────────────────

def function_line(filepath="data/cleaned_data.csv", year_range=None, selected_countries=None):
    """
    Line Chart: Global Renewable Energy Trend Over Years.

    Shows the growth of different renewable energy sources (solar, wind, hydro,
    total renewables) from 1990 to 2022 at the global level.

    If selected_countries is provided, aggregates only those countries.
    year_range: [start_year, end_year] — filters the x-axis range.

    Returns:
        plotly.graph_objects.Figure
    """
    df = _load_data(filepath)
    trend = _get_global_trend(df)

    # Apply year filter
    if year_range:
        trend = trend[(trend["year"] >= year_range[0]) & (trend["year"] <= year_range[1])]
    else:
        trend = trend[trend["year"] >= 1990]

    # If specific countries are selected, re-aggregate only those
    if selected_countries and len(selected_countries) > 0:
        country_df = df[df["country"].isin(selected_countries)]
        if year_range:
            country_df = country_df[
                (country_df["year"] >= year_range[0]) &
                (country_df["year"] <= year_range[1])
            ]
        else:
            country_df = country_df[country_df["year"] >= 1990]
        cols = ["renewables_electricity", "solar_electricity",
                "wind_electricity", "hydro_electricity", "nuclear_electricity"]
        trend = country_df.groupby("year")[cols].sum().reset_index()

    fig = go.Figure()

    # Total Renewables — thick main line
    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["renewables_electricity"].round(2),
        name="Total Renewables",
        mode="lines",
        line=dict(color=COLORS["renewables"], width=3),
        hovertemplate="%{y:.1f} TWh<extra>Total Renewables</extra>",
    ))

    # Solar
    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["solar_electricity"].round(2),
        name="Solar",
        mode="lines",
        line=dict(color=COLORS["solar"], width=2, dash="dot"),
        hovertemplate="%{y:.1f} TWh<extra>Solar</extra>",
    ))

    # Wind
    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["wind_electricity"].round(2),
        name="Wind",
        mode="lines",
        line=dict(color=COLORS["wind"], width=2, dash="dash"),
        hovertemplate="%{y:.1f} TWh<extra>Wind</extra>",
    ))

    # Hydro
    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["hydro_electricity"].round(2),
        name="Hydro",
        mode="lines",
        line=dict(color=COLORS["hydro"], width=2, dash="dashdot"),
        hovertemplate="%{y:.1f} TWh<extra>Hydro</extra>",
    ))

    # Nuclear
    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["nuclear_electricity"].round(2),
        name="Nuclear",
        mode="lines",
        line=dict(color=COLORS["nuclear"], width=2, dash="longdash"),
        hovertemplate="%{y:.1f} TWh<extra>Nuclear</extra>",
    ))

    scope_label = (
        f"Selected Countries ({len(selected_countries)})"
        if selected_countries else "Global"
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


# ─────────────────────────────────────────────
# CHART 2 — AREA CHART
# Fossil Fuel to Renewable Transition Over Time
# ─────────────────────────────────────────────

def function_area(filepath="data/cleaned_data.csv", year_range=None, selected_countries=None):
    """
    Area Chart: Fossil Fuel vs Renewable Transition Over Time.

    Stacked area chart showing the composition of energy production over time —
    coal, oil, gas vs renewables + nuclear — visualising the energy transition.

    year_range: [start_year, end_year]
    selected_countries: list of country names to filter (optional)

    Returns:
        plotly.graph_objects.Figure
    """
    df = _load_data(filepath)
    trend = _get_global_trend(df)

    # Apply year filter
    if year_range:
        trend = trend[(trend["year"] >= year_range[0]) & (trend["year"] <= year_range[1])]
    else:
        trend = trend[trend["year"] >= 1990]

    # If specific countries selected, re-aggregate
    if selected_countries and len(selected_countries) > 0:
        country_df = df[df["country"].isin(selected_countries)]
        if year_range:
            country_df = country_df[
                (country_df["year"] >= year_range[0]) &
                (country_df["year"] <= year_range[1])
            ]
        else:
            country_df = country_df[country_df["year"] >= 1990]
        cols = ["coal_production", "oil_production", "gas_production",
                "renewables_electricity", "nuclear_electricity"]
        trend = country_df.groupby("year")[cols].sum().reset_index()

    fig = go.Figure()

    # Fossil fuels — stacked below (warm colors)
    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["coal_production"].round(2),
        name="Coal",
        mode="lines",
        stackgroup="one",
        fillcolor="rgba(136, 135, 128, 0.7)",   # gray
        line=dict(color=COLORS["coal"], width=0.5),
        hovertemplate="%{y:.1f} TWh<extra>Coal</extra>",
    ))

    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["oil_production"].round(2),
        name="Oil",
        mode="lines",
        stackgroup="one",
        fillcolor="rgba(44, 44, 42, 0.65)",     # dark gray
        line=dict(color=COLORS["oil"], width=0.5),
        hovertemplate="%{y:.1f} TWh<extra>Oil</extra>",
    ))

    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["gas_production"].round(2),
        name="Gas",
        mode="lines",
        stackgroup="one",
        fillcolor="rgba(216, 90, 48, 0.65)",    # coral
        line=dict(color=COLORS["gas"], width=0.5),
        hovertemplate="%{y:.1f} TWh<extra>Gas</extra>",
    ))

    # Clean energy — stacked on top (green / teal)
    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["renewables_electricity"].round(2),
        name="Renewables",
        mode="lines",
        stackgroup="one",
        fillcolor="rgba(29, 158, 117, 0.7)",    # teal
        line=dict(color=COLORS["renewables"], width=0.5),
        hovertemplate="%{y:.1f} TWh<extra>Renewables</extra>",
    ))

    fig.add_trace(go.Scatter(
        x=trend["year"],
        y=trend["nuclear_electricity"].round(2),
        name="Nuclear",
        mode="lines",
        stackgroup="one",
        fillcolor="rgba(212, 83, 126, 0.65)",   # pink
        line=dict(color=COLORS["nuclear"], width=0.5),
        hovertemplate="%{y:.1f} TWh<extra>Nuclear</extra>",
    ))

    scope_label = (
        f"Selected Countries ({len(selected_countries)})"
        if selected_countries else "Global"
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


# ─────────────────────────────────────────────
# FILTERS LAYOUT
# create_filters_layout()
# ─────────────────────────────────────────────

def create_filters_layout(filepath="data/cleaned_data.csv"):
    """
    Creates the full interactive filters panel for the dashboard.

    Filter IDs (must match callbacks in callbacks.py — share with Person 5):
        "country-dropdown"    : dcc.Dropdown  (multi=True)
        "continent-checklist" : dcc.Checklist
        "year-slider"         : dcc.RangeSlider  → value = [start_year, end_year]
        "energy-source-radio" : dcc.RadioItems

    Returns:
        dash.html.Div  — the complete filters panel
    """
    df = _load_data(filepath)
    countries = _get_individual_countries(df)
    years = sorted(df["year"].unique())
    min_year, max_year = int(min(years)), int(max(years))

    # Build slider marks (every 10 years + endpoints)
    slider_marks = {
        yr: {"label": str(yr), "style": {"fontSize": "11px"}}
        for yr in range(min_year, max_year + 1, 10)
    }
    slider_marks[max_year] = {"label": str(max_year), "style": {"fontSize": "11px"}}

    CONTINENTS = [
        "Africa", "Asia", "Europe",
        "North America", "South America", "Oceania",
    ]

    ENERGY_SOURCES = [
        {"label": "🌿  Renewables",    "value": "renewables_electricity"},
        {"label": "☀️  Solar",          "value": "solar_electricity"},
        {"label": "💨  Wind",           "value": "wind_electricity"},
        {"label": "💧  Hydro",          "value": "hydro_electricity"},
        {"label": "⚛️  Nuclear",        "value": "nuclear_electricity"},
        {"label": "🏭  Coal",           "value": "coal_production"},
        {"label": "🔥  Gas",            "value": "gas_production"},
        {"label": "🛢️  Oil",            "value": "oil_production"},
        {"label": "⚡  Total Consumption", "value": "primary_energy_consumption"},
    ]

    # ── Shared label style
    label_style = {
        "fontSize": "12px",
        "fontWeight": "500",
        "color": "#5F5E5A",
        "marginBottom": "6px",
        "textTransform": "uppercase",
        "letterSpacing": "0.04em",
    }

    filter_card_style = {
        "background": "white",
        "border": "0.5px solid #D3D1C7",
        "borderRadius": "10px",
        "padding": "14px 16px",
        "marginBottom": "12px",
    }

    layout = html.Div(
        id="filters-panel",
        style={
            "width": "100%",
            "fontFamily": "Arial, sans-serif",
        },
        children=[

            # ── Title
            html.H3(
                "Dashboard Filters",
                style={
                    "fontSize": "15px",
                    "fontWeight": "500",
                    "color": "#2C2C2A",
                    "marginBottom": "16px",
                    "marginTop": "0",
                }
            ),

            # ── 1. Year Range Slider
            html.Div(style=filter_card_style, children=[
                html.P("Year Range", style=label_style),
                dcc.RangeSlider(
                    id="year-slider",
                    min=min_year,
                    max=max_year,
                    step=1,
                    value=[1990, max_year],
                    marks=slider_marks,
                    tooltip={"placement": "bottom", "always_visible": False},
                    allowCross=False,
                ),
                html.Div(
                    id="year-slider-output",
                    style={"fontSize": "12px", "color": "#888780", "marginTop": "8px"},
                ),
            ]),

            # ── 2. Country Dropdown (multi)
            html.Div(style=filter_card_style, children=[
                html.P("Select Countries", style=label_style),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[{"label": c, "value": c} for c in countries],
                    value=[],
                    multi=True,
                    placeholder="All countries (global aggregate)",
                    style={"fontSize": "13px"},
                    clearable=True,
                ),
            ]),

            # ── 3. Continent Checklist
            html.Div(style=filter_card_style, children=[
                html.P("Filter by Continent", style=label_style),
                dcc.Checklist(
                    id="continent-checklist",
                    options=[{"label": f"  {c}", "value": c} for c in CONTINENTS],
                    value=CONTINENTS,          # all selected by default
                    inline=False,
                    inputStyle={"marginRight": "6px"},
                    labelStyle={
                        "display": "block",
                        "fontSize": "13px",
                        "color": "#2C2C2A",
                        "marginBottom": "4px",
                        "cursor": "pointer",
                    },
                ),
            ]),

            # ── 4. Energy Source Radio
            html.Div(style=filter_card_style, children=[
                html.P("Primary Energy Metric", style=label_style),
                dcc.RadioItems(
                    id="energy-source-radio",
                    options=ENERGY_SOURCES,
                    value="renewables_electricity",   # default
                    inputStyle={"marginRight": "6px"},
                    labelStyle={
                        "display": "block",
                        "fontSize": "13px",
                        "color": "#2C2C2A",
                        "marginBottom": "6px",
                        "cursor": "pointer",
                    },
                ),
            ]),

            # ── Reset button
            html.Div(
                html.Button(
                    "Reset Filters",
                    id="reset-filters-btn",
                    n_clicks=0,
                    style={
                        "width": "100%",
                        "padding": "8px",
                        "fontSize": "13px",
                        "cursor": "pointer",
                        "background": "white",
                        "border": "0.5px solid #D3D1C7",
                        "borderRadius": "8px",
                        "color": "#5F5E5A",
                    }
                )
            ),
        ],
    )

    return layout


# ─────────────────────────────────────────────
# QUICK TEST  (run: python time_filters.py)
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import os

    # Resolve data path relative to this file
    base = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base, "data", "cleaned_data.csv")

    print("Testing function_line() ...")
    fig1 = function_line(filepath=data_path)
    print("  Traces:", [t.name for t in fig1.data])
    print("  OK ✓")

    print("Testing function_area() ...")
    fig2 = function_area(filepath=data_path)
    print("  Traces:", [t.name for t in fig2.data])
    print("  OK ✓")

    print("Testing create_filters_layout() ...")
    layout = create_filters_layout(filepath=data_path)
    print("  Component ID:", layout.id)
    print("  OK ✓")

    print("\nAll tests passed!")