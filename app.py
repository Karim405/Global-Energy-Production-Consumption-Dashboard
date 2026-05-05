from dash import Dash, dcc, html

from relation_distribution import (
    function_scatter,
    function_bubble,
    function_hist,
    function_box,
    function_violin
)


app = Dash(__name__)

CARD_STYLE = {
    "backgroundColor": "white",
    "padding": "20px",
    "marginBottom": "30px",
    "borderRadius": "12px",
    "boxShadow": "0 4px 12px rgba(0, 0, 0, 0.08)"
}

SECTION_TITLE_STYLE = {
    "color": "#1f3b4d",
    "borderBottom": "2px solid #d9e2ec",
    "paddingBottom": "8px",
    "marginTop": "35px",
    "marginBottom": "20px"
}

CHART_TITLE_STYLE = {
    "color": "#243b53",
    "fontSize": "22px",
    "marginBottom": "5px"
}

CHART_DESC_STYLE = {
    "color": "#627d98",
    "fontSize": "15px",
    "marginBottom": "15px"
}


app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f4f7fb",
        "padding": "25px",
        "minHeight": "100vh"
    },
    children=[
        html.Div(
            style={
                "backgroundColor": "#1f3b4d",
                "color": "white",
                "padding": "25px",
                "borderRadius": "14px",
                "textAlign": "center",
                "marginBottom": "30px"
            },
            children=[
                html.H1(
                    "Global Energy Production & Consumption Dashboard",
                    style={"margin": "0"}
                ),
                html.P(
                    "Relationship and Distribution Analysis Module",
                    style={"marginTop": "10px", "fontSize": "18px"}
                )
            ]
        ),

        html.H2("Relationship Charts", style=SECTION_TITLE_STYLE),

        html.Div(
            style=CARD_STYLE,
            children=[
                html.H3("1. GDP vs Energy Consumption", style=CHART_TITLE_STYLE),
                html.P(
                    "This scatter plot shows the relationship between a country's GDP and its primary energy consumption.",
                    style=CHART_DESC_STYLE
                ),
                dcc.Graph(figure=function_scatter())
            ]
        ),

        html.Div(
            style=CARD_STYLE,
            children=[
                html.H3("2. GDP vs Renewable Energy Share", style=CHART_TITLE_STYLE),
                html.P(
                    "This bubble plot compares GDP with renewable energy share. Bubble size represents population.",
                    style=CHART_DESC_STYLE
                ),
                dcc.Graph(figure=function_bubble())
            ]
        ),

        html.H2("Distribution Charts", style=SECTION_TITLE_STYLE),

        html.Div(
            style=CARD_STYLE,
            children=[
                html.H3("3. Distribution of Per Capita Energy Use", style=CHART_TITLE_STYLE),
                html.P(
                    "This histogram shows how energy use per person is distributed across countries.",
                    style=CHART_DESC_STYLE
                ),
                dcc.Graph(figure=function_hist())
            ]
        ),

        html.Div(
            style=CARD_STYLE,
            children=[
                html.H3("4. Carbon Intensity Proxy by Region", style=CHART_TITLE_STYLE),
                html.P(
                    "This box plot compares the carbon intensity proxy across world regions.",
                    style=CHART_DESC_STYLE
                ),
                dcc.Graph(figure=function_box())
            ]
        ),

        html.Div(
            style=CARD_STYLE,
            children=[
                html.H3("5. Renewable Share Distribution by Region", style=CHART_TITLE_STYLE),
                html.P(
                    "This violin plot shows the distribution shape of renewable energy share across regions.",
                    style=CHART_DESC_STYLE
                ),
                dcc.Graph(figure=function_violin())
            ]
        )
    ]
)


if __name__ == "__main__":
    app.run(debug=True)