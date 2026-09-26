import os
import time
import pandas as pd
from flask import Flask, render_template, request

from analysis.data_analysis import (
    load_data, clean_data, apply_filters, get_kpis,
    get_price_statistics, get_city_analysis, get_bedroom_analysis,
    get_bathroom_analysis, get_condition_analysis, get_year_analysis,
    get_waterfront_analysis, get_renovation_analysis, get_correlation_analysis,
    get_date_analysis, get_insights
)
from utils.chart_generator import generate_all_charts

app = Flask(__name__)

# Global dataset cache
raw_df = None
cleaned_df = None

def init_dataset():
    global raw_df, cleaned_df
    try:
        raw_df = load_data()
        cleaned_df = clean_data(raw_df)
        print(f"Dataset loaded successfully: {len(cleaned_df)} records after cleaning.")
        # Generate initial default charts
        generate_all_charts(cleaned_df)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        raw_df = pd.DataFrame()
        cleaned_df = pd.DataFrame()

# Initialize data on app start
init_dataset()

def extract_filters_from_request(req):
    return {
        'city': req.args.get('city', 'All'),
        'bedrooms': req.args.get('bedrooms', 'All'),
        'bathrooms': req.args.get('bathrooms', 'All'),
        'condition': req.args.get('condition', 'All'),
        'waterfront': req.args.get('waterfront', 'All'),
        'min_price': req.args.get('min_price', ''),
        'max_price': req.args.get('max_price', ''),
        'search': req.args.get('search', '')
    }

def get_filter_options():
    if cleaned_df is None or len(cleaned_df) == 0:
        return {
            'cities': [],
            'bedrooms': [],
            'bathrooms': [],
            'conditions': [1, 2, 3, 4, 5],
            'waterfronts': [0, 1]
        }
    return {
        'cities': sorted(cleaned_df['city'].dropna().unique().tolist()),
        'bedrooms': [int(b) if float(b).is_integer() else float(b) for b in sorted(cleaned_df['bedrooms'].dropna().unique().tolist())],
        'bathrooms': sorted(cleaned_df['bathrooms'].dropna().unique().tolist()),
        'conditions': sorted(cleaned_df['condition'].dropna().unique().tolist()),
        'waterfronts': [0, 1]
    }

@app.context_processor
def utility_processor():
    def format_currency(value):
        try:
            return f"${float(value):,.2f}"
        except (ValueError, TypeError):
            return "$0.00"

    def format_number(value, decimals=0):
        try:
            if decimals == 0:
                return f"{int(round(float(value))):,}"
            return f"{float(value):,.{decimals}f}"
        except (ValueError, TypeError):
            return "0"

    return dict(format_currency=format_currency, format_number=format_number)

@app.route('/')
def index():
    filters = extract_filters_from_request(request)
    filtered_df = apply_filters(cleaned_df, filters)
    
    # Check if custom filter is active (not default)
    is_filtered = any([
        filters['city'] != 'All',
        filters['bedrooms'] != 'All',
        filters['bathrooms'] != 'All',
        filters['condition'] != 'All',
        filters['waterfront'] != 'All',
        bool(filters['min_price']),
        bool(filters['max_price'])
    ])
    
    # Generate dynamic charts for filtered data
    chart_version = int(time.time())
    generate_all_charts(filtered_df)
    
    kpis = get_kpis(filtered_df)
    insights = get_insights(filtered_df)
    filter_opts = get_filter_options()
    
    return render_template(
        'index.html',
        kpis=kpis,
        insights=insights,
        filters=filters,
        filter_opts=filter_opts,
        is_filtered=is_filtered,
        chart_version=chart_version,
        active_page='dashboard'
    )

@app.route('/properties')
def properties():
    filters = extract_filters_from_request(request)
    filtered_df = apply_filters(cleaned_df, filters)
    
    # Pagination
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        page = 1
        
    per_page = 25
    total_items = len(filtered_df)
    total_pages = max(1, (total_items + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))
    
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    page_df = filtered_df.iloc[start_idx:end_idx].copy()
    
    # Format date string for template
    if not page_df.empty and 'date' in page_df.columns:
        page_df['formatted_date'] = page_df['date'].dt.strftime('%Y-%m-%d')
    else:
        page_df['formatted_date'] = ''
        
    properties_list = page_df.to_dict(orient='records')
    filter_opts = get_filter_options()
    
    return render_template(
        'properties.html',
        properties=properties_list,
        filters=filters,
        filter_opts=filter_opts,
        page=page,
        total_pages=total_pages,
        total_items=total_items,
        per_page=per_page,
        start_item=start_idx + 1 if total_items > 0 else 0,
        end_item=min(end_idx, total_items),
        active_page='properties'
    )

@app.route('/analysis')
def analysis():
    filters = extract_filters_from_request(request)
    filtered_df = apply_filters(cleaned_df, filters)
    
    chart_version = int(time.time())
    generate_all_charts(filtered_df)
    
    stats = get_price_statistics(filtered_df)
    city_df = get_city_analysis(filtered_df)
    bedroom_df = get_bedroom_analysis(filtered_df)
    bathroom_df = get_bathroom_analysis(filtered_df)
    condition_df = get_condition_analysis(filtered_df)
    year_df = get_year_analysis(filtered_df)
    waterfront_df = get_waterfront_analysis(filtered_df)
    renovation_df = get_renovation_analysis(filtered_df)
    date_df = get_date_analysis(filtered_df)
    
    filter_opts = get_filter_options()
    insights = get_insights(filtered_df)

    return render_template(
        'analysis.html',
        stats=stats,
        city_table=city_df.to_dict(orient='records'),
        bedroom_table=bedroom_df.to_dict(orient='records'),
        bathroom_table=bathroom_df.to_dict(orient='records'),
        condition_table=condition_df.to_dict(orient='records'),
        year_table=year_df.head(15).to_dict(orient='records'),
        waterfront_table=waterfront_df.to_dict(orient='records'),
        renovation_table=renovation_df.to_dict(orient='records'),
        date_table=date_df.head(10).to_dict(orient='records'),
        filters=filters,
        filter_opts=filter_opts,
        insights=insights,
        chart_version=chart_version,
        active_page='analysis'
    )

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
