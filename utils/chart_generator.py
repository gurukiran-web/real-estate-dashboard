import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np

# Set consistent aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

DARK_BG = '#0f172a'
CARD_BG = '#1e293b'
TEXT_COLOR = '#f8fafc'
GRID_COLOR = '#334155'
ACCENT_BLUE = '#6366f1'
ACCENT_CYAN = '#06b6d4'
ACCENT_GREEN = '#10b981'
ACCENT_ORANGE = '#f59e0b'
ACCENT_PURPLE = '#a855f7'
ACCENT_RED = '#ef4444'

def configure_chart_style(fig, ax, title, xlabel, ylabel):
    """
    Applies custom dark/sleek styling to matplotlib figures.
    """
    fig.patch.set_facecolor(CARD_BG)
    ax.set_facecolor(CARD_BG)
    
    ax.set_title(title, color=TEXT_COLOR, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(xlabel, color='#94a3b8', fontsize=11, fontweight='semibold', labelpad=10)
    ax.set_ylabel(ylabel, color='#94a3b8', fontsize=11, fontweight='semibold', labelpad=10)
    
    ax.tick_params(colors='#94a3b8', labelsize=10)
    ax.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
        spine.set_linewidth(1)

def format_currency_axis(ax, axis='y'):
    """
    Formats axis ticks as $XXk or $X.XM currency labels.
    """
    def currency_fmt(x, pos):
        if x >= 1e6:
            return f'${x*1e-6:.1f}M'
        elif x >= 1e3:
            return f'${x*1e-3:.0f}k'
        elif x == 0:
            return '$0'
        else:
            return f'${x:.0f}'

    formatter = ticker.FuncFormatter(currency_fmt)
    if axis == 'y':
        ax.yaxis.set_major_formatter(formatter)
    else:
        ax.xaxis.set_major_formatter(formatter)

def create_no_data_chart(output_path, title):
    """
    Generates a placeholder chart when no data matches current filters.
    """
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=120)
    configure_chart_style(fig, ax, title, "", "")
    ax.text(0.5, 0.5, 'No Data Available for Selected Filters', 
            horizontalalignment='center', verticalalignment='center',
            color='#94a3b8', fontsize=14, fontweight='bold', transform=ax.transAxes)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

# 1. Price Distribution Chart
def generate_price_distribution(df, output_path):
    if len(df) == 0:
        create_no_data_chart(output_path, "House Price Distribution")
        return
        
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=130)
    
    # Clip prices for visualization if extreme max outlier present
    price_data = df['price']
    
    sns.histplot(price_data, kde=True, ax=ax, color=ACCENT_CYAN, 
                 edgecolor='#0284c7', alpha=0.6, linewidth=1)
    
    format_currency_axis(ax, axis='x')
    configure_chart_style(fig, ax, "House Price Distribution (with KDE)", "House Price ($USD)", "Number of Properties")
    
    # Add median line
    med_val = df['price'].median()
    ax.axvline(med_val, color=ACCENT_ORANGE, linestyle='--', linewidth=2, label=f'Median: ${med_val:,.0f}')
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

# 2. Price vs Living Area
def generate_price_vs_living_area(df, output_path):
    if len(df) == 0:
        create_no_data_chart(output_path, "Price vs Living Area (sqft)")
        return

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=130)
    
    # Scatter plot with regression line
    sns.regplot(data=df, x='sqft_living', y='price', ax=ax,
                scatter_kws={'color': ACCENT_BLUE, 'alpha': 0.5, 's': 25},
                line_kws={'color': ACCENT_RED, 'linewidth': 2, 'label': 'Trend Line'})
                
    format_currency_axis(ax, axis='y')
    configure_chart_style(fig, ax, "Price vs Living Area (sqft)", "Living Area (sqft)", "House Price ($USD)")
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

# 3. Bedroom Price Chart
def generate_bedroom_price_chart(df, output_path):
    if len(df) == 0:
        create_no_data_chart(output_path, "Average Price by Bedrooms")
        return

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=130)
    
    bed_df = df.groupby('bedrooms')['price'].mean().reset_index()
    
    barplot = sns.barplot(data=bed_df, x='bedrooms', y='price', ax=ax, 
                          palette='viridis', hue='bedrooms', legend=False)
                          
    format_currency_axis(ax, axis='y')
    configure_chart_style(fig, ax, "Average Price by Number of Bedrooms", "Number of Bedrooms", "Average Price ($USD)")
    
    # Value labels on bars
    for p in barplot.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            ax.annotate(f'${height*1e-3:.0f}k' if height < 1e6 else f'${height*1e-6:.2f}M',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=8.5, color=TEXT_COLOR, xytext=(0, 3),
                        textcoords='offset points')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

# 4. Bathroom Price Chart
def generate_bathroom_price_chart(df, output_path):
    if len(df) == 0:
        create_no_data_chart(output_path, "Average Price by Bathrooms")
        return

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=130)
    
    bath_df = df.groupby('bathrooms')['price'].mean().reset_index().sort_values(by='bathrooms')
    
    sns.lineplot(data=bath_df, x='bathrooms', y='price', ax=ax, 
                 color=ACCENT_GREEN, marker='o', linewidth=2.5, markersize=7)
                 
    format_currency_axis(ax, axis='y')
    configure_chart_style(fig, ax, "Average Price by Number of Bathrooms", "Number of Bathrooms", "Average Price ($USD)")

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

# 5. City Price Chart (Top 10 Cities)
def generate_city_price_chart(df, output_path):
    if len(df) == 0:
        create_no_data_chart(output_path, "Top 10 Cities by Average House Price")
        return

    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=130)
    
    city_df = df.groupby('city')['price'].mean().reset_index().sort_values(by='price', ascending=False).head(10)
    
    sns.barplot(data=city_df, y='city', x='price', ax=ax, 
                palette='mako', hue='city', legend=False)
                
    format_currency_axis(ax, axis='x')
    configure_chart_style(fig, ax, "Top 10 Cities by Average House Price", "Average Price ($USD)", "City")
    
    for p in ax.patches:
        width = p.get_width()
        if not np.isnan(width) and width > 0:
            ax.annotate(f'${width*1e-3:.0f}k' if width < 1e6 else f'${width*1e-6:.2f}M',
                        (width, p.get_y() + p.get_height() / 2.),
                        ha='left', va='center', fontsize=9, color=TEXT_COLOR, xytext=(5, 0),
                        textcoords='offset points')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

# 6. Waterfront Chart
def generate_waterfront_chart(df, output_path):
    if len(df) == 0:
        create_no_data_chart(output_path, "Waterfront vs Non-Waterfront Price Comparison")
        return

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=130)
    
    wf_df = df.copy()
    wf_df['waterfront_label'] = wf_df['waterfront'].map({0: 'No Waterfront', 1: 'Waterfront'})
    
    wf_stats = wf_df.groupby('waterfront_label')['price'].agg(['mean', 'median']).reset_index()
    
    bar_width = 0.35
    x = np.arange(len(wf_stats))
    
    ax.bar(x - bar_width/2, wf_stats['mean'], bar_width, label='Average Price', color=ACCENT_CYAN, alpha=0.85)
    ax.bar(x + bar_width/2, wf_stats['median'], bar_width, label='Median Price', color=ACCENT_PURPLE, alpha=0.85)
    
    ax.set_xticks(x)
    ax.set_xticklabels(wf_stats['waterfront_label'], color=TEXT_COLOR, fontweight='bold')
    
    format_currency_axis(ax, axis='y')
    configure_chart_style(fig, ax, "Waterfront vs Non-Waterfront Price Comparison", "Property Type", "Price ($USD)")
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    for p in ax.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            ax.annotate(f'${height*1e-3:.0f}k' if height < 1e6 else f'${height*1e-6:.2f}M',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=8.5, color=TEXT_COLOR, xytext=(0, 3),
                        textcoords='offset points')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

# 7. Condition Price Chart
def generate_condition_price_chart(df, output_path):
    if len(df) == 0:
        create_no_data_chart(output_path, "Average Price by Property Condition")
        return

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=130)
    
    cond_df = df.groupby('condition')['price'].mean().reset_index()
    
    barplot = sns.barplot(data=cond_df, x='condition', y='price', ax=ax,
                          palette='rocket', hue='condition', legend=False)
                          
    format_currency_axis(ax, axis='y')
    configure_chart_style(fig, ax, "Average Price by Property Condition Rating (1-5)", "Condition Score", "Average Price ($USD)")
    
    for p in barplot.patches:
        height = p.get_height()
        if not np.isnan(height) and height > 0:
            ax.annotate(f'${height*1e-3:.0f}k' if height < 1e6 else f'${height*1e-6:.2f}M',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, color=TEXT_COLOR, xytext=(0, 3),
                        textcoords='offset points')

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

# 8. Year Built vs Price Chart
def generate_year_price_chart(df, output_path):
    if len(df) == 0:
        create_no_data_chart(output_path, "Construction Year vs Price")
        return

    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=130)
    
    yr_df = df.groupby('yr_built')['price'].mean().reset_index()
    
    sns.lineplot(data=yr_df, x='yr_built', y='price', ax=ax, color=ACCENT_ORANGE, linewidth=2)
    
    # Smooth moving average line
    yr_df['ma'] = yr_df['price'].rolling(window=10, min_periods=1).mean()
    sns.lineplot(data=yr_df, x='yr_built', y='ma', ax=ax, color=ACCENT_RED, 
                 linewidth=2.5, linestyle='--', label='10-Yr Moving Average')

    format_currency_axis(ax, axis='y')
    configure_chart_style(fig, ax, "Average Price by Construction Year (yr_built)", "Year Built", "Average Price ($USD)")
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

# 9. Correlation Heatmap Chart
def generate_correlation_heatmap(df, output_path):
    numeric_cols = [
        'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
        'floors', 'waterfront', 'view', 'condition', 'sqft_above',
        'sqft_basement', 'yr_built', 'yr_renovated'
    ]
    avail_cols = [c for c in numeric_cols if c in df.columns]
    
    if len(df) == 0 or len(avail_cols) == 0:
        create_no_data_chart(output_path, "Correlation Heatmap")
        return

    fig, ax = plt.subplots(figsize=(9.5, 6.5), dpi=130)
    corr = df[avail_cols].corr()
    
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax,
                cbar_kws={"shrink": .8}, annot_kws={"size": 7.5}, linewidths=0.5)

    configure_chart_style(fig, ax, "Correlation Heatmap of Property Features", "", "")
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)

def generate_all_charts(df, charts_dir='static/charts'):
    """
    Generates and saves all project dashboard charts.
    """
    os.makedirs(charts_dir, exist_ok=True)
    
    generate_price_distribution(df, os.path.join(charts_dir, 'price_distribution.png'))
    generate_city_price_chart(df, os.path.join(charts_dir, 'price_by_city.png'))
    generate_price_vs_living_area(df, os.path.join(charts_dir, 'sqft_price.png'))
    generate_bedroom_price_chart(df, os.path.join(charts_dir, 'bedrooms_price.png'))
    generate_bathroom_price_chart(df, os.path.join(charts_dir, 'bathrooms_price.png'))
    generate_condition_price_chart(df, os.path.join(charts_dir, 'condition_price.png'))
    generate_year_price_chart(df, os.path.join(charts_dir, 'year_price.png'))
    generate_waterfront_chart(df, os.path.join(charts_dir, 'waterfront_price.png'))
    generate_correlation_heatmap(df, os.path.join(charts_dir, 'correlation_heatmap.png'))
