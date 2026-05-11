# Global-Energy-Production-Consumption-Dashboard

## Description
This project explores how countries around the world produce and consume energy from
various sources including fossil fuels (oil, gas, coal), nuclear power, and renewable sources
(solar, wind, hydro). Teams will compare energy consumption and renewable adoption
rates across countries, investigate the relationship between economic development and
energy use patterns, analyze the distribution of energy metrics like per capita consumption
and carbon intensity, and track the global energy transition from fossil fuels to renewables
over decades. The goal is to build a dashboard that visualizes the world's energy landscape
and the progress toward clean energy.

# ⚡ Global Energy Production & Consumption Dashboard

An interactive, multi-page Plotly Dash dashboard covering all chart types from the Data Visualization course (Week 1–9).

## 📁 Project Structure

```
EnergyDashboard/
├── app.py                  # Main Dash application (entry point)
├── callbacks.py            # Placeholder (callbacks are in app.py)
├── comparison_A.py         # Person 1 — Comparison charts A (Column, Bar, Stacked)
├── comparison_B_kpi.py     # Person 2 — Comparison charts B + KPI logic
├── relation_distribution.py # Person 3 — Scatter, Bubble, Histogram, Box, Violin
├── time_filters.py         # Person 4 — Line, Area charts + Filters layout
├── shared_ids.py           # Shared component IDs for the team
├── requirements.txt        # Python dependencies
├── data/
│   └── cleaned_data.csv    # ← PUT YOUR DATA FILE HERE
└── README.md
```

## 🚀 How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place your data file:**
   Put `cleaned_data.csv` inside the `data/` folder.

3. **Run the dashboard:**
   ```bash
   python app.py
   ```

4. **Open in browser:**
   Navigate to `http://127.0.0.1:8050/`

## 📊 Dashboard Pages

| Page | Charts |
|------|--------|
| **Overview & KPIs** | 4 KPI cards + Global Trend Line + Continent Bar |
| **Comparison A** | Column Chart, Bar Chart, Stacked Bar Chart |
| **Comparison B** | Stacked Bar, Clustered Column, Clustered Bar |
| **Relationships** | Scatter Chart, Bubble Chart |
| **Distributions** | Histogram, Box Chart, Violin Chart |
| **Time Series** | Line Chart, Area Chart |

## 🎛️ Interactive Filters

All charts respond to the filter panel on the right side:
- **Year Range Slider** — filter data by year range
- **Country Dropdown** — focus on specific countries
- **Continent Checklist** — include/exclude continents
- **Energy Source Radio** — select primary energy metric
- **Reset Button** — reset all filters to default

## 👥 Team Roles

| Person | Responsibility | File |
|--------|---------------|------|
| Ahmed Waleed| Comparison Charts A | `comparison_A.py` |
| Hassan Mohamed| Comparison Charts B + KPIs | `comparison_B_kpi.py` |
| Omar Adel| Relationship & Distribution | `relation_distribution.py` |
| Omar Ragab| Time Series + Filters | `time_filters.py` |
| Karim Hamada | App layout + Callbacks | `app.py` |
