import pandas as pd
import plotly.express as px

try:
    from shared_ids import DATA_PATH
except ImportError:
    DATA_PATH = "data/cleaned_data.csv"


def _prepare_latest_real_countries(df):
    df = df.copy()

    df["year"] = pd.to_datetime(df["year"], errors="coerce").dt.year
    latest_year = df["year"].max()

    df_latest = df[df["year"] == latest_year].copy()

    try:
        import country_converter as coco

        cc = coco.CountryConverter()
        df_latest["real_iso3"] = cc.pandas_convert(
            series=df_latest["country"],
            to="ISO3"
        )

        df_latest = df_latest[
            df_latest["real_iso3"].notna() &
            (df_latest["real_iso3"] != "not found")
        ].copy()

    except ImportError:
        aggregate_keywords = (
            "World|Asia|Europe|Africa|America|OECD|OPEC|CIS|Ember|"
            "income|ASEAN|Middle East|Non-OECD|G20|G7|European Union"
        )

        df_latest = df_latest[
            ~df_latest["country"].astype(str).str.contains(
                aggregate_keywords,
                case=False,
                na=False
            )
        ].copy()

    return df_latest, latest_year


def _shorten_country_names(df):
    name_map = {
        "United States": "USA",
        "South Korea": "S. Korea",
        "United Kingdom": "UK"
    }

    df = df.copy()
    df["country"] = df["country"].replace(name_map)
    return df


def function_chart1(df):
    """
    Column Chart:
    Top 10 Countries by Total Energy Consumption.
    """

    df_latest, latest_year = _prepare_latest_real_countries(df)

    df_latest["primary_energy_consumption"] = pd.to_numeric(
        df_latest["primary_energy_consumption"],
        errors="coerce"
    )

    df_latest = df_latest[df_latest["primary_energy_consumption"] > 0].copy()

    top_10 = (
        df_latest
        .sort_values("primary_energy_consumption", ascending=False)
        .head(10)
        .copy()
    )

    top_10 = _shorten_country_names(top_10)
    top_10 = top_10.sort_values("primary_energy_consumption", ascending=False)

    top_color = "lightgreen"
    other_color = "lightblue"

    fig = px.bar(
        top_10,
        x="country",
        y="primary_energy_consumption",
        title=f"Top 10 Countries by Total Energy Consumption ({latest_year})",
        labels={
            "country": "Country",
            "primary_energy_consumption": "Total Energy Consumption (TWh)"
        }
    )

    fig.data = []

    fig.add_bar(
        x=[top_10.iloc[0]["country"]],
        y=[top_10.iloc[0]["primary_energy_consumption"]],
        name="Maximum Performer",
        marker_color=top_color,
        text=[top_10.iloc[0]["primary_energy_consumption"]],
        texttemplate="%{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Energy Consumption: %{y:,.2f} TWh<extra></extra>"
    )

    fig.add_bar(
        x=top_10.iloc[1:]["country"],
        y=top_10.iloc[1:]["primary_energy_consumption"],
        name="Standard Performance",
        marker_color=other_color,
        text=top_10.iloc[1:]["primary_energy_consumption"],
        texttemplate="%{text:,.0f}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Energy Consumption: %{y:,.2f} TWh<extra></extra>"
    )

    fig.update_layout(
        template="plotly_white",
        barmode="group",
        showlegend=True,
        font=dict(color="black"),
        title={
            "text": f"Top 10 Countries by Total Energy Consumption ({latest_year})",
            "x": 0.5,
            "xanchor": "center"
        },
        legend=dict(
            title="",
            x=0.98,
            y=0.98,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="black",
            borderwidth=1
        ),
        margin=dict(l=50, r=50, t=90, b=80),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="black", width=2)
            )
        ]
    )

    fig.update_xaxes(
        title_text="Country",
        tickangle=0,
        showgrid=False
    )

    fig.update_yaxes(
        title_text="Total Energy Consumption (TWh)",
        gridcolor="lightgray",
        rangemode="tozero"
    )

    return fig


def function_chart2(df):
    """
    Bar Chart:
    Top 10 Countries by Renewable Energy Share.
    """

    df_latest, latest_year = _prepare_latest_real_countries(df)

    df_latest["primary_energy_consumption"] = pd.to_numeric(
        df_latest["primary_energy_consumption"],
        errors="coerce"
    )

    df_latest["renewables_electricity"] = pd.to_numeric(
        df_latest["renewables_electricity"],
        errors="coerce"
    )

    df_latest = df_latest[
        (df_latest["primary_energy_consumption"] > 0) &
        (df_latest["renewables_electricity"] >= 0)
    ].copy()

    df_latest["renewable_share"] = (
        df_latest["renewables_electricity"] /
        df_latest["primary_energy_consumption"]
    ) * 100

    df_latest = df_latest[
        df_latest["renewable_share"].notna() &
        (df_latest["renewable_share"] > 0)
    ].copy()

    top_10 = (
        df_latest
        .sort_values("renewable_share", ascending=False)
        .head(10)
        .copy()
    )

    top_10 = _shorten_country_names(top_10)

    # For horizontal bar charts, ascending puts the highest value at the top.
    top_10 = top_10.sort_values("renewable_share", ascending=True)

    top_color = "lightgreen"
    other_color = "lightblue"

    standard = top_10.iloc[:-1]
    maximum = top_10.iloc[-1]

    fig = px.bar(
        top_10,
        x="renewable_share",
        y="country",
        orientation="h",
        title=f"Top 10 Countries by Renewable Energy Share ({latest_year})",
        labels={
            "country": "Country",
            "renewable_share": "Renewable Energy Share (%)"
        }
    )

    fig.data = []

    fig.add_bar(
        x=standard["renewable_share"],
        y=standard["country"],
        orientation="h",
        name="Standard Performance",
        marker_color=other_color,
        text=standard["renewable_share"],
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Renewable Share: %{x:.2f}%<extra></extra>"
    )

    fig.add_bar(
        x=[maximum["renewable_share"]],
        y=[maximum["country"]],
        orientation="h",
        name="Maximum Performer",
        marker_color=top_color,
        text=[maximum["renewable_share"]],
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Renewable Share: %{x:.2f}%<extra></extra>"
    )

    fig.update_layout(
        template="plotly_white",
        barmode="group",
        showlegend=True,
        font=dict(color="black"),
        title={
            "text": f"Top 10 Countries by Renewable Energy Share ({latest_year})",
            "x": 0.5,
            "xanchor": "center"
        },
        legend=dict(
            title="",
            x=0.98,
            y=0.98,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor="black",
            borderwidth=1
        ),
        margin=dict(l=100, r=90, t=90, b=70),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="black", width=2)
            )
        ]
    )

    fig.update_xaxes(
        title_text="Renewable Energy Share (%)",
        gridcolor="lightgray",
        rangemode="tozero"
    )

    fig.update_yaxes(
        title_text="Country",
        showgrid=False
    )

    return fig


if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)

    print("Testing function_chart1() ...")
    fig1 = function_chart1(df)
    print("Chart 1 bars:", sum(len(trace.x) for trace in fig1.data))
    assert sum(len(trace.x) for trace in fig1.data) == 10
    print("Chart 1 OK ✓")

    print("Testing function_chart2() ...")
    fig2 = function_chart2(df)
    print("Chart 2 bars:", sum(len(trace.y) for trace in fig2.data))
    assert sum(len(trace.y) for trace in fig2.data) == 10
    print("Chart 2 OK ✓")

    fig2.show()