import pandas as pd
import plotly.express as px


def function_chart1(df):
    """
    Column Chart:
    Top 10 Countries by Total Energy Consumption.
    """

    df = df.copy()

    df["year"] = pd.to_datetime(df["year"], errors="coerce").dt.year
    df["primary_energy_consumption"] = pd.to_numeric(
        df["primary_energy_consumption"],
        errors="coerce"
    )

    latest_year = df["year"].max()

    df_latest = df[
        (df["year"] == latest_year) &
        (df["primary_energy_consumption"] > 0)
    ].copy()

    # Keep real countries only, not regions/aggregates
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

    top_10 = (
        df_latest
        .sort_values("primary_energy_consumption", ascending=False)
        .head(10)
        .copy()
    )

    # Summarize long labels
    name_map = {
        "United States": "USA",
        "South Korea": "S. Korea"
    }
    top_10["country"] = top_10["country"].replace(name_map)

    # Winner must be on the far left
    top_10 = top_10.sort_values("primary_energy_consumption", ascending=False)

    top_color = "lightgreen"
    other_color = "lightblue"

    # Base figure
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

    # Replace base trace with two clean legend traces
    fig.data = []

    # Maximum performer
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

    # Standard performers
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
        uniformtext_mode="hide"
    )

    # Black chart border
    fig.update_layout(
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


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned_data.csv")

    print("Testing function_chart1() ...")
    fig = function_chart1(df)

    fig.show()

    print("Title:", fig.layout.title.text)
    print("Bars:", sum(len(trace.x) for trace in fig.data))
    print("Countries:", list(fig.data[0].x) + list(fig.data[1].x))

    assert sum(len(trace.x) for trace in fig.data) == 10
    print("OK ✓")