"""
Relationship & Distribution Module
Global Energy Production project

Required charts:
1) function_scatter()  -> GDP vs Energy Consumption
2) function_bubble()   -> GDP vs Renewable Share, bubble size = population
3) function_hist()     -> Distribution of Per Capita Energy Use
4) function_box()      -> Carbon Intensity by Continent
5) function_violin()   -> Renewable Share Distribution by Region
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


DATA_FILE_NAME = "cleaned_data.csv"

BLACK = "#000000"
GRID = "#d0d0d0"
LIGHT_BLUE = "#bfe3ff"
BLUE_2 = "#8ec9f5"
BLUE_3 = "#5aaee8"
BLUE_4 = "#2f8fce"
BLUE_5 = "#1267a8"
BLUE_SCALE = [LIGHT_BLUE, BLUE_2, BLUE_3, BLUE_4, BLUE_5]
LIGHT_ORANGE = "#ffd69b"
LIGHT_GREEN = "#b7e3a8"
WHITE = "#ffffff"


AGGREGATE_NAMES = {
    "africa",
    "asia",
    "asia pacific",
    "asean",
    "cis",
    "europe",
    "european union",
    "g20",
    "g7",
    "high-income countries",
    "latin america and caribbean",
    "low-income countries",
    "lower-middle-income countries",
    "middle east",
    "non-oecd",
    "non-opec",
    "north america",
    "oecd",
    "opec",
    "oceania",
    "south america",
    "south and central america",
    "upper-middle-income countries",
    "world",
}

AGGREGATE_MARKERS = (
    " (ei)",
    " (eia)",
    " (ember)",
    " (shift)",
    "ieo ",
    "oecd -",
    "opec -",
    "other non-oecd",
)


CONTINENT_MAP = {
    # Africa
    "Algeria": "Africa",
    "Angola": "Africa",
    "Burundi": "Africa",
    "Chad": "Africa",
    "Congo": "Africa",
    "Egypt": "Africa",
    "Equatorial Guinea": "Africa",
    "Gabon": "Africa",
    "Kenya": "Africa",
    "Libya": "Africa",
    "Morocco": "Africa",
    "Nigeria": "Africa",
    "South Africa": "Africa",
    "South Sudan": "Africa",
    "Sudan": "Africa",
    "Tunisia": "Africa",
    "Zimbabwe": "Africa",

    # Americas
    "Argentina": "Americas",
    "Bolivia": "Americas",
    "Brazil": "Americas",
    "Canada": "Americas",
    "Chile": "Americas",
    "Colombia": "Americas",
    "Costa Rica": "Americas",
    "Ecuador": "Americas",
    "El Salvador": "Americas",
    "Mexico": "Americas",
    "Peru": "Americas",
    "Trinidad and Tobago": "Americas",
    "United States": "Americas",
    "Uruguay": "Americas",
    "Venezuela": "Americas",

    # Asia
    "Azerbaijan": "Asia",
    "Bahrain": "Asia",
    "Bangladesh": "Asia",
    "Brunei": "Asia",
    "China": "Asia",
    "Georgia": "Asia",
    "Hong Kong": "Asia",
    "India": "Asia",
    "Indonesia": "Asia",
    "Iran": "Asia",
    "Iraq": "Asia",
    "Israel": "Asia",
    "Japan": "Asia",
    "Kazakhstan": "Asia",
    "Kuwait": "Asia",
    "Malaysia": "Asia",
    "Mongolia": "Asia",
    "Myanmar": "Asia",
    "Oman": "Asia",
    "Pakistan": "Asia",
    "Philippines": "Asia",
    "Qatar": "Asia",
    "Russia": "Asia",
    "Saudi Arabia": "Asia",
    "Singapore": "Asia",
    "South Korea": "Asia",
    "Sri Lanka": "Asia",
    "Syria": "Asia",
    "Taiwan": "Asia",
    "Thailand": "Asia",
    "Turkey": "Asia",
    "Turkmenistan": "Asia",
    "United Arab Emirates": "Asia",
    "Uzbekistan": "Asia",
    "Vietnam": "Asia",
    "Yemen": "Asia",

    # Europe
    "Austria": "Europe",
    "Belarus": "Europe",
    "Belgium": "Europe",
    "Bosnia and Herzegovina": "Europe",
    "Bulgaria": "Europe",
    "Croatia": "Europe",
    "Cyprus": "Europe",
    "Czechia": "Europe",
    "Denmark": "Europe",
    "Estonia": "Europe",
    "Finland": "Europe",
    "France": "Europe",
    "Germany": "Europe",
    "Greece": "Europe",
    "Hungary": "Europe",
    "Iceland": "Europe",
    "Ireland": "Europe",
    "Italy": "Europe",
    "Kosovo": "Europe",
    "Latvia": "Europe",
    "Lithuania": "Europe",
    "Luxembourg": "Europe",
    "Malta": "Europe",
    "Moldova": "Europe",
    "Montenegro": "Europe",
    "North Macedonia": "Europe",
    "Norway": "Europe",
    "Poland": "Europe",
    "Portugal": "Europe",
    "Romania": "Europe",
    "Serbia": "Europe",
    "Slovakia": "Europe",
    "Slovenia": "Europe",
    "Spain": "Europe",
    "Sweden": "Europe",
    "Switzerland": "Europe",
    "Ukraine": "Europe",
    "United Kingdom": "Europe",

    # Oceania
    "Australia": "Oceania",
    "New Zealand": "Oceania",
}


REGION_MAP = {
    "Canada": "North America",
    "United States": "North America",

    "Argentina": "Latin America",
    "Bolivia": "Latin America",
    "Brazil": "Latin America",
    "Chile": "Latin America",
    "Colombia": "Latin America",
    "Costa Rica": "Latin America",
    "Ecuador": "Latin America",
    "El Salvador": "Latin America",
    "Mexico": "Latin America",
    "Peru": "Latin America",
    "Trinidad and Tobago": "Latin America",
    "Uruguay": "Latin America",
    "Venezuela": "Latin America",

    "Algeria": "Middle East & North Africa",
    "Bahrain": "Middle East & North Africa",
    "Egypt": "Middle East & North Africa",
    "Iran": "Middle East & North Africa",
    "Iraq": "Middle East & North Africa",
    "Israel": "Middle East & North Africa",
    "Kuwait": "Middle East & North Africa",
    "Libya": "Middle East & North Africa",
    "Morocco": "Middle East & North Africa",
    "Oman": "Middle East & North Africa",
    "Qatar": "Middle East & North Africa",
    "Saudi Arabia": "Middle East & North Africa",
    "Syria": "Middle East & North Africa",
    "Tunisia": "Middle East & North Africa",
    "Turkey": "Middle East & North Africa",
    "United Arab Emirates": "Middle East & North Africa",
    "Yemen": "Middle East & North Africa",

    "Angola": "Sub-Saharan Africa",
    "Burundi": "Sub-Saharan Africa",
    "Chad": "Sub-Saharan Africa",
    "Congo": "Sub-Saharan Africa",
    "Equatorial Guinea": "Sub-Saharan Africa",
    "Gabon": "Sub-Saharan Africa",
    "Kenya": "Sub-Saharan Africa",
    "Nigeria": "Sub-Saharan Africa",
    "South Africa": "Sub-Saharan Africa",
    "South Sudan": "Sub-Saharan Africa",
    "Sudan": "Sub-Saharan Africa",
    "Zimbabwe": "Sub-Saharan Africa",

    "Bangladesh": "South Asia",
    "India": "South Asia",
    "Pakistan": "South Asia",
    "Sri Lanka": "South Asia",

    "Azerbaijan": "Central Asia",
    "Georgia": "Central Asia",
    "Kazakhstan": "Central Asia",
    "Russia": "Central Asia",
    "Turkmenistan": "Central Asia",
    "Uzbekistan": "Central Asia",

    "Australia": "East Asia & Pacific",
    "Brunei": "East Asia & Pacific",
    "China": "East Asia & Pacific",
    "Hong Kong": "East Asia & Pacific",
    "Indonesia": "East Asia & Pacific",
    "Japan": "East Asia & Pacific",
    "Malaysia": "East Asia & Pacific",
    "Mongolia": "East Asia & Pacific",
    "Myanmar": "East Asia & Pacific",
    "New Zealand": "East Asia & Pacific",
    "Philippines": "East Asia & Pacific",
    "Singapore": "East Asia & Pacific",
    "South Korea": "East Asia & Pacific",
    "Taiwan": "East Asia & Pacific",
    "Thailand": "East Asia & Pacific",
    "Vietnam": "East Asia & Pacific",
}

EUROPEAN_COUNTRIES = {
    country for country, continent in CONTINENT_MAP.items() if continent == "Europe"
}
REGION_MAP.update({country: "Europe" for country in EUROPEAN_COUNTRIES})

REGION_LABELS = {
    "East Asia & Pacific": "East Asia<br>& Pacific",
    "Latin America": "Latin<br>America",
    "Middle East & North Africa": "Middle East<br>& North Africa",
    "North America": "North<br>America",
    "Sub-Saharan Africa": "Sub-Saharan<br>Africa",
}


def _plotly():
    try:
        import plotly.express as px
        import plotly.graph_objects as go
    except ImportError as exc:
        raise ImportError(
            "Plotly is required to draw these charts. Install it with: pip install plotly"
        ) from exc
    return px, go


def _resolve_data_path(data_path: str | Path | None = None) -> Path:
    if data_path is not None:
        path = Path(data_path)
        if not path.exists():
            raise FileNotFoundError(f"Could not find data file: {path}")
        return path

    possible_paths = [
        Path.cwd() / DATA_FILE_NAME,
        Path(__file__).resolve().with_name(DATA_FILE_NAME),
        Path.home() / "Downloads" / DATA_FILE_NAME,
    ]

    for path in possible_paths:
        if path.exists():
            return path

    raise FileNotFoundError(
        f"Could not find {DATA_FILE_NAME}. Put it beside this file or in Downloads."
    )


def _is_aggregate(country: object) -> bool:
    name = str(country).strip().lower()
    return name in AGGREGATE_NAMES or any(marker in name for marker in AGGREGATE_MARKERS)


def _continent(country: object) -> str:
    name = str(country).strip()
    return CONTINENT_MAP.get(name, "Other")


def _region(country: object) -> str:
    name = str(country).strip()
    return REGION_MAP.get(name, "Other")


def _required_columns(df: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))


def _prepare_data(
    data_path: str | Path | None = None,
    year: int | None = None,
    include_aggregates: bool = False,
) -> tuple[pd.DataFrame, int]:
    df = pd.read_csv(_resolve_data_path(data_path))

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

    required = [
        "country",
        "year",
        "population",
        "gdp",
        "coal_production",
        "gas_production",
        "oil_production",
        "low_carbon_electricity",
        "electricity_generation",
        "primary_energy_consumption",
        "renewables_electricity",
    ]

    _required_columns(df, required)

    df["year_number"] = pd.to_numeric(
        df["year"].astype(str).str.extract(r"(\d{4})", expand=False),
        errors="coerce",
    )

    selected_year = int(df["year_number"].max() if year is None else year)
    df = df[df["year_number"].eq(selected_year)].copy()

    if not include_aggregates:
        df = df[~df["country"].map(_is_aggregate)].copy()

    number_cols = [
        "population",
        "gdp",
        "coal_production",
        "gas_production",
        "oil_production",
        "low_carbon_electricity",
        "electricity_generation",
        "primary_energy_consumption",
        "renewables_electricity",
    ]

    for col in number_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").clip(lower=0)

    df = df.dropna(subset=["country", *number_cols])

    df["continent"] = df["country"].map(_continent)
    df["region"] = df["country"].map(_region)
    df["region_label"] = df["region"].map(REGION_LABELS).fillna(df["region"])

    fossil = df["coal_production"] + df["gas_production"] + df["oil_production"]
    total_mix = fossil + df["low_carbon_electricity"]

    df["renewable_share"] = (
        df["renewables_electricity"]
        / df["electricity_generation"].replace(0, np.nan)
        * 100
    ).clip(0, 100)

    df["per_capita_energy"] = (
        df["primary_energy_consumption"]
        / df["population"].replace(0, np.nan)
        * 100
    )

    df["carbon_intensity"] = (
        fossil / total_mix.replace(0, np.nan) * 100
    ).clip(0, 100)

    df["population_size"] = np.expm1(df["population"].clip(upper=22))
    df = df.replace([np.inf, -np.inf], np.nan)

    return df, selected_year


def _zero_range(values: pd.Series, top_padding: float = 0.12) -> list[float]:
    clean = pd.to_numeric(values, errors="coerce").dropna()

    if clean.empty or clean.max() <= 0:
        return [0, 1]

    return [0, float(clean.max()) * (1 + top_padding)]


def _guideline_layout(
    fig,
    title: str,
    x_title: str,
    y_title: str,
    x_values: pd.Series | None = None,
    y_values: pd.Series | None = None,
    height: int = 640,
):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor=WHITE,
        plot_bgcolor=WHITE,
        showlegend=True,

        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(size=22, color=BLACK),
        ),

        xaxis_title=x_title,
        yaxis_title=y_title,
        height=height,

        margin=dict(l=95, r=260, t=95, b=85),

        font=dict(
            color=BLACK,
            size=13,
            family="Arial, sans-serif",
        ),

        legend=dict(
            title="Legend",
            orientation="v",
            x=1.02,
            y=1,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.96)",
            bordercolor=BLACK,
            borderwidth=1,
            font=dict(size=12, color=BLACK),
        ),

        hoverlabel=dict(
            bgcolor=WHITE,
            font_size=13,
            font_color=BLACK,
            bordercolor=BLACK,
        ),
    )

    fig.update_xaxes(
        showline=True,
        linewidth=1.5,
        linecolor=BLACK,
        mirror=True,
        showgrid=True,
        gridcolor="rgba(0,0,0,0.16)",
        griddash="dot",
        zeroline=True,
        zerolinecolor=BLACK,
        tickangle=0,
        ticks="outside",
        title_font=dict(size=15, color=BLACK),
        tickfont=dict(size=12, color=BLACK),
        automargin=True,
    )

    fig.update_yaxes(
        showline=True,
        linewidth=1.5,
        linecolor=BLACK,
        mirror=True,
        showgrid=True,
        gridcolor="rgba(0,0,0,0.16)",
        griddash="dot",
        zeroline=True,
        zerolinecolor=BLACK,
        ticks="outside",
        title_font=dict(size=15, color=BLACK),
        tickfont=dict(size=12, color=BLACK),
        automargin=True,
    )

    if x_values is not None:
        fig.update_xaxes(range=_zero_range(x_values, top_padding=0.16))
    else:
        fig.update_xaxes(rangemode="tozero")

    if y_values is not None:
        fig.update_yaxes(range=_zero_range(y_values, top_padding=0.18))
    else:
        fig.update_yaxes(rangemode="tozero")

    return fig


def _label_box_medians(
    fig,
    df: pd.DataFrame,
    category: str,
    value: str,
    row: int | None = None,
    col: int | None = None,
) -> None:
    _, go = _plotly()

    medians = df.groupby(category, observed=True)[value].median().reset_index()

    trace = go.Scatter(
        x=medians[category],
        y=medians[value],
        mode="markers+text",
        marker=dict(color=WHITE, size=9, line=dict(color=BLACK, width=1.5)),
        text=medians[value].map(lambda v: f"{v:.1f}"),
        textposition="middle right",
        textfont=dict(color=BLACK, size=10),
        name="Median",
        showlegend=True,
        hoverinfo="skip",
    )

    if row is None or col is None:
        fig.add_trace(trace)
    else:
        fig.add_trace(trace, row=row, col=col)


def _label_high_outliers(
    fig,
    df: pd.DataFrame,
    category: str,
    value: str,
    row: int | None = None,
    col: int | None = None,
) -> None:
    _, go = _plotly()

    outlier_rows = []

    for _, group in df.groupby(category, observed=True):
        q1 = group[value].quantile(0.25)
        q3 = group[value].quantile(0.75)
        iqr = q3 - q1
        upper_fence = q3 + 1.5 * iqr

        outliers = group[group[value].gt(upper_fence)]

        if outliers.empty:
            outliers = group.nlargest(1, value)

        outlier_rows.append(outliers.nlargest(1, value).iloc[0])

    outliers_df = pd.DataFrame(outlier_rows)

    trace = go.Scatter(
        x=outliers_df[category],
        y=outliers_df[value],
        mode="markers+text",
        marker=dict(color=LIGHT_GREEN, size=8, line=dict(color=BLACK, width=1)),
        text=outliers_df.apply(lambda item: f"{item['country']}: {item[value]:.1f}", axis=1),
        textposition="top right",
        textfont=dict(color=BLACK, size=9),
        name="Outlier",
        showlegend=True,
        hoverinfo="skip",
    )

    if row is None or col is None:
        fig.add_trace(trace)
    else:
        fig.add_trace(trace, row=row, col=col)


def _values_text(values: pd.Series, max_items: int = 10) -> str:
    rounded = [f"{value:.1f}" for value in sorted(values.dropna().tolist())]

    if len(rounded) <= max_items:
        return ", ".join(rounded)

    return ", ".join(rounded[:max_items]) + f", ... (+{len(rounded) - max_items} more)"


def _histogram_bins(values: pd.Series, bin_count: int = 8) -> pd.DataFrame:
    values = pd.to_numeric(values, errors="coerce").dropna()
    values = values[values > 0].sort_values()

    if values.empty:
        raise ValueError("No positive per-capita energy values are available for histogram.")

    if values.min() == values.max():
        edges = np.array([values.min() - 0.5, values.max() + 0.5])
    else:
        edges = np.linspace(values.min(), values.max(), bin_count + 1)

    rows = []

    for index in range(len(edges) - 1):
        start = float(edges[index])
        end = float(edges[index + 1])

        if index == len(edges) - 2:
            included = values[(values >= start) & (values <= end)]
            interval = f"[{start:.1f}, {end:.1f}]"
        else:
            included = values[(values >= start) & (values < end)]
            interval = f"[{start:.1f}, {end:.1f})"

        rows.append(
            {
                "bin": f"Bin {index + 1}",
                "interval": interval,
                "values": _values_text(included),
                "count": int(included.count()),
                "center": (start + end) / 2,
                "width": end - start,
            }
        )

    return pd.DataFrame(rows)


def _box_statistics(df: pd.DataFrame, category: str, value: str) -> pd.DataFrame:
    rows = []

    for name, group in df.groupby(category, observed=True):
        clean = group.dropna(subset=[value]).copy()
        values = clean[value]

        q1 = values.quantile(0.25)
        median = values.median()
        q3 = values.quantile(0.75)
        iqr = q3 - q1

        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr

        inliers = clean[clean[value].between(lower_fence, upper_fence)]
        outliers = clean[~clean[value].between(lower_fence, upper_fence)]

        outlier_text = "None"

        if not outliers.empty:
            outlier_text = "; ".join(
                f"{item.country} {getattr(item, value):.1f}"
                for item in outliers.nlargest(3, value).itertuples()
            )

        rows.append(
            {
                "Group": name,
                "Min Whisker": inliers[value].min(),
                "Q1": q1,
                "Median": median,
                "Q3": q3,
                "Max Whisker": inliers[value].max(),
                "IQR": iqr,
                "Outliers": outlier_text,
            }
        )

    stats = pd.DataFrame(rows)
    return stats.sort_values("Median", ascending=False)


# ==================================================
# 1) SCATTER PLOT
# ==================================================

def function_scatter(
    data_path: str | Path | None = None,
    year: int | None = None,
    include_aggregates: bool = False,
):
    """
    Scatter Plot:
    GDP vs Energy Consumption.
    """
    _, go = _plotly()

    df, selected_year = _prepare_data(data_path, year, include_aggregates)

    plot_df = df.dropna(subset=["gdp", "primary_energy_consumption"]).copy()

    plot_df = plot_df[
        (plot_df["gdp"] > 0)
        & (plot_df["primary_energy_consumption"] > 0)
    ].copy()

    if plot_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="GDP vs Energy Consumption — No Data",
            template="plotly_white",
            height=640,
        )
        return fig

    top_outliers = (
        plot_df.sort_values("primary_energy_consumption", ascending=False)
        .head(5)
        .copy()
    )

    normal_df = plot_df.drop(index=top_outliers.index)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=normal_df["gdp"],
            y=normal_df["primary_energy_consumption"],
            mode="markers",
            marker=dict(
                color=LIGHT_BLUE,
                size=12,
                opacity=0.85,
                line=dict(color=BLACK, width=1),
            ),
            name="Standard Countries",
            customdata=normal_df[["country", "continent"]],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Continent: %{customdata[1]}<br>"
                "GDP: %{x:.2f}<br>"
                "Energy Consumption: %{y:.2f} TWh"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=top_outliers["gdp"],
            y=top_outliers["primary_energy_consumption"],
            mode="markers+text",
            marker=dict(
                color=LIGHT_ORANGE,
                size=17,
                opacity=0.95,
                line=dict(color=BLACK, width=1.4),
            ),
            text=top_outliers["country"],
            textposition="top center",
            textfont=dict(color=BLACK, size=11),
            name="Top Energy Consumers",
            customdata=top_outliers[["country", "continent"]],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Continent: %{customdata[1]}<br>"
                "GDP: %{x:.2f}<br>"
                "Energy Consumption: %{y:.2f} TWh"
                "<extra></extra>"
            ),
        )
    )

    fig = _guideline_layout(
        fig,
        title=f"GDP vs Energy Consumption ({selected_year})",
        x_title="GDP",
        y_title="Energy Consumption (TWh)",
        x_values=plot_df["gdp"],
        y_values=plot_df["primary_energy_consumption"],
        height=660,
    )

    fig.update_layout(
        annotations=[
            dict(
                text="Shows whether countries with higher GDP also tend to consume more energy.",
                x=0,
                y=1.08,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=13, color="#555"),
                align="left",
            )
        ]
    )

    return fig


# ==================================================
# 2) BUBBLE PLOT
# ==================================================

def function_bubble(
    data_path: str | Path | None = None,
    year: int | None = None,
    include_aggregates: bool = False,
):
    """
    Bubble Plot:
    GDP vs Renewable Share.
    Bubble size represents population.
    """
    _, go = _plotly()

    df, selected_year = _prepare_data(data_path, year, include_aggregates)

    plot_df = df.dropna(
        subset=["gdp", "renewable_share", "population_size", "population"]
    ).copy()

    plot_df = plot_df[
        (plot_df["gdp"] > 0)
        & (plot_df["population_size"] > 0)
        & (plot_df["renewable_share"] >= 0)
    ].copy()

    if plot_df.empty:
        fig = go.Figure()
        fig.update_layout(
            title="GDP vs Renewable Share — No Data",
            template="plotly_white",
            height=640,
        )
        return fig

    top_population = (
        plot_df.sort_values("population", ascending=False)
        .head(5)
        .copy()
    )

    normal_df = plot_df.drop(index=top_population.index)

    max_population_size = plot_df["population_size"].max()

    normal_sizes = (
        normal_df["population_size"] / max_population_size * 38 + 9
    )

    outlier_sizes = (
        top_population["population_size"] / max_population_size * 52 + 12
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=normal_df["gdp"],
            y=normal_df["renewable_share"],
            mode="markers",
            marker=dict(
                color=LIGHT_BLUE,
                size=normal_sizes,
                opacity=0.72,
                line=dict(color=BLACK, width=1),
                sizemode="diameter",
            ),
            name="Standard Countries",
            customdata=normal_df[["country", "continent", "population"]],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Continent: %{customdata[1]}<br>"
                "GDP: %{x:.2f}<br>"
                "Renewable Share: %{y:.1f}%<br>"
                "Population: %{customdata[2]:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=top_population["gdp"],
            y=top_population["renewable_share"],
            mode="markers+text",
            marker=dict(
                color=LIGHT_ORANGE,
                size=outlier_sizes,
                opacity=0.88,
                line=dict(color=BLACK, width=1.4),
                sizemode="diameter",
            ),
            text=top_population["country"],
            textposition="top center",
            textfont=dict(color=BLACK, size=11),
            name="Largest Population",
            customdata=top_population[["country", "continent", "population"]],
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Continent: %{customdata[1]}<br>"
                "GDP: %{x:.2f}<br>"
                "Renewable Share: %{y:.1f}%<br>"
                "Population: %{customdata[2]:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    fig = _guideline_layout(
        fig,
        title=f"GDP vs Renewable Share ({selected_year})",
        x_title="GDP",
        y_title="Renewable Share (%)",
        x_values=plot_df["gdp"],
        y_values=pd.Series([100]),
        height=660,
    )

    fig.update_yaxes(range=[0, 105])

    fig.update_layout(
        annotations=[
            dict(
                text="Bubble size represents population. Larger bubbles indicate more populated countries.",
                x=0,
                y=1.08,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=13, color="#555"),
                align="left",
            )
        ]
    )

    return fig


# ==================================================
# 3) HISTOGRAM
# ==================================================

def function_hist(
    data_path: str | Path | None = None,
    year: int | None = None,
    include_aggregates: bool = False,
):
    """
    Histogram:
    Distribution of Per Capita Energy Use.
    """
    _, go = _plotly()
    from plotly.subplots import make_subplots

    df, selected_year = _prepare_data(data_path, year, include_aggregates)

    plot_df = df.dropna(subset=["per_capita_energy"]).copy()
    plot_df = plot_df[plot_df["per_capita_energy"] > 0]

    bin_table = _histogram_bins(plot_df["per_capita_energy"], bin_count=8)

    fig = make_subplots(
        rows=2,
        cols=1,
        specs=[[{"type": "table"}], [{"type": "xy"}]],
        row_heights=[0.34, 0.66],
        vertical_spacing=0.16,
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=[
                    "<b>Bin Number</b>",
                    "<b>Interval [Start, End)</b>",
                    "<b>Values Included</b>",
                    "<b>Count (Frequency)</b>",
                ],
                fill_color="#f7eaea",
                line_color=BLACK,
                align="left",
                font=dict(color=BLACK, size=12),
                height=28,
            ),
            cells=dict(
                values=[
                    bin_table["bin"],
                    bin_table["interval"],
                    bin_table["values"],
                    bin_table["count"],
                ],
                fill_color=WHITE,
                line_color=BLACK,
                align=["left", "left", "left", "center"],
                font=dict(color=BLACK, size=11),
                height=26,
            ),
            columnwidth=[0.16, 0.22, 0.46, 0.16],
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            x=bin_table["center"],
            y=bin_table["count"],
            width=bin_table["width"],
            marker=dict(color=LIGHT_BLUE, line=dict(color=BLACK, width=1)),
            text=bin_table["count"],
            textposition="outside",
            cliponaxis=False,
            name=f"Country Frequency (n={len(plot_df)})",
            showlegend=True,
            hovertemplate="Interval: %{customdata}<br>Countries: %{y}<extra></extra>",
            customdata=bin_table["interval"],
        ),
        row=2,
        col=1,
    )

    fig = _guideline_layout(
        fig,
        title=f"Distribution of Per Capita Energy Use ({selected_year})",
        x_title="Per Capita Energy Use",
        y_title="Frequency (Country Count)",
        x_values=plot_df["per_capita_energy"],
        y_values=bin_table["count"],
        height=960,
    )

    fig.update_layout(
        legend=dict(
            title="Legend",
            x=0.96,
            y=0.53,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor=GRID,
            borderwidth=1,
            font=dict(size=10),
        )
    )

    tick_values = [bin_table["center"].iloc[0] - bin_table["width"].iloc[0] / 2]
    tick_values += (bin_table["center"] + bin_table["width"] / 2).round(1).tolist()

    fig.update_xaxes(
        range=[tick_values[0], tick_values[-1]],
        tickmode="array",
        tickvals=tick_values,
        row=2,
        col=1,
    )

    return fig


# ==================================================
# 4) BOX PLOT
# ==================================================

def function_box(
    data_path: str | Path | None = None,
    year: int | None = None,
    include_aggregates: bool = False,
):
    """
    Box Plot:
    Carbon Intensity by Continent.
    """
    _, go = _plotly()
    from plotly.subplots import make_subplots

    df, selected_year = _prepare_data(data_path, year, include_aggregates)

    plot_df = df.dropna(subset=["continent", "carbon_intensity"]).copy()
    plot_df = plot_df[plot_df["continent"] != "Other"]

    stats_table = _box_statistics(plot_df, "continent", "carbon_intensity")

    continent_order = (
        plot_df.groupby("continent", observed=True)["carbon_intensity"]
        .median()
        .sort_values(ascending=False)
        .index
        .tolist()
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        specs=[[{"type": "table"}], [{"type": "xy"}]],
        row_heights=[0.34, 0.66],
        vertical_spacing=0.16,
    )

    fig.add_trace(
        go.Table(
            header=dict(
                values=[
                    "<b>Continent</b>",
                    "<b>Min Whisker</b>",
                    "<b>Q1</b>",
                    "<b>Median</b>",
                    "<b>Q3</b>",
                    "<b>Max Whisker</b>",
                    "<b>IQR</b>",
                    "<b>Outliers</b>",
                ],
                fill_color="#ead6c6",
                line_color=BLACK,
                align="center",
                font=dict(color=BLACK, size=11),
                height=28,
            ),
            cells=dict(
                values=[
                    stats_table["Group"],
                    stats_table["Min Whisker"].map(lambda value: f"{value:.1f}"),
                    stats_table["Q1"].map(lambda value: f"{value:.1f}"),
                    stats_table["Median"].map(lambda value: f"{value:.1f}"),
                    stats_table["Q3"].map(lambda value: f"{value:.1f}"),
                    stats_table["Max Whisker"].map(lambda value: f"{value:.1f}"),
                    stats_table["IQR"].map(lambda value: f"{value:.1f}"),
                    stats_table["Outliers"],
                ],
                fill_color=WHITE,
                line_color=BLACK,
                align=["left", "center", "center", "center", "center", "center", "center", "left"],
                font=dict(color=BLACK, size=10),
                height=25,
            ),
            columnwidth=[0.13, 0.12, 0.08, 0.1, 0.08, 0.12, 0.08, 0.29],
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Box(
            x=plot_df["continent"],
            y=plot_df["carbon_intensity"],
            name="IQR",
            showlegend=True,
            boxpoints="outliers",
            fillcolor=LIGHT_BLUE,
            line=dict(color=BLACK),
            marker=dict(color=LIGHT_GREEN, size=7, line=dict(color=BLACK, width=1)),
            hovertemplate="Continent: %{x}<br>Carbon Intensity: %{y:.1f}%<extra></extra>",
        ),
        row=2,
        col=1,
    )

    _label_box_medians(fig, plot_df, "continent", "carbon_intensity", row=2, col=1)
    _label_high_outliers(fig, plot_df, "continent", "carbon_intensity", row=2, col=1)

    fig = _guideline_layout(
        fig,
        title=f"Carbon Intensity by Continent ({selected_year})",
        x_title="Continent",
        y_title="Carbon Intensity (%)",
        y_values=pd.Series([100]),
        height=960,
    )

    fig.update_layout(
        legend=dict(
            title="Legend",
            x=0.96,
            y=0.53,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor=GRID,
            borderwidth=1,
            font=dict(size=10),
        )
    )

    fig.update_xaxes(categoryorder="array", categoryarray=continent_order, row=2, col=1)

    return fig


# ==================================================
# 5) VIOLIN PLOT
# ==================================================

def function_violin(
    data_path: str | Path | None = None,
    year: int | None = None,
    include_aggregates: bool = False,
):
    """
    Violin Plot:
    Renewable Share Distribution by Region.
    """
    _, go = _plotly()

    df, selected_year = _prepare_data(data_path, year, include_aggregates)

    plot_df = df.dropna(subset=["region_label", "renewable_share"]).copy()
    plot_df = plot_df[plot_df["region_label"] != "Other"]

    region_order = (
        plot_df.groupby("region_label", observed=True)["renewable_share"]
        .median()
        .sort_values(ascending=False)
        .index
        .tolist()
    )

    colors = [
        LIGHT_BLUE,
        BLUE_2,
        BLUE_3,
        BLUE_4,
        BLUE_5,
        LIGHT_GREEN,
        LIGHT_ORANGE,
        "#d6c7ff",
        "#c7f4f1",
    ]

    fig = go.Figure()

    for index, region in enumerate(region_order):
        region_df = plot_df[plot_df["region_label"] == region]
        color = colors[index % len(colors)]

        fig.add_trace(
            go.Violin(
                x=region_df["region_label"],
                y=region_df["renewable_share"],
                name=region.replace("<br>", " "),
                fillcolor=color,
                line=dict(color=BLACK, width=1.2),
                marker=dict(color=color, line=dict(color=BLACK, width=0.8)),
                box_visible=True,
                meanline_visible=False,
                points=False,
                spanmode="hard",
                showlegend=True,
                hovertemplate=(
                    f"Region: {region.replace('<br>', ' ')}"
                    "<br>Renewable Share: %{y:.1f}%<extra></extra>"
                ),
            )
        )

    _label_box_medians(fig, plot_df, "region_label", "renewable_share")

    fig = _guideline_layout(
        fig,
        title=f"Renewable Share Distribution by Region ({selected_year})",
        x_title="Region",
        y_title="Renewable Share (%)",
        y_values=pd.Series([100]),
        height=600,
    )

    fig.update_xaxes(categoryorder="array", categoryarray=region_order)

    return fig


if __name__ == "__main__":
    function_scatter().show()
    function_bubble().show()
    function_hist().show()
    function_box().show()
    function_violin().show()