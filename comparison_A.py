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
##chart1

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
##testchart1
if __name__ == "__main__":
    import pandas as pd

    # اقرأ الداتا
    df = pd.read_csv(DATA_PATH)

    print("Testing function_chart1() ...")

    # استدعاء الشارت
    fig1 = function_chart1(df)

    print("Chart 1 OK ✓")

    # عرض الشارت
    fig1.show()


##chart2

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

##testchart2


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

##chart3
import pandas as pd
import plotly.graph_objects as go
def function_chart3(df):
    """
    Stacked Bar Chart:
    Energy Mix Composition for Selected Countries
    Coal + Oil + Gas + Renewables
    """

    import pandas as pd
    import plotly.graph_objects as go

    df_latest, latest_year = _prepare_latest_real_countries(df)

    df_latest["coal"] = pd.to_numeric(
        df_latest["coal_production"], errors="coerce"
    ).fillna(0)

    df_latest["oil"] = pd.to_numeric(
        df_latest["oil_production"], errors="coerce"
    ).fillna(0)

    df_latest["gas"] = pd.to_numeric(
        df_latest["gas_production"], errors="coerce"
    ).fillna(0)

    df_latest["renewables"] = pd.to_numeric(
        df_latest["renewables_electricity"], errors="coerce"
    ).fillna(0)

    df_latest["total"] = (
        df_latest["coal"]
        + df_latest["oil"]
        + df_latest["gas"]
        + df_latest["renewables"]
    )

    top = (
        df_latest[df_latest["total"] > 0]
        .sort_values("total", ascending=False)
        .head(5)
        .copy()
    )

    top = _shorten_country_names(top)
    top = top.sort_values("total", ascending=True)

    fig = go.Figure()

    fig.add_bar(
        y=top["country"],
        x=top["coal"],
        name="Coal",
        orientation="h",
        marker_color="#C7DCEB",
        marker_line=dict(color="white", width=1),
        text=top["coal"].round(0),
        texttemplate="%{text:.0f}",
        textposition="inside",
        textfont=dict(color="black", size=11),
        hovertemplate="<b>%{y}</b><br>Coal: %{x:.2f}<extra></extra>"
    )

    fig.add_bar(
        y=top["country"],
        x=top["oil"],
        name="Oil",
        orientation="h",
        marker_color="#9FC4DB",
        marker_line=dict(color="white", width=1),
        text=top["oil"].round(0),
        texttemplate="%{text:.0f}",
        textposition="inside",
        textfont=dict(color="black", size=11),
        hovertemplate="<b>%{y}</b><br>Oil: %{x:.2f}<extra></extra>"
    )

    fig.add_bar(
        y=top["country"],
        x=top["gas"],
        name="Gas",
        orientation="h",
        marker_color="#5DADE2",
        marker_line=dict(color="white", width=1),
        text=top["gas"].round(0),
        texttemplate="%{text:.0f}",
        textposition="inside",
        textfont=dict(color="black", size=11),
        hovertemplate="<b>%{y}</b><br>Gas: %{x:.2f}<extra></extra>"
    )

    fig.add_bar(
        y=top["country"],
        x=top["renewables"],
        name="Renewables",
        orientation="h",
        marker_color="#7DDA7A",
        marker_line=dict(color="white", width=1),
        text=top["renewables"].round(0),
        texttemplate="%{text:.0f}",
        textposition="inside",
        textfont=dict(color="black", size=11),
        hovertemplate="<b>%{y}</b><br>Renewables: %{x:.2f}<extra></extra>"
    )

    max_total = top["total"].max()

    for _, row in top.iterrows():
        fig.add_annotation(
            x=row["total"] + max_total * 0.02,
            y=row["country"],
            text=f"Total: {row['total']:.0f}",
            showarrow=False,
            font=dict(size=12, color="black")
        )

    fig.update_layout(
        title={
            "text": f"Energy Mix Composition for Selected Countries ({latest_year})",
            "x": 0.5,
            "xanchor": "center",
            "font": dict(size=18, color="black")
        },
        xaxis_title="Total Energy",
        yaxis_title="Country",
        barmode="stack",
        template="plotly_white",
        font=dict(color="black"),
        legend=dict(
            title="Energy Source",
            traceorder="normal",
            x=0.98,
            y=0.98,
            xanchor="right",
            yanchor="top",
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        ),
        margin=dict(l=120, r=160, t=90, b=70),
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
        gridcolor="lightgray",
        rangemode="tozero",
        range=[0, max_total * 1.2]
    )

    fig.update_yaxes(showgrid=False)

    return fig

##testchart3

if __name__ == "__main__":
    df = pd.read_csv(DATA_PATH)

    print("Testing function_chart3() ...")
    fig = function_chart3(df)
    print("Chart 3 OK ✓")

    fig.show()