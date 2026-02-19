"""
=============================================================
PROJECT 1: Supply Chain & Inventory Optimization Analysis
=============================================================
Author: Marmik Vyas
Tools: Python · Pandas · Matplotlib · Seaborn · Power BI Ready
Dataset: Synthetic Supply Chain Dataset (simulated real-world)

Business Problem:
    A manufacturing/export company wants to reduce inventory costs,
    minimize stockouts, and improve supplier performance.
    As a Business Analyst, we need to:
    1. Identify slow-moving and fast-moving SKUs
    2. Detect stockout risk across product categories
    3. Evaluate supplier delivery performance
    4. Generate KPI-ready data for Power BI dashboard

Key BA Deliverables:
    - Inventory Health Report
    - Supplier Scorecard
    - Demand Trend Analysis
    - Stockout Risk Matrix
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─── STYLING ───────────────────────────────────────────────
plt.style.use('seaborn-v0_8-whitegrid')
COLORS = {
    'primary': '#2E75B6',
    'secondary': '#ED7D31',
    'success': '#70AD47',
    'danger': '#FF0000',
    'warning': '#FFC000',
    'neutral': '#A5A5A5'
}

print("=" * 60)
print("SUPPLY CHAIN & INVENTORY OPTIMIZATION ANALYSIS")
print("Business Analyst: Marmik Vyas")
print("=" * 60)

# ─── STEP 1: DATA GENERATION (simulates real export company data) ───
np.random.seed(42)

categories = ['Electronics', 'Textiles', 'Furniture', 'Packaging', 'Raw Materials']
suppliers  = ['SupplierA', 'SupplierB', 'SupplierC', 'SupplierD', 'SupplierE']
skus = [f'SKU-{str(i).zfill(4)}' for i in range(1, 101)]  # 100 SKUs

# --- Inventory Dataset ---
inventory_data = []
for sku in skus:
    cat = np.random.choice(categories)
    sup = np.random.choice(suppliers)
    opening_stock   = np.random.randint(50, 500)
    avg_daily_sales = np.random.uniform(1, 20)
    reorder_point   = avg_daily_sales * 14   # 14-day lead time
    current_stock   = np.random.randint(0, 400)
    days_of_stock   = current_stock / avg_daily_sales if avg_daily_sales > 0 else 0
    stockout_risk   = 'High' if days_of_stock < 7 else ('Medium' if days_of_stock < 14 else 'Low')
    movement        = 'Fast' if avg_daily_sales > 10 else ('Medium' if avg_daily_sales > 5 else 'Slow')

    inventory_data.append({
        'SKU': sku,
        'Category': cat,
        'Supplier': sup,
        'Opening_Stock': opening_stock,
        'Current_Stock': current_stock,
        'Avg_Daily_Sales': round(avg_daily_sales, 2),
        'Reorder_Point': round(reorder_point, 0),
        'Days_of_Stock': round(days_of_stock, 1),
        'Stockout_Risk': stockout_risk,
        'Movement_Type': movement,
        'Unit_Cost': round(np.random.uniform(50, 2000), 2),
        'Holding_Cost_Per_Day': round(np.random.uniform(0.5, 5), 2)
    })

df_inv = pd.DataFrame(inventory_data)
df_inv['Inventory_Value'] = df_inv['Current_Stock'] * df_inv['Unit_Cost']
df_inv['Holding_Cost_Total'] = df_inv['Current_Stock'] * df_inv['Holding_Cost_Per_Day'] * 30

# --- Sales Time Series (12 months) ---
dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
sales_records = []
for date in dates:
    for cat in categories:
        base_sales = {'Electronics': 150, 'Textiles': 200, 'Furniture': 80, 'Packaging': 300, 'Raw Materials': 250}
        seasonality = 1 + 0.3 * np.sin(2 * np.pi * date.month / 12)
        noise = np.random.normal(1, 0.1)
        units_sold = max(0, int(base_sales[cat] * seasonality * noise))
        revenue = units_sold * np.random.uniform(500, 2000)
        sales_records.append({'Date': date, 'Category': cat, 'Units_Sold': units_sold, 'Revenue': revenue})

df_sales = pd.DataFrame(sales_records)
df_sales['Month'] = df_sales['Date'].dt.to_period('M')
df_sales['Quarter'] = df_sales['Date'].dt.to_period('Q')

# --- Supplier Performance Dataset ---
supplier_data = []
for sup in suppliers:
    for month in pd.period_range('2024-01', '2024-12', freq='M'):
        orders = np.random.randint(20, 80)
        on_time = int(orders * np.random.uniform(0.65, 0.98))
        defect_rate = round(np.random.uniform(0.5, 8.0), 2)
        lead_time_actual = np.random.randint(7, 21)
        lead_time_promised = 14
        supplier_data.append({
            'Supplier': sup,
            'Month': month,
            'Total_Orders': orders,
            'On_Time_Deliveries': on_time,
            'Defect_Rate_Pct': defect_rate,
            'Actual_Lead_Time': lead_time_actual,
            'Promised_Lead_Time': lead_time_promised
        })

df_sup = pd.DataFrame(supplier_data)
df_sup['OTD_Rate'] = (df_sup['On_Time_Deliveries'] / df_sup['Total_Orders'] * 100).round(2)
df_sup['Lead_Time_Variance'] = df_sup['Actual_Lead_Time'] - df_sup['Promised_Lead_Time']

print("\n✅ Data Generated Successfully")
print(f"   → Inventory Records: {len(df_inv)}")
print(f"   → Sales Records:     {len(df_sales)}")
print(f"   → Supplier Records:  {len(df_sup)}")

# ─── STEP 2: BUSINESS KPI CALCULATIONS ───────────────────────────
print("\n" + "─" * 60)
print("SECTION 1: KEY PERFORMANCE INDICATORS")
print("─" * 60)

total_inv_value = df_inv['Inventory_Value'].sum()
total_holding_cost = df_inv['Holding_Cost_Total'].sum()
high_risk_skus = len(df_inv[df_inv['Stockout_Risk'] == 'High'])
slow_moving_skus = len(df_inv[df_inv['Movement_Type'] == 'Slow'])
total_revenue_ytd = df_sales['Revenue'].sum()

print(f"\n📦 INVENTORY KPIs:")
print(f"   Total Inventory Value:    ₹{total_inv_value:,.0f}")
print(f"   Monthly Holding Cost:     ₹{total_holding_cost:,.0f}")
print(f"   High Stockout Risk SKUs:  {high_risk_skus} ({high_risk_skus}%)")
print(f"   Slow-Moving SKUs:         {slow_moving_skus} ({slow_moving_skus}%)")
print(f"\n💰 SALES KPIs:")
print(f"   Total Revenue YTD:        ₹{total_revenue_ytd:,.0f}")
avg_monthly_rev = df_sales.groupby('Month')['Revenue'].sum().mean()
print(f"   Avg Monthly Revenue:      ₹{avg_monthly_rev:,.0f}")

# ─── STEP 3: STOCKOUT RISK ANALYSIS ───────────────────────────────
print("\n" + "─" * 60)
print("SECTION 2: STOCKOUT RISK ANALYSIS")
print("─" * 60)

risk_summary = df_inv.groupby(['Category', 'Stockout_Risk']).size().unstack(fill_value=0)
print("\nStockout Risk by Category:")
print(risk_summary)

high_risk_detail = df_inv[df_inv['Stockout_Risk'] == 'High'][['SKU', 'Category', 'Current_Stock', 'Days_of_Stock', 'Avg_Daily_Sales']].head(10)
print("\nTop 10 High-Risk SKUs:")
print(high_risk_detail.to_string(index=False))

# ─── STEP 4: SUPPLIER SCORECARD ───────────────────────────────────
print("\n" + "─" * 60)
print("SECTION 3: SUPPLIER SCORECARD")
print("─" * 60)

supplier_scorecard = df_sup.groupby('Supplier').agg(
    Avg_OTD_Rate=('OTD_Rate', 'mean'),
    Avg_Defect_Rate=('Defect_Rate_Pct', 'mean'),
    Avg_Lead_Time_Variance=('Lead_Time_Variance', 'mean'),
    Total_Orders=('Total_Orders', 'sum')
).round(2)
supplier_scorecard['Performance_Score'] = (
    supplier_scorecard['Avg_OTD_Rate'] * 0.5 -
    supplier_scorecard['Avg_Defect_Rate'] * 3 -
    supplier_scorecard['Avg_Lead_Time_Variance'] * 2
).round(2)
supplier_scorecard['Rating'] = supplier_scorecard['Performance_Score'].apply(
    lambda x: '⭐⭐⭐ Excellent' if x > 40 else ('⭐⭐ Good' if x > 30 else '⭐ Needs Improvement')
)
print("\nSupplier Performance Scorecard:")
print(supplier_scorecard.to_string())

# ─── STEP 5: VISUALIZATIONS ───────────────────────────────────────
fig = plt.figure(figsize=(20, 16))
fig.suptitle('Supply Chain & Inventory Optimization Dashboard\nBusiness Analyst: Marmik Vyas',
             fontsize=16, fontweight='bold', y=0.98)

# Plot 1: Stockout Risk Distribution
ax1 = fig.add_subplot(3, 3, 1)
risk_counts = df_inv['Stockout_Risk'].value_counts()
colors_risk = [COLORS['danger'], COLORS['warning'], COLORS['success']]
wedges, texts, autotexts = ax1.pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%',
                                    colors=colors_risk, startangle=90)
ax1.set_title('Stockout Risk Distribution', fontweight='bold', fontsize=11)

# Plot 2: Movement Type by Category
ax2 = fig.add_subplot(3, 3, 2)
move_cat = df_inv.groupby(['Category', 'Movement_Type']).size().unstack(fill_value=0)
move_cat.plot(kind='bar', ax=ax2, color=[COLORS['success'], COLORS['primary'], COLORS['warning']])
ax2.set_title('SKU Movement Type by Category', fontweight='bold', fontsize=11)
ax2.set_xlabel('')
ax2.tick_params(axis='x', rotation=30)
ax2.legend(fontsize=8)

# Plot 3: Monthly Revenue Trend
ax3 = fig.add_subplot(3, 3, 3)
monthly_rev = df_sales.groupby('Month')['Revenue'].sum().reset_index()
monthly_rev['Month_Str'] = monthly_rev['Month'].astype(str)
ax3.plot(monthly_rev['Month_Str'], monthly_rev['Revenue'] / 1e6, color=COLORS['primary'],
         linewidth=2.5, marker='o', markersize=5)
ax3.fill_between(range(len(monthly_rev)), monthly_rev['Revenue'] / 1e6, alpha=0.2, color=COLORS['primary'])
ax3.set_title('Monthly Revenue Trend (₹M)', fontweight='bold', fontsize=11)
ax3.set_xticks(range(0, 12, 2))
ax3.set_xticklabels(monthly_rev['Month_Str'].iloc[::2], rotation=30, fontsize=8)
ax3.set_xlabel('')

# Plot 4: Supplier OTD Rate
ax4 = fig.add_subplot(3, 3, 4)
sup_otd = supplier_scorecard['Avg_OTD_Rate'].sort_values(ascending=False)
bars = ax4.barh(sup_otd.index, sup_otd.values,
                color=[COLORS['success'] if v >= 85 else COLORS['warning'] if v >= 75 else COLORS['danger'] for v in sup_otd.values])
ax4.axvline(85, color='red', linestyle='--', linewidth=1.5, label='Target: 85%')
ax4.set_title('Supplier On-Time Delivery Rate (%)', fontweight='bold', fontsize=11)
ax4.set_xlim(0, 100)
ax4.legend(fontsize=9)
for i, (v, bar) in enumerate(zip(sup_otd.values, bars)):
    ax4.text(v + 0.5, bar.get_y() + bar.get_height()/2, f'{v:.1f}%', va='center', fontsize=9)

# Plot 5: Inventory Value by Category
ax5 = fig.add_subplot(3, 3, 5)
inv_cat = df_inv.groupby('Category')['Inventory_Value'].sum().sort_values(ascending=False)
bars5 = ax5.bar(inv_cat.index, inv_cat.values / 1e6, color=COLORS['primary'])
ax5.set_title('Inventory Value by Category (₹M)', fontweight='bold', fontsize=11)
ax5.tick_params(axis='x', rotation=30)
for bar in bars5:
    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'₹{bar.get_height():.1f}M', ha='center', fontsize=8)

# Plot 6: Revenue by Category (stacked area)
ax6 = fig.add_subplot(3, 3, 6)
cat_monthly = df_sales.groupby(['Month', 'Category'])['Revenue'].sum().unstack(fill_value=0)
cat_monthly.index = [str(m) for m in cat_monthly.index]
cat_colors = [COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning'], COLORS['neutral']]
ax6.stackplot(range(len(cat_monthly)), [cat_monthly[c] / 1e6 for c in cat_monthly.columns],
              labels=cat_monthly.columns, colors=cat_colors, alpha=0.8)
ax6.set_title('Revenue by Category - Stacked (₹M)', fontweight='bold', fontsize=11)
ax6.legend(loc='upper left', fontsize=7)
ax6.set_xticks(range(0, 12, 3))
ax6.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])

# Plot 7: Supplier Defect Rate
ax7 = fig.add_subplot(3, 3, 7)
sup_defect = supplier_scorecard['Avg_Defect_Rate'].sort_values()
bars7 = ax7.barh(sup_defect.index, sup_defect.values,
                  color=[COLORS['success'] if v < 3 else COLORS['warning'] if v < 5 else COLORS['danger'] for v in sup_defect.values])
ax7.axvline(3, color='red', linestyle='--', linewidth=1.5, label='Target: <3%')
ax7.set_title('Supplier Defect Rate (%)', fontweight='bold', fontsize=11)
ax7.legend(fontsize=9)

# Plot 8: Days of Stock Distribution
ax8 = fig.add_subplot(3, 3, 8)
ax8.hist(df_inv['Days_of_Stock'], bins=20, color=COLORS['primary'], edgecolor='white', alpha=0.85)
ax8.axvline(7, color='red', linestyle='--', linewidth=2, label='Critical: 7 days')
ax8.axvline(14, color='orange', linestyle='--', linewidth=2, label='Reorder: 14 days')
ax8.set_title('Days of Stock Distribution', fontweight='bold', fontsize=11)
ax8.set_xlabel('Days of Stock')
ax8.legend(fontsize=9)

# Plot 9: Supplier Performance Scores
ax9 = fig.add_subplot(3, 3, 9)
perf_scores = supplier_scorecard['Performance_Score'].sort_values(ascending=False)
bar_colors = [COLORS['success'] if v > 40 else COLORS['warning'] if v > 30 else COLORS['danger'] for v in perf_scores.values]
bars9 = ax9.bar(perf_scores.index, perf_scores.values, color=bar_colors)
ax9.set_title('Overall Supplier Performance Score', fontweight='bold', fontsize=11)
ax9.tick_params(axis='x', rotation=30)
for bar in bars9:
    ax9.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{bar.get_height():.1f}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('/home/claude/projects/1_supply_chain/supply_chain_dashboard.png', dpi=150, bbox_inches='tight')
plt.close()
print("\n✅ Dashboard saved: supply_chain_dashboard.png")

# ─── STEP 6: EXPORT DATA FOR POWER BI ────────────────────────────
df_inv.to_csv('/home/claude/projects/1_supply_chain/inventory_data.csv', index=False)
df_sales.to_csv('/home/claude/projects/1_supply_chain/sales_data.csv', index=False)
df_sup.to_csv('/home/claude/projects/1_supply_chain/supplier_data.csv', index=False)
supplier_scorecard.to_csv('/home/claude/projects/1_supply_chain/supplier_scorecard.csv')
print("✅ CSV files exported for Power BI: inventory_data.csv, sales_data.csv, supplier_data.csv")

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE — See dashboard PNG + CSV files for Power BI")
print("=" * 60)
