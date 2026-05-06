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
| Person 1 | Comparison Charts A | `comparison_A.py` |
| Person 2 | Comparison Charts B + KPIs | `comparison_B_kpi.py` |
| Person 3 | Relationship & Distribution | `relation_distribution.py` |
| Person 4 | Time Series + Filters | `time_filters.py` |
| Person 5 | App layout + Callbacks | `app.py` |
