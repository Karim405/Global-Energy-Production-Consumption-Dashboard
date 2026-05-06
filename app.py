"""
app.py
======
Global Energy Production & Consumption Dashboard
Main Dash application
"""

import os

import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc

from shared_ids import DATA_PATH, Filters, Graphs, KPI
from time_filters import create_filters_layout, function_line, function_area
from comparison_A import function_chart1, function_chart2, function_chart3
from comparison_B_kpi import (
    function_chart4,
    function_chart5,
    function_chart6,
    get_kpi_values,
)
from relation_distribution import (
    function_scatter,
    function_bubble,
    function_hist,
    function_box,
    function_violin,
)


# ==================================================
# PATHS
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, DATA_PATH)


# ==================================================
# LOAD DATA ONCE
# ==================================================

df_global = pd.read_csv(DATA_FILE)

# Clean column names
df_global.columns = (
    df_global.columns
    .astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
    .str.replace("-", "_", regex=False)
    .str.replace("__", "_", regex=False)
)

# Fix country column if needed
if "country" not in df_global.columns:
    for possible_col in ["entity", "location", "name", "country_name"]:
        if possible_col in df_global.columns:
            df_global = df_global.rename(columns={possible_col: "country"})
            break

if "country" not in df_global.columns:
    raise KeyError("No country column found in dataset.")

# Robust year extraction
if "year" not in df_global.columns:
    raise KeyError("No year column found in dataset.")

year_as_text = df_global["year"].astype(str)
extracted_year = year_as_text.str.extract(r"(\d{4})", expand=False)

df_global["year"] = pd.to_numeric(extracted_year, errors="coerce")
df_global = df_global.dropna(subset=["year"])
df_global["year"] = df_global["year"].astype(int)


# ==================================================
# CONTINENT MAPPING
# ==================================================

CONTINENT_MAP_SIMPLE = {
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
# DASH APP INIT
# ==================================================

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@600;700&display=swap",
    ],
    suppress_callback_exceptions=True,
    title="Global Energy Dashboard",
)

server = app.server


# ==================================================
# DESIGN TOKENS
# ==================================================

NAV_BG = "#0D1117"
SIDEBAR_BG = "#F7F9FC"
ACCENT = "#00D4AA"
TEXT_DARK = "#1A1F2E"
TEXT_MID = "#4A5568"
CARD_BG = "#FFFFFF"
BORDER = "#E2E8F0"

SIDEBAR_WIDTH = "260px"
RIGHT_FILTER_WIDTH = "260px"


# ==================================================
# SHARED COMPONENTS
# ==================================================

def nav_link(label, page_id, icon):
    return html.Div(
        id=f"nav-{page_id}",
        children=[
            html.Span(icon, style={"fontSize": "18px", "marginRight": "10px"}),
            html.Span(label, style={"fontSize": "14px", "fontWeight": "500"}),
        ],
        n_clicks=0,
        style={
            "display": "flex",
            "alignItems": "center",
            "padding": "10px 16px",
            "borderRadius": "8px",
            "cursor": "pointer",
            "color": "#CBD5E0",
            "marginBottom": "4px",
            "transition": "all 0.2s",
            "fontFamily": "'Barlow', sans-serif",
        },
        className="nav-item",
    )


def card(title, children, col_width=12, height=None):
    height_style = {"minHeight": f"{height}px"} if height else {}

    return dbc.Col(
        width=col_width,
        children=[
            html.Div(
                style={
                    "background": CARD_BG,
                    "borderRadius": "12px",
                    "border": f"1px solid {BORDER}",
                    "padding": "20px",
                    "marginBottom": "20px",
                    "boxShadow": "0 1px 3px rgba(0,0,0,0.06)",
                    **height_style,
                },
                children=[
                    html.H6(
                        title,
                        style={
                            "fontFamily": "'Barlow Condensed', sans-serif",
                            "fontWeight": "600",
                            "fontSize": "15px",
                            "color": TEXT_MID,
                            "marginBottom": "16px",
                            "textTransform": "uppercase",
                            "letterSpacing": "0.06em",
                            "borderBottom": f"2px solid {ACCENT}",
                            "paddingBottom": "8px",
                        },
                    ),
                    *children,
                ],
            )
        ],
    )


def kpi_card(icon, label, value_id, color=ACCENT):
    return dbc.Col(
        width=3,
        children=[
            html.Div(
                style={
                    "background": f"linear-gradient(135deg, {color}15, {color}08)",
                    "border": f"1px solid {color}30",
                    "borderRadius": "12px",
                    "padding": "20px",
                    "textAlign": "center",
                    "marginBottom": "20px",
                    "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
                },
                children=[
                    html.Div(icon, style={"fontSize": "32px", "marginBottom": "8px"}),
                    html.Div(
                        id=value_id,
                        style={
                            "fontFamily": "'Barlow Condensed', sans-serif",
                            "fontSize": "26px",
                            "fontWeight": "700",
                            "color": color,
                            "lineHeight": "1",
                        },
                    ),
                    html.Div(
                        label,
                        style={
                            "fontSize": "12px",
                            "color": TEXT_MID,
                            "marginTop": "6px",
                            "fontWeight": "500",
                            "fontFamily": "'Barlow', sans-serif",
                        },
                    ),
                ],
            )
        ],
    )


def section_title(text):
    return html.Div(
        text,
        style={
            "fontFamily": "'Barlow Condensed', sans-serif",
            "fontSize": "22px",
            "fontWeight": "700",
            "color": TEXT_DARK,
            "marginBottom": "16px",
            "borderLeft": f"4px solid {ACCENT}",
            "paddingLeft": "12px",
        },
    )


# ==================================================
# SIDEBAR
# ==================================================

sidebar = html.Div(
    style={
        "width": SIDEBAR_WIDTH,
        "minWidth": SIDEBAR_WIDTH,
        "background": NAV_BG,
        "height": "100vh",
        "position": "fixed",
        "top": 0,
        "left": 0,
        "display": "flex",
        "flexDirection": "column",
        "padding": "0",
        "zIndex": 1000,
        "boxShadow": "2px 0 12px rgba(0,0,0,0.3)",
    },
    children=[
        html.Div(
            style={
                "padding": "24px 20px 20px",
                "borderBottom": "1px solid #1E2A3A",
            },
            children=[
                html.Div("⚡", style={"fontSize": "36px", "marginBottom": "8px"}),
                html.Div(
                    "Global Energy",
                    style={
                        "fontFamily": "'Barlow Condensed', sans-serif",
                        "fontSize": "20px",
                        "fontWeight": "700",
                        "color": ACCENT,
                        "letterSpacing": "0.05em",
                        "lineHeight": "1",
                    },
                ),
                html.Div(
                    "Dashboard",
                    style={
                        "fontFamily": "'Barlow Condensed', sans-serif",
                        "fontSize": "20px",
                        "fontWeight": "700",
                        "color": "#FFFFFF",
                        "letterSpacing": "0.05em",
                    },
                ),
            ],
        ),
        html.Div(
            style={"padding": "16px 12px", "flex": "1"},
            children=[
                html.Div(
                    "ANALYTICS",
                    style={
                        "fontSize": "10px",
                        "fontWeight": "600",
                        "color": "#4A5568",
                        "letterSpacing": "0.1em",
                        "padding": "0 4px",
                        "marginBottom": "8px",
                        "fontFamily": "'Barlow', sans-serif",
                    },
                ),
                nav_link("Overview & KPIs", "overview", "📊"),
                nav_link("Comparison A", "comparison-a", "🏆"),
                nav_link("Comparison B", "comparison-b", "🏭"),
                nav_link("Relationships", "relationships", "🔗"),
                nav_link("Distributions", "distributions", "📈"),
                nav_link("Time Series", "timeseries", "⏳"),
            ],
        ),
        html.Div(
            style={
                "padding": "16px 20px",
                "borderTop": "1px solid #1E2A3A",
            },
            children=[
                html.Div(
                    "Data: Our World in Data",
                    style={
                        "fontSize": "11px",
                        "color": "#4A5568",
                        "fontFamily": "'Barlow', sans-serif",
                    },
                )
            ],
        ),
    ],
)


# ==================================================
# PAGE LAYOUTS
# ==================================================

page_overview = html.Div(
    [
        section_title("Dashboard Overview"),
        html.P(
            "Global energy production and consumption at a glance. Use the filters on the right to explore the data.",
            style={
                "color": TEXT_MID,
                "marginBottom": "24px",
                "fontFamily": "'Barlow', sans-serif",
            },
        ),

        dbc.Row(
            [
                kpi_card("⚡", "Total Energy Consumption (TWh)", KPI.TOTAL_CONSUMPTION, ACCENT),
                kpi_card("🌿", "Avg Renewable Share", KPI.AVG_RENEWABLE_SHARE, "#2ECC71"),
                kpi_card("🏭", "Top Energy Producer", KPI.TOP_PRODUCER, "#E74C3C"),
                kpi_card("🌡️", "Avg Carbon Intensity", KPI.AVG_CARBON_INTENSITY, "#F39C12"),
            ]
        ),

        dbc.Row(
            [
                card(
                    "Global Renewable Energy Trend",
                    [
                        dcc.Graph(
                            id=Graphs.LINE,
                            config={"displayModeBar": False},
                            style={"height": "520px"},
                        )
                    ],
                    col_width=12,
                ),
            ]
        ),

        dbc.Row(
            [
                card(
                    "Fossil vs Renewable by Continent",
                    [
                        dcc.Graph(
                            id=Graphs.CHART4_STACKED_BAR,
                            config={"displayModeBar": False},
                            style={"height": "560px"},
                        )
                    ],
                    col_width=12,
                ),
            ]
        ),
    ]
)


page_comparison_a = html.Div(
    [
        section_title("Comparison A — Energy Leaders"),

        dbc.Row(
            [
                card(
                    "Top 10 Countries by Selected Energy Metric",
                    [
                        dcc.Graph(
                            id=Graphs.CHART1_COLUMN,
                            config={"displayModeBar": False},
                            style={"height": "600px"},
                        )
                    ],
                    col_width=12,
                )
            ]
        ),

        dbc.Row(
            [
                card(
                    "Top 10 Countries by Renewable Energy Share",
                    [
                        dcc.Graph(
                            id=Graphs.CHART2_BAR,
                            config={"displayModeBar": False},
                            style={"height": "650px"},
                        )
                    ],
                    col_width=12,
                )
            ]
        ),

        dbc.Row(
            [
                card(
                    "Energy Mix Composition — Top 5 Countries",
                    [
                        dcc.Graph(
                            id=Graphs.CHART3_STACKED_COL,
                            config={"displayModeBar": False},
                            style={"height": "650px"},
                        )
                    ],
                    col_width=12,
                )
            ]
        ),
    ]
)


page_comparison_b = html.Div(
    [
        section_title("Comparison B — Fossil & Renewable Breakdown"),
        dbc.Row(
            [
                card(
                    "Fossil vs Renewable by Continent",
                    [
                        dcc.Graph(
                            id="graph-chart4-full",
                            config={"displayModeBar": False},
                            style={"height": "560px"},
                        )
                    ],
                    col_width=12,
                )
            ]
        ),
        dbc.Row(
            [
                card(
                    "Oil vs Gas vs Coal — Top 10 Countries",
                    [
                        dcc.Graph(
                            id=Graphs.CHART5_CLUSTERED_COL,
                            config={"displayModeBar": False},
                            style={"height": "590px"},
                        )
                    ],
                    col_width=12,
                ),
            ]
        ),
        dbc.Row(
            [
                card(
                    "Solar vs Wind vs Hydro — Top 10 Countries",
                    [
                        dcc.Graph(
                            id=Graphs.CHART6_CLUSTERED_BAR,
                            config={"displayModeBar": False},
                            style={"height": "590px"},
                        )
                    ],
                    col_width=12,
                ),
            ]
        ),
    ]
)


page_relationships = html.Div(
    [
        section_title("Relationship Charts"),

        dbc.Row(
            [
                card(
                    "GDP vs Energy Consumption",
                    [
                        dcc.Graph(
                            id=Graphs.SCATTER,
                            config={"displayModeBar": False},
                            style={"height": "680px"},
                        )
                    ],
                    col_width=12,
                ),
            ]
        ),

        dbc.Row(
            [
                card(
                    "GDP vs Renewable Share — Bubble Size = Population",
                    [
                        dcc.Graph(
                            id=Graphs.BUBBLE,
                            config={"displayModeBar": False},
                            style={"height": "680px"},
                        )
                    ],
                    col_width=12,
                ),
            ]
        ),
    ]
)


page_distributions = html.Div(
    [
        section_title("Distribution Charts"),
        dbc.Row(
            [
                card(
                    "Per Capita Energy Distribution",
                    [
                        dcc.Graph(
                            id=Graphs.HISTOGRAM,
                            config={"displayModeBar": False},
                            style={"height": "920px"},
                        )
                    ],
                    col_width=12,
                )
            ]
        ),
        dbc.Row(
            [
                card(
                    "Carbon Intensity by Continent",
                    [
                        dcc.Graph(
                            id=Graphs.BOX,
                            config={"displayModeBar": False},
                            style={"height": "920px"},
                        )
                    ],
                    col_width=12,
                ),
            ]
        ),
        dbc.Row(
            [
                card(
                    "Renewable Share Distribution by Region",
                    [
                        dcc.Graph(
                            id=Graphs.VIOLIN,
                            config={"displayModeBar": False},
                            style={"height": "640px"},
                        )
                    ],
                    col_width=12,
                ),
            ]
        ),
    ]
)


page_timeseries = html.Div(
    [
        section_title("Time Series Analysis"),
        dbc.Row(
            [
                card(
                    "Global Renewable Energy Trend Over Years",
                    [
                        dcc.Graph(
                            id="ts-line-full",
                            config={"displayModeBar": False},
                            style={"height": "560px"},
                        )
                    ],
                    col_width=12,
                )
            ]
        ),
        dbc.Row(
            [
                card(
                    "Fossil Fuel to Renewable Transition Over Time",
                    [
                        dcc.Graph(
                            id=Graphs.AREA,
                            config={"displayModeBar": False},
                            style={"height": "560px"},
                        )
                    ],
                    col_width=12,
                )
            ]
        ),
    ]
)


# ==================================================
# ALL PAGES ALWAYS EXIST IN THE LAYOUT
# ==================================================

PAGE_IDS = [
    "overview",
    "comparison-a",
    "comparison-b",
    "relationships",
    "distributions",
    "timeseries",
]

ALL_PAGES_LAYOUT = html.Div(
    [
        html.Div(id="page-overview", children=page_overview, style={"display": "block"}),
        html.Div(id="page-comparison-a", children=page_comparison_a, style={"display": "none"}),
        html.Div(id="page-comparison-b", children=page_comparison_b, style={"display": "none"}),
        html.Div(id="page-relationships", children=page_relationships, style={"display": "none"}),
        html.Div(id="page-distributions", children=page_distributions, style={"display": "none"}),
        html.Div(id="page-timeseries", children=page_timeseries, style={"display": "none"}),
    ]
)


# ==================================================
# FILTERS PANEL
# ==================================================

filters_panel = html.Div(
    style={
        "width": RIGHT_FILTER_WIDTH,
        "minWidth": RIGHT_FILTER_WIDTH,
        "background": SIDEBAR_BG,
        "height": "100vh",
        "position": "fixed",
        "top": 0,
        "right": 0,
        "overflowY": "auto",
        "padding": "20px 16px",
        "borderLeft": f"1px solid {BORDER}",
        "zIndex": 999,
    },
    children=[
        html.Div(
            "⚙️ Filters",
            style={
                "fontFamily": "'Barlow Condensed', sans-serif",
                "fontSize": "18px",
                "fontWeight": "700",
                "color": TEXT_DARK,
                "marginBottom": "16px",
            },
        ),
        create_filters_layout(DATA_FILE),
    ],
)


# ==================================================
# MAIN LAYOUT
# ==================================================

app.layout = html.Div(
    style={
        "background": "#F0F4F8",
        "minHeight": "100vh",
        "fontFamily": "'Barlow', sans-serif",
    },
    children=[
        dcc.Store(id="active-page", data="overview"),
        sidebar,
        filters_panel,
        html.Div(
            id="page-content",
            style={
                "marginLeft": SIDEBAR_WIDTH,
                "marginRight": RIGHT_FILTER_WIDTH,
                "padding": "28px 32px",
                "minHeight": "100vh",
            },
            children=ALL_PAGES_LAYOUT,
        ),
    ],
)


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def _filtered_df(year_range, countries, continents):
    df = df_global.copy()

    if year_range:
        df = df[
            (df["year"] >= int(year_range[0]))
            & (df["year"] <= int(year_range[1]))
        ]

    df["continent"] = df["country"].map(CONTINENT_MAP_SIMPLE)

    if continents:
        df = df[df["continent"].isin(continents)]

    if countries:
        df = df[df["country"].isin(countries)]

    return df


def _selected_year(year_range):
    if year_range:
        return int(year_range[1])
    return int(df_global["year"].max())


# ==================================================
# CALLBACKS
# ==================================================

NAV_IDS = [
    "overview",
    "comparison-a",
    "comparison-b",
    "relationships",
    "distributions",
    "timeseries",
]


@app.callback(
    Output("active-page", "data"),
    [Input(f"nav-{page_id}", "n_clicks") for page_id in NAV_IDS],
    prevent_initial_call=False,
)
def update_active_page(*args):
    ctx = callback_context

    if not ctx.triggered or ctx.triggered[0]["value"] is None:
        return "overview"

    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    return triggered_id.replace("nav-", "")


@app.callback(
    Output("page-overview", "style"),
    Output("page-comparison-a", "style"),
    Output("page-comparison-b", "style"),
    Output("page-relationships", "style"),
    Output("page-distributions", "style"),
    Output("page-timeseries", "style"),
    Input("active-page", "data"),
)
def toggle_pages(active_page):
    styles = []

    for page_id in PAGE_IDS:
        if page_id == active_page:
            styles.append({"display": "block"})
        else:
            styles.append({"display": "none"})

    return styles


@app.callback(
    Output(KPI.TOTAL_CONSUMPTION, "children"),
    Output(KPI.AVG_RENEWABLE_SHARE, "children"),
    Output(KPI.TOP_PRODUCER, "children"),
    Output(KPI.AVG_CARBON_INTENSITY, "children"),
    Input(Filters.YEAR_SLIDER, "value"),
    Input(Filters.COUNTRY_DROPDOWN, "value"),
    Input(Filters.CONTINENT_CHECKLIST, "value"),
)
def update_kpis(year_range, countries, continents):
    df = _filtered_df(year_range, countries, continents)
    kpis = get_kpi_values(df)

    total = float(kpis["total"])
    avg_renew = float(kpis["avg_renew"])
    top_producer = kpis["top_prod"]
    avg_carbon = float(kpis["avg_carbon"])

    if total >= 1_000_000:
        total_text = f"{total / 1_000_000:.2f}M"
    elif total >= 1_000:
        total_text = f"{total / 1_000:.2f}K"
    else:
        total_text = f"{total:.2f}"

    renew_text = f"{avg_renew:.1f}%"
    carbon_text = f"{avg_carbon:.3f}"

    return total_text, renew_text, top_producer, carbon_text


@app.callback(
    Output(Graphs.CHART1_COLUMN, "figure"),
    Output(Graphs.CHART2_BAR, "figure"),
    Output(Graphs.CHART3_STACKED_COL, "figure"),
    Input(Filters.YEAR_SLIDER, "value"),
    Input(Filters.COUNTRY_DROPDOWN, "value"),
    Input(Filters.CONTINENT_CHECKLIST, "value"),
    Input(Filters.ENERGY_SOURCE_RADIO, "value"),
)
def update_comparison_a(year_range, countries, continents, selected_metric):
    df = _filtered_df(year_range, countries, continents)

    fig1 = function_chart1(df, metric_col=selected_metric)
    fig2 = function_chart2(df)
    fig3 = function_chart3(df)

    return fig1, fig2, fig3


@app.callback(
    Output(Graphs.CHART4_STACKED_BAR, "figure"),
    Output("graph-chart4-full", "figure"),
    Output(Graphs.CHART5_CLUSTERED_COL, "figure"),
    Output(Graphs.CHART6_CLUSTERED_BAR, "figure"),
    Input(Filters.YEAR_SLIDER, "value"),
    Input(Filters.COUNTRY_DROPDOWN, "value"),
    Input(Filters.CONTINENT_CHECKLIST, "value"),
)
def update_comparison_b(year_range, countries, continents):
    df = _filtered_df(year_range, countries, continents)

    fig4 = function_chart4(df)
    fig5 = function_chart5(df)
    fig6 = function_chart6(df)

    return fig4, fig4, fig5, fig6


@app.callback(
    Output(Graphs.SCATTER, "figure"),
    Output(Graphs.BUBBLE, "figure"),
    Input(Filters.YEAR_SLIDER, "value"),
    Input(Filters.COUNTRY_DROPDOWN, "value"),
    Input(Filters.CONTINENT_CHECKLIST, "value"),
)
def update_relationships(year_range, countries, continents):
    year = _selected_year(year_range)

    fig_scatter = function_scatter(data_path=DATA_FILE, year=year)
    fig_bubble = function_bubble(data_path=DATA_FILE, year=year)

    return fig_scatter, fig_bubble


@app.callback(
    Output(Graphs.HISTOGRAM, "figure"),
    Output(Graphs.BOX, "figure"),
    Output(Graphs.VIOLIN, "figure"),
    Input(Filters.YEAR_SLIDER, "value"),
    Input(Filters.COUNTRY_DROPDOWN, "value"),
    Input(Filters.CONTINENT_CHECKLIST, "value"),
)
def update_distributions(year_range, countries, continents):
    year = _selected_year(year_range)

    fig_hist = function_hist(data_path=DATA_FILE, year=year)
    fig_box = function_box(data_path=DATA_FILE, year=year)
    fig_violin = function_violin(data_path=DATA_FILE, year=year)

    return fig_hist, fig_box, fig_violin


@app.callback(
    Output(Graphs.LINE, "figure"),
    Output("ts-line-full", "figure"),
    Output(Graphs.AREA, "figure"),
    Input(Filters.YEAR_SLIDER, "value"),
    Input(Filters.COUNTRY_DROPDOWN, "value"),
    Input(Filters.CONTINENT_CHECKLIST, "value"),
)
def update_timeseries(year_range, countries, continents):
    selected_countries = countries if countries else None

    fig_line = function_line(
        filepath=DATA_FILE,
        year_range=year_range,
        selected_countries=selected_countries,
    )

    fig_area = function_area(
        filepath=DATA_FILE,
        year_range=year_range,
        selected_countries=selected_countries,
    )

    return fig_line, fig_line, fig_area


@app.callback(
    Output(Filters.COUNTRY_DROPDOWN, "value"),
    Output(Filters.CONTINENT_CHECKLIST, "value"),
    Output(Filters.YEAR_SLIDER, "value"),
    Output(Filters.ENERGY_SOURCE_RADIO, "value"),
    Input(Filters.RESET_BTN, "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(n_clicks):
    min_year = int(df_global["year"].min())
    max_year = int(df_global["year"].max())

    continents = [
        "Africa",
        "Asia",
        "Europe",
        "North America",
        "South America",
        "Oceania",
    ]

    return [], continents, [min_year, max_year], "primary_energy_consumption"


@app.callback(
    Output("year-slider-output", "children"),
    Input(Filters.YEAR_SLIDER, "value"),
)
def update_year_label(value):
    if value:
        return f"Selected: {value[0]} – {value[1]}"
    return ""


# ==================================================
# CUSTOM CSS
# ==================================================

app.index_string = """
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>Global Energy Dashboard</title>
    {%favicon%}
    {%css%}
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background: #F0F4F8;
        }

        .nav-item:hover {
            background: rgba(0, 212, 170, 0.1) !important;
            color: #00D4AA !important;
        }

        .nav-item:hover span {
            color: #00D4AA !important;
        }

        ::-webkit-scrollbar {
            width: 6px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }

        ::-webkit-scrollbar-thumb {
            background: #CBD5E0;
            border-radius: 3px;
        }

        .rc-slider-track {
            background-color: #00D4AA !important;
        }

        .rc-slider-handle {
            border-color: #00D4AA !important;
        }

        .Select-control {
            border-color: #E2E8F0 !important;
        }

        .Select-control:focus {
            border-color: #00D4AA !important;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
"""


# ==================================================
# RUN APP
# ==================================================

if __name__ == "__main__":
    app.run(debug=True, port=8050)