import os
import pandas as pd
import numpy as np

def load_data(filepath=None):
    """
    Loads raw CSV data from standard location or specified filepath.
    """
    if filepath is None:
        possible_paths = [
            os.path.join('data', 'data.csv'),
            'data.csv',
            os.path.join(os.path.dirname(__file__), '..', 'data', 'data.csv'),
            os.path.join(os.path.dirname(__file__), '..', 'data.csv')
        ]
        for p in possible_paths:
            if os.path.exists(p):
                filepath = p
                break
    
    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset data.csv not found at path: {filepath}")
    
    df = pd.read_csv(filepath)
    return df

def clean_data(df):
    """
    Cleans raw real estate dataset:
    - Removes duplicate rows
    - Filters out invalid non-positive prices
    - Converts date strings to datetime objects
    - Enforces appropriate numeric data types
    """
    df = df.copy()
    
    # Remove duplicate records
    df = df.drop_duplicates()
    
    # Filter out invalid prices (price <= 0)
    df = df[df['price'] > 0]
    
    # Parse date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['year_sold'] = df['date'].dt.year
    df['month_sold'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B %Y')
    df['date_only'] = df['date'].dt.date
    
    # Enforce numeric types
    numeric_cols = [
        'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 
        'floors', 'waterfront', 'view', 'condition', 'sqft_above', 
        'sqft_basement', 'yr_built', 'yr_renovated'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Clean text columns
    text_cols = ['street', 'city', 'statezip', 'country']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            
    return df

def apply_filters(df, filters):
    """
    Filters dataframe dynamically based on dictionary of URL query parameters.
    """
    filtered = df.copy()
    if not filters:
        return filtered
        
    city = filters.get('city')
    if city and city != 'All':
        filtered = filtered[filtered['city'] == city]
        
    bedrooms = filters.get('bedrooms')
    if bedrooms and bedrooms != 'All':
        try:
            filtered = filtered[filtered['bedrooms'] == float(bedrooms)]
        except ValueError:
            pass
            
    bathrooms = filters.get('bathrooms')
    if bathrooms and bathrooms != 'All':
        try:
            filtered = filtered[filtered['bathrooms'] == float(bathrooms)]
        except ValueError:
            pass

    condition = filters.get('condition')
    if condition and condition != 'All':
        try:
            filtered = filtered[filtered['condition'] == int(condition)]
        except ValueError:
            pass
            
    waterfront = filters.get('waterfront')
    if waterfront and waterfront != 'All':
        try:
            filtered = filtered[filtered['waterfront'] == int(waterfront)]
        except ValueError:
            pass

    min_price = filters.get('min_price')
    if min_price and min_price != '' and min_price is not None:
        try:
            filtered = filtered[filtered['price'] >= float(min_price)]
        except ValueError:
            pass

    max_price = filters.get('max_price')
    if max_price and max_price != '' and max_price is not None:
        try:
            filtered = filtered[filtered['price'] <= float(max_price)]
        except ValueError:
            pass
            
    search = filters.get('search')
    if search and search.strip():
        s = search.strip().lower()
        filtered = filtered[
            filtered['street'].str.lower().str.contains(s) |
            filtered['city'].str.lower().str.contains(s) |
            filtered['statezip'].str.lower().str.contains(s)
        ]

    return filtered

def get_kpis(df):
    """
    Computes key performance indicator metrics.
    """
    if len(df) == 0:
        return {
            'total_properties': 0,
            'avg_price': 0.0,
            'median_price': 0.0,
            'max_price': 0.0,
            'min_price': 0.0,
            'avg_sqft': 0.0,
            'avg_bedrooms': 0.0
        }
        
    return {
        'total_properties': int(len(df)),
        'avg_price': float(df['price'].mean()),
        'median_price': float(df['price'].median()),
        'max_price': float(df['price'].max()),
        'min_price': float(df['price'].min()),
        'avg_sqft': float(df['sqft_living'].mean()),
        'avg_bedrooms': float(df['bedrooms'].mean())
    }

def get_price_statistics(df):
    """
    Returns descriptive statistics of property prices.
    """
    if len(df) == 0:
        return {
            'count': 0, 'mean': 0, 'std': 0, 'min': 0, 
            '25%': 0, '50%': 0, '75%': 0, 'max': 0, 'skewness': 0
        }
    stats = df['price'].describe().to_dict()
    stats['skewness'] = float(df['price'].skew())
    return stats

def get_city_analysis(df):
    """
    Groups properties by city and calculates aggregated statistics.
    """
    if len(df) == 0:
        return pd.DataFrame(columns=['city', 'count', 'avg_price', 'median_price', 'min_price', 'max_price', 'price_range'])
    city_group = df.groupby('city').agg(
        count=('price', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median'),
        min_price=('price', 'min'),
        max_price=('price', 'max')
    ).reset_index()
    city_group['price_range'] = city_group['max_price'] - city_group['min_price']
    return city_group.sort_values(by='avg_price', ascending=False)

def get_bedroom_analysis(df):
    """
    Groups properties by bedroom count.
    """
    if len(df) == 0:
        return pd.DataFrame(columns=['bedrooms', 'count', 'avg_price', 'median_price'])
    bed_group = df.groupby('bedrooms').agg(
        count=('price', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median')
    ).reset_index()
    return bed_group.sort_values(by='bedrooms')

def get_bathroom_analysis(df):
    """
    Groups properties by bathroom count.
    """
    if len(df) == 0:
        return pd.DataFrame(columns=['bathrooms', 'count', 'avg_price', 'median_price'])
    bath_group = df.groupby('bathrooms').agg(
        count=('price', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median')
    ).reset_index()
    return bath_group.sort_values(by='bathrooms')

def get_condition_analysis(df):
    """
    Groups properties by condition score (1 to 5).
    """
    if len(df) == 0:
        return pd.DataFrame(columns=['condition', 'count', 'avg_price', 'median_price'])
    cond_group = df.groupby('condition').agg(
        count=('price', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median')
    ).reset_index()
    return cond_group.sort_values(by='condition')

def get_year_analysis(df):
    """
    Groups properties by construction year (yr_built).
    """
    if len(df) == 0:
        return pd.DataFrame(columns=['yr_built', 'count', 'avg_price', 'median_price'])
    yr_group = df.groupby('yr_built').agg(
        count=('price', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median')
    ).reset_index()
    return yr_group.sort_values(by='yr_built')

def get_waterfront_analysis(df):
    """
    Analyzes waterfront vs non-waterfront properties.
    """
    if len(df) == 0:
        return pd.DataFrame(columns=['waterfront', 'label', 'count', 'avg_price', 'median_price'])
    wf_group = df.groupby('waterfront').agg(
        count=('price', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median')
    ).reset_index()
    wf_group['label'] = wf_group['waterfront'].map({0: 'No Waterfront', 1: 'Waterfront'})
    return wf_group

def get_renovation_analysis(df):
    """
    Analyzes renovated vs non-renovated properties (yr_renovated > 0).
    """
    if len(df) == 0:
        return pd.DataFrame(columns=['is_renovated', 'count', 'avg_price', 'median_price'])
    df_temp = df.copy()
    df_temp['is_renovated'] = np.where(df_temp['yr_renovated'] > 0, 'Renovated', 'Not Renovated')
    ren_group = df_temp.groupby('is_renovated').agg(
        count=('price', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median')
    ).reset_index()
    return ren_group

def get_correlation_analysis(df):
    """
    Computes correlation matrix between numerical features.
    """
    numeric_cols = [
        'price', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot',
        'floors', 'waterfront', 'view', 'condition', 'sqft_above',
        'sqft_basement', 'yr_built', 'yr_renovated'
    ]
    available_cols = [c for c in numeric_cols if c in df.columns]
    if len(df) == 0 or len(available_cols) == 0:
        return pd.DataFrame()
    return df[available_cols].corr()

def get_date_analysis(df):
    """
    Analyzes sales/listing trends over time.
    """
    if len(df) == 0 or 'date' not in df.columns:
        return pd.DataFrame(columns=['date_only', 'count', 'avg_price', 'median_price'])
    date_group = df.groupby('date_only').agg(
        count=('price', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median')
    ).reset_index()
    return date_group.sort_values(by='date_only')

def get_insights(df):
    """
    Generates dynamic data-driven insight statements based on active dataframe.
    """
    if len(df) == 0:
        return ["No property records match the selected filter criteria."]
        
    kpis = get_kpis(df)
    city_analysis = get_city_analysis(df)
    waterfront_analysis = get_waterfront_analysis(df)
    renovation_analysis = get_renovation_analysis(df)
    
    top_city = city_analysis.iloc[0]['city'] if len(city_analysis) > 0 else 'N/A'
    top_city_avg = city_analysis.iloc[0]['avg_price'] if len(city_analysis) > 0 else 0.0
    
    top_volume_city = city_analysis.sort_values(by='count', ascending=False).iloc[0]['city'] if len(city_analysis) > 0 else 'N/A'
    top_volume_count = city_analysis.sort_values(by='count', ascending=False).iloc[0]['count'] if len(city_analysis) > 0 else 0
    
    wf_1_avg = 0.0
    wf_0_avg = 0.0
    for _, row in waterfront_analysis.iterrows():
        if row['waterfront'] == 1:
            wf_1_avg = row['avg_price']
        elif row['waterfront'] == 0:
            wf_0_avg = row['avg_price']
            
    ren_avg = 0.0
    non_ren_avg = 0.0
    for _, row in renovation_analysis.iterrows():
        if row['is_renovated'] == 'Renovated':
            ren_avg = row['avg_price']
        elif row['is_renovated'] == 'Not Renovated':
            non_ren_avg = row['avg_price']

    skewness = df['price'].skew() if len(df) > 1 else 0
    skew_desc = "heavily right-skewed due to luxury real estate outliers" if skewness > 1 else "moderately skewed"

    insights = [
        f"The current selection contains {kpis['total_properties']:,} properties.",
        f"The average observed house price is ${kpis['avg_price']:,.2f}, while the median price is ${kpis['median_price']:,.2f}.",
        f"The overall house price distribution is {skew_desc} (skewness coefficient: {skewness:.2f}).",
        f"Properties in this dataset have an average living area of {kpis['avg_sqft']:,.0f} sqft with an average of {kpis['avg_bedrooms']:.2f} bedrooms.",
        f"The city with the highest average observed price is {top_city} at ${top_city_avg:,.2f} per property.",
        f"{top_volume_city} has the highest concentration of property listings with {top_volume_count:,} properties.",
        f"Waterfront properties have a higher average observed price (${wf_1_avg:,.2f}) compared to non-waterfront properties (${wf_0_avg:,.2f}) in this dataset.",
        f"Renovated properties have an average observed price of ${ren_avg:,.2f} versus ${non_ren_avg:,.2f} for non-renovated properties."
    ]
    return insights
