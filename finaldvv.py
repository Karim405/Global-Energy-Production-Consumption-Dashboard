# %%
import pandas as pd
import numpy as np
import plotly.express as px


# %%
df=pd.read_csv(r"c:\Users\OC\Downloads\cleaned_data.csv")

# %%
df.head(5)

# %%
# %%
print(df.columns)

# %%

df = df[~df['country'].str.contains(r"\(")]

regions = ['World', 'Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']

df = df[~df['country'].isin(regions)]

# %%
print(df['country'].unique()[:20])

# %%
continent_map = {
    # Africa
    "Egypt": "Africa", "Nigeria": "Africa", "South Africa": "Africa",
    "Algeria": "Africa", "Morocco": "Africa", "Kenya": "Africa",

    # Asia
    "China": "Asia", "India": "Asia", "Japan": "Asia",
    "Saudi Arabia": "Asia", "Indonesia": "Asia", "South Korea": "Asia",

    # Europe
    "Germany": "Europe", "France": "Europe", "United Kingdom": "Europe",
    "Italy": "Europe", "Spain": "Europe", "Netherlands": "Europe",

    # North America
    "United States": "North America", "Canada": "North America", "Mexico": "North America",

    # South America
    "Brazil": "South America", "Argentina": "South America", "Chile": "South America",

    # Oceania
    "Australia": "Oceania", "New Zealand": "Oceania"
}

# %%
df['continent'] = df['country'].map(continent_map)

# %%
df = df.dropna(subset=['continent'])

# %%
print(df[['country','continent']].head(20))


# %%
df_grouped = df.groupby('continent').agg({
    'coal_production': 'sum',
    'gas_production': 'sum',
    'oil_production': 'sum',
    'renewables_electricity': 'sum'
}).reset_index()

df_grouped['fossil'] = (
    df_grouped['coal_production'] +
    df_grouped['gas_production'] +
    df_grouped['oil_production']
)

df_grouped['renewable'] = df_grouped['renewables_electricity']

# %%
df_grouped = df_grouped.sort_values(by='fossil', ascending=False)

# %%
# be number integer
df_grouped['fossil'] = df_grouped['fossil'].fillna(0)
df_grouped['renewable'] = df_grouped['renewable'].fillna(0)

df_grouped['fossil'] = df_grouped['fossil'].astype(float)
df_grouped['renewable'] = df_grouped['renewable'].astype(float)

df_grouped['total'] = df_grouped['fossil'] + df_grouped['renewable']

# %%
import plotly.graph_objects as go

def function_chart4():

    
    df_grouped['fossil'] = df_grouped['fossil'].fillna(0)
    df_grouped['renewable'] = df_grouped['renewable'].fillna(0)

    # total
    df_grouped['total'] = df_grouped['fossil'] + df_grouped['renewable']

    
    df_sorted = df_grouped.sort_values(by='total', ascending=True).reset_index(drop=True)

    
    max_idx = df_sorted['total'].idxmax()

    
    fossil_colors = ['#c6dbef'] * len(df_sorted)
    fossil_colors[max_idx] = '#b7e4c7'   # light green

    
    renewable_colors = ['#4a90c2'] * len(df_sorted)
    renewable_colors[max_idx] = '#2e7d32'  # dark green

    fig = go.Figure()

    # Fossil
    fig.add_bar(
        y=df_sorted['continent'],
        x=df_sorted['fossil'],
        name='Fossil',
        orientation='h',
        marker=dict(color=fossil_colors),
        text=df_sorted['fossil'].round(0),
        textposition='inside',
        insidetextanchor='middle'
    )

    # Renewable
    fig.add_bar(
        y=df_sorted['continent'],
        x=df_sorted['renewable'],
        name='Renewable',
        orientation='h',
        marker=dict(color=renewable_colors),
        text=df_sorted['renewable'].round(0),
        textposition='inside',
        insidetextanchor='middle'
    )

    # 🔥 Legend explanation (dummy traces)
    fig.add_trace(go.Bar(
        x=[None],
        y=[None],
        name='Max Fossil (Light Green)',
        marker=dict(color='#b7e4c7'),
        showlegend=True
    ))

    fig.add_trace(go.Bar(
        x=[None],
        y=[None],
        name='Max Renewable (Dark Green)',
        marker=dict(color='#2e7d32'),
        showlegend=True
    ))

    # Total labels
    for i in range(len(df_sorted)):
        fig.add_annotation(
            x=df_sorted['total'].iloc[i],
            y=df_sorted['continent'].iloc[i],
            text="Total: " + str(int(df_sorted['total'].iloc[i])),
            showarrow=False,
            xshift=30,
            font=dict(color="black")
        )

    # Layout
    fig.update_layout(
        barmode='stack',

        title={
            'text': "Fossil vs Renewable Consumption by Continent",
            'x': 0.5,
            'xanchor': 'center'
        },

        xaxis_title="Energy",
        yaxis_title="Continent",

        template="plotly_white",
        paper_bgcolor="#f4f6f9",
        plot_bgcolor="white",

        margin=dict(l=40, r=120, t=70, b=40),

        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        ),

        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0, y0=0,
                x1=1, y1=1,
                line=dict(color="black", width=1)
            )
        ],

        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(0,0,0,0.25)",
            griddash="dot",
            gridwidth=1
        ),

        yaxis=dict(showgrid=False)
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_xaxes(range=[0, df_sorted['total'].max() * 1.15])

    return fig


fig = function_chart4()
fig.show()

# %%
print(df_grouped.head())
print(df_grouped[['fossil','renewable']].sum())

# %%
print(df_grouped.columns)



# %%
print(df.columns)


# %%
import plotly.graph_objects as go

def function_chart5():

    df_clean = df.copy()

    df_country = df_clean.groupby('country', as_index=False)[
        ['oil_production', 'gas_production', 'coal_production']
    ].sum()

    df_country['total_fossil'] = (
        df_country['oil_production'] +
        df_country['gas_production'] +
        df_country['coal_production']
    )

    df_sorted = df_country.sort_values(by='total_fossil', ascending=False).head(10)

    max_oil  = df_sorted['oil_production'].max()
    max_gas  = df_sorted['gas_production'].max()
    max_coal = df_sorted['coal_production'].max()

    oil_blue  = '#9ecae1'
    gas_blue  = '#6baed6'
    coal_blue = '#4292c6'

    oil_green  = '#b2f2bb'
    gas_green  = '#a3e4a9'
    coal_green = '#8fd19e'

    oil_colors  = [oil_green if v == max_oil else oil_blue for v in df_sorted['oil_production']]
    gas_colors  = [gas_green if v == max_gas else gas_blue for v in df_sorted['gas_production']]
    coal_colors = [coal_green if v == max_coal else coal_blue for v in df_sorted['coal_production']]

    fig = go.Figure()

    fig.add_bar(
        x=df_sorted['country'],
        y=df_sorted['oil_production'],
        marker=dict(color=oil_colors),
        text=df_sorted['oil_production'].astype(int),
        textposition='outside',
        textfont=dict(size=11, color='black'),
        showlegend=False,
        offsetgroup=0
    )

    fig.add_bar(
        x=df_sorted['country'],
        y=df_sorted['gas_production'],
        marker=dict(color=gas_colors),
        text=df_sorted['gas_production'].astype(int),
        textposition='outside',
        textfont=dict(size=11, color='black'),
        showlegend=False,
        offsetgroup=1
    )

    fig.add_bar(
        x=df_sorted['country'],
        y=df_sorted['coal_production'],
        marker=dict(color=coal_colors),
        text=df_sorted['coal_production'].astype(int),
        textposition='outside',
        textfont=dict(size=11, color='black'),
        showlegend=False,
        offsetgroup=2
    )

    # Legend زي ما هو
    fig.add_bar(x=[None], y=[None], name='Oil', marker=dict(color=oil_blue))
    fig.add_bar(x=[None], y=[None], name='Gas', marker=dict(color=gas_blue))
    fig.add_bar(x=[None], y=[None], name='Coal', marker=dict(color=coal_blue))

    fig.add_bar(x=[None], y=[None], name='Max Oil', marker=dict(color=oil_green))
    fig.add_bar(x=[None], y=[None], name='Max Gas', marker=dict(color=gas_green))
    fig.add_bar(x=[None], y=[None], name='Max Coal', marker=dict(color=coal_green))

    fig.update_layout(
        barmode='group',

        width=1500,
        height=600,

        
        bargap=0.05,
        bargroupgap=0.01,

        title=dict(text="Oil vs Gas vs Coal (Top 10 Countries)", x=0.5),

        xaxis=dict(
            title="Country",
            tickangle=0,
            tickfont=dict(size=12),
            automargin=True
        ),

        yaxis=dict(
            title="Energy Production",
            tickfont=dict(size=12)
        ),

        template="plotly_white",

        legend=dict(
            x=1, y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        ),

        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2)
            )
        ],

        margin=dict(l=50, r=50, t=70, b=80)
    )

    return fig


fig = function_chart5()
fig.show()

# %%
import plotly.graph_objects as go

def function_chart3():

    df_clean = df.copy()

    df_energy = df_clean.groupby('country', as_index=False)[
        ['solar_electricity', 'wind_electricity', 'hydro_electricity']
    ].sum()

    df_energy['total'] = (
        df_energy['solar_electricity'] +
        df_energy['wind_electricity'] +
        df_energy['hydro_electricity']
    )

    df_sorted = df_energy.sort_values(by='total', ascending=False).head(10)

    max_solar = df_sorted['solar_electricity'].max()
    max_wind  = df_sorted['wind_electricity'].max()
    max_hydro = df_sorted['hydro_electricity'].max()

    
    solar_blue  = '#9ecae1'
    wind_blue   = '#6baed6'
    hydro_blue  = '#4292c6'

    solar_green = '#b2f2bb'
    wind_green  = '#a3e4a9'
    hydro_green = '#8fd19e'

    
    solar_colors = [solar_green if v == max_solar else solar_blue for v in df_sorted['solar_electricity']]
    wind_colors  = [wind_green if v == max_wind else wind_blue for v in df_sorted['wind_electricity']]
    hydro_colors = [hydro_green if v == max_hydro else hydro_blue for v in df_sorted['hydro_electricity']]

    fig = go.Figure()

    fig.add_bar(
        x=df_sorted['country'],
        y=df_sorted['solar_electricity'],
        marker=dict(color=solar_colors),
        text=df_sorted['solar_electricity'].astype(int),
        textposition='outside',
        textfont=dict(size=11, color='black'),
        showlegend=False,
        offsetgroup=0
    )

    fig.add_bar(
        x=df_sorted['country'],
        y=df_sorted['wind_electricity'],
        marker=dict(color=wind_colors),
        text=df_sorted['wind_electricity'].astype(int),
        textposition='outside',
        textfont=dict(size=11, color='black'),
        showlegend=False,
        offsetgroup=1
    )

    fig.add_bar(
        x=df_sorted['country'],
        y=df_sorted['hydro_electricity'],
        marker=dict(color=hydro_colors),
        text=df_sorted['hydro_electricity'].astype(int),
        textposition='outside',
        textfont=dict(size=11, color='black'),
        showlegend=False,
        offsetgroup=2
    )

    
    solar_blue_l = '#9ecae1'
    wind_blue_l  = '#6baed6'
    hydro_blue_l = '#4292c6'

    solar_green_l = '#b2f2bb'
    wind_green_l  = '#a3e4a9'
    hydro_green_l = '#8fd19e'

    fig.add_bar(x=[None], y=[None], name='Solar', marker=dict(color=solar_blue_l))
    fig.add_bar(x=[None], y=[None], name='Wind', marker=dict(color=wind_blue_l))
    fig.add_bar(x=[None], y=[None], name='Hydro', marker=dict(color=hydro_blue_l))

    fig.add_bar(x=[None], y=[None], name='Max Solar', marker=dict(color=solar_green_l))
    fig.add_bar(x=[None], y=[None], name='Max Wind', marker=dict(color=wind_green_l))
    fig.add_bar(x=[None], y=[None], name='Max Hydro', marker=dict(color=hydro_green_l))

    fig.update_layout(
        barmode='group',

        width=1500,
        height=600,

        bargap=0.05,
        bargroupgap=0.01,

        title=dict(text="Solar vs Wind vs Hydro (Top 10 Countries)", x=0.5),

        xaxis=dict(
            title="Country",
            tickangle=0,
            tickfont=dict(size=12),
            automargin=True
        ),

        yaxis=dict(
            title="Electricity Generation",
            tickfont=dict(size=12)
        ),

        template="plotly_white",

        legend=dict(
            x=1, y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        ),

        # 🖤 نفس الإطار بتاع chart5
        shapes=[
            dict(
                type="rect",
                xref="paper", yref="paper",
                x0=0, y0=0, x1=1, y1=1,
                line=dict(color="black", width=2)
            )
        ],

        margin=dict(l=50, r=50, t=70, b=80)
    )

    return fig


fig = function_chart3()
fig.show()

# %%
print(df.columns)

# %%
def get_kpi_values(df):

    df = df.copy()

    # =========================
    # 🔥 Total Global Consumption
    # =========================
    total_global_consumption = df['primary_energy_consumption'].sum()

    # =========================
    # 🔥 Renewable Share (FIXED)
    # =========================
    renewable_cols = [
        'solar_electricity',
        'wind_electricity',
        'hydro_electricity'
    ]

    df['renewable_total'] = df[renewable_cols].sum(axis=1)

    df['renewable_share'] = df.apply(
        lambda row: (
            row['renewable_total'] / row['primary_energy_consumption']
            if row['primary_energy_consumption'] != 0 else 0
        ),
        axis=1
    )

    avg_renewable_share = df['renewable_share'].mean()

    # =========================
    # 🔥 Top Producer
    # =========================
    df['total_production'] = (
        df['oil_production'] +
        df['gas_production'] +
        df['coal_production']
    )

    top_producer = df.groupby('country')['total_production'].sum().idxmax()

    # =========================
    # 🔥 Carbon Intensity
    # =========================
    avg_carbon_intensity = df['energy_per_gdp'].mean()

    return {
        "total_global_consumption": total_global_consumption,
        "avg_renewable_share": avg_renewable_share,
        "top_producer": top_producer,
        "avg_carbon_intensity": avg_carbon_intensity
    }


# =========================
# 🔥 Display
# =========================

kpis = get_kpi_values(df)

print("🔥 KPI SUMMARY")
print("=" * 40)
print(f"Total Global Consumption : {kpis['total_global_consumption']:.2f}")
print(f"Avg Renewable Share      : {kpis['avg_renewable_share']:.2%}")
print(f"Top Producer             : {kpis['top_producer']}")
print(f"Avg Carbon Intensity     : {kpis['avg_carbon_intensity']:.2f}")

# %%
df[['solar_electricity','wind_electricity','hydro_electricity','renewables_electricity','primary_energy_consumption']].describe()

# %%



