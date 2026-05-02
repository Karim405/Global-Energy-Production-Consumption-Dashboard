"""
shared_ids.py
=============
ملف الـ IDs المشتركة بين كل أعضاء الفريق
Global Energy Production & Consumption Dashboard

⚠️  مهم جداً:
    - متغيرش أي ID في الملف ده
    - أي حد بيعمل component أو callback لازم يـ import منه
    - لو محتاج ID جديد، أضفه هنا وبلّغ باقي الفريق

استخدام:
    from shared_ids import Filters, Graphs, KPI
"""


# ══════════════════════════════════════════════
#  FILTERS  (Person 4 — time_filters.py)
# ══════════════════════════════════════════════

class Filters:
    """IDs بتاعة عناصر التحكم — بيعملها Person 4، بيستخدمها Person 5 في الـ callbacks."""

    COUNTRY_DROPDOWN = "country-dropdown"
    # نوع    : dcc.Dropdown  (multi=True)
    # قيمة   : list of country name strings  e.g. ["Egypt", "Germany"]
    # default: []  →  يعني global aggregate

    CONTINENT_CHECKLIST = "continent-checklist"
    # نوع    : dcc.Checklist
    # قيمة   : list of continent strings
    # options: ["Africa","Asia","Europe","North America","South America","Oceania"]
    # default: كل القارات محددة

    YEAR_SLIDER = "year-slider"
    # نوع    : dcc.RangeSlider
    # قيمة   : [start_year, end_year]  e.g. [1990, 2022]
    # range  : 1900 → 2022

    ENERGY_SOURCE_RADIO = "energy-source-radio"
    # نوع    : dcc.RadioItems
    # قيمة   : اسم الـ column في الداتا — واحدة من الأتي:
    #   "renewables_electricity"
    #   "solar_electricity"
    #   "wind_electricity"
    #   "hydro_electricity"
    #   "nuclear_electricity"
    #   "coal_production"
    #   "gas_production"
    #   "oil_production"
    #   "primary_energy_consumption"
    # default: "renewables_electricity"

    RESET_BTN = "reset-filters-btn"
    # نوع    : html.Button
    # قيمة   : n_clicks (int)


# ══════════════════════════════════════════════
#  GRAPHS  (Persons 1, 2, 3, 4)
# ══════════════════════════════════════════════

class Graphs:
    """IDs بتاعة الـ dcc.Graph components — بيحطها Person 5 في الـ layout، والكل بيكتب figure ليها."""

    # ── Person 1 — Comparison A
    CHART1_COLUMN = "graph-chart1-column"         # Top 10 by Energy Consumption
    CHART2_BAR = "graph-chart2-bar"            # Top 10 by Renewable Share
    # Energy Mix for Selected Countries
    CHART3_STACKED_COL = "graph-chart3-stacked-col"

    # ── Person 2 — Comparison B
    # Fossil vs Renewable by Continent
    CHART4_STACKED_BAR = "graph-chart4-stacked-bar"
    # Oil vs Gas vs Coal top countries
    CHART5_CLUSTERED_COL = "graph-chart5-clustered-col"
    # Solar vs Wind vs Hydro comparison
    CHART6_CLUSTERED_BAR = "graph-chart6-clustered-bar"

    # ── Person 3 — Relationship & Distribution
    SCATTER = "graph-scatter"               # GDP vs Energy Consumption
    BUBBLE = "graph-bubble"                # GDP vs Renewable Share (size=pop)
    HISTOGRAM = "graph-histogram"             # Per Capita Energy Distribution
    BOX = "graph-box"                   # Carbon Intensity by Continent
    VIOLIN = "graph-violin"                # Renewable Share by Region

    # ── Person 4 — Time Series
    LINE = "graph-line"                  # Global Renewable Trend Over Years
    AREA = "graph-area"                  # Fossil → Renewable Transition


# ══════════════════════════════════════════════
#  KPI CARDS  (Person 2 — comparison_B_kpi.py)
# ══════════════════════════════════════════════

class KPI:
    """IDs بتاعة الـ KPI cards — Person 2 بيحسب القيم، Person 5 بيعمل الـ update."""

    TOTAL_CONSUMPTION = "kpi-total-consumption"
    # القيمة : إجمالي استهلاك الطاقة العالمي (TWh)

    AVG_RENEWABLE_SHARE = "kpi-avg-renewable-share"
    # القيمة : متوسط نسبة الطاقة المتجددة (%)

    TOP_PRODUCER = "kpi-top-producer"
    # القيمة : اسم أكبر منتج للطاقة

    AVG_CARBON_INTENSITY = "kpi-avg-carbon-intensity"
    # القيمة : متوسط كثافة الكربون (energy_per_gdp)


# ══════════════════════════════════════════════
#  DATA PATH  (مشترك بين الكل)
# ══════════════════════════════════════════════

DATA_PATH = "data/cleaned_data.csv"
# الداتا لازم تبقى في  ProjectFolder/data/cleaned_data.csv


# ══════════════════════════════════════════════
#  QUICK REFERENCE TABLE
# ══════════════════════════════════════════════

if __name__ == "__main__":
    rows = [
        ("FILTER",  "country-dropdown",        "Person 4",  "Person 5"),
        ("FILTER",  "continent-checklist",      "Person 4",  "Person 5"),
        ("FILTER",  "year-slider",              "Person 4",  "Person 5"),
        ("FILTER",  "energy-source-radio",      "Person 4",  "Person 5"),
        ("GRAPH",   "graph-chart1-column",      "Person 1",  "Person 5"),
        ("GRAPH",   "graph-chart2-bar",         "Person 1",  "Person 5"),
        ("GRAPH",   "graph-chart3-stacked-col", "Person 1",  "Person 5"),
        ("GRAPH",   "graph-chart4-stacked-bar", "Person 2",  "Person 5"),
        ("GRAPH",   "graph-chart5-clustered-col", "Person 2", "Person 5"),
        ("GRAPH",   "graph-chart6-clustered-bar", "Person 2", "Person 5"),
        ("GRAPH",   "graph-scatter",            "Person 3",  "Person 5"),
        ("GRAPH",   "graph-bubble",             "Person 3",  "Person 5"),
        ("GRAPH",   "graph-histogram",          "Person 3",  "Person 5"),
        ("GRAPH",   "graph-box",                "Person 3",  "Person 5"),
        ("GRAPH",   "graph-violin",             "Person 3",  "Person 5"),
        ("GRAPH",   "graph-line",               "Person 4",  "Person 5"),
        ("GRAPH",   "graph-area",               "Person 4",  "Person 5"),
        ("KPI",     "kpi-total-consumption",    "Person 2",  "Person 5"),
        ("KPI",     "kpi-avg-renewable-share",  "Person 2",  "Person 5"),
        ("KPI",     "kpi-top-producer",         "Person 2",  "Person 5"),
        ("KPI",     "kpi-avg-carbon-intensity", "Person 2",  "Person 5"),
    ]

    print(f"{'Type':<8} {'ID':<32} {'Owner':<12} {'Used By'}")
    print("-" * 65)
    for r in rows:
        print(f"{r[0]:<8} {r[1]:<32} {r[2]:<12} {r[3]}")
