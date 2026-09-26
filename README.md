# Real Estate House Price Analytics Dashboard

Subtitle: **Exploring Property Prices, Features, Locations and Market Trends**

A comprehensive, modular web application and data science dashboard designed for real estate property analysis. Built using **Python Flask**, **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**, **HTML5**, and **CSS3**.

---

## 📌 Project Overview

The **Real Estate House Price Analytics Dashboard** provides interactive exploration and statistical insights into housing market data containing approximately 4,600 property records. The project cleans the dataset, dynamically computes Key Performance Indicators (KPIs), plots Seaborn visualization charts, and presents automated data-driven insights.

---

## 📊 Dataset Structure

The dataset contains the following property fields:

| Column | Description |
| :--- | :--- |
| `date` | Date of listing / transaction |
| `price` | House sale price ($USD) |
| `bedrooms` | Number of bedrooms |
| `bathrooms` | Number of bathrooms |
| `sqft_living` | Square footage of interior living space |
| `sqft_lot` | Square footage of the land lot |
| `floors` | Number of floors/levels |
| `waterfront` | Waterfront dummy variable (0 = No, 1 = Yes) |
| `view` | View rating score |
| `condition` | Property condition rating (1 to 5) |
| `sqft_above` | Square footage of house above ground level |
| `sqft_basement` | Square footage of basement space |
| `yr_built` | Year original construction was completed |
| `yr_renovated` | Year of last renovation (0 if never renovated) |
| `street` | Street address |
| `city` | City name |
| `statezip` | State and ZIP code |
| `country` | Country |

---

## 🛠️ Technologies Used

* **Backend Framework**: Python Flask
* **Data Processing & Analytics**: Pandas, NumPy
* **Data Visualizations**: Matplotlib, Seaborn
* **Frontend Design**: HTML5, CSS3 (Vanilla CSS, CSS Grid, Flexbox)
* **Templating Engine**: Jinja2

---

## ✨ Key Features

1. **Executive KPI Dashboard**:
   * Total Properties Count
   * Average House Price ($USD)
   * Median House Price ($USD)
   * Maximum Property Listing Price
   * Average Living Area (sqft)
   * Average Bedroom Count

2. **Seaborn Data Visualizations**:
   * **Price Distribution**: Histogram + Kernel Density Estimate (KDE) curve
   * **Price vs Living Area**: Scatter plot with linear regression trend line
   * **Price by Bedrooms**: Bar chart of average property price by bedroom count
   * **Price by Bathrooms**: Trend plot of average price across bathroom counts
   * **Price by City**: Top 10 cities ranked by average property value
   * **Waterfront Comparison**: Bar comparison between waterfront and non-waterfront homes
   * **Property Condition**: Average price across condition rating scores (1-5)
   * **Construction Year Trend**: Price progression over construction years (`yr_built`)
   * **Correlation Heatmap**: Full feature correlation heatmap

3. **Dynamic Filtering**:
   * Filter dataset by City, Bedrooms, Bathrooms, Condition, Waterfront, Min Price, and Max Price.
   * All KPIs, charts, and analysis tables update dynamically based on active filters.

4. **Interactive Property Table (`/properties`)**:
   * Paginated data table displaying detailed records.
   * Instant keyword search across street address, city, and zip code.
   * Formatted currency and property numbers.

5. **Automated Business Insights**:
   * Automatically generated data statements highlighting key metrics without hard-coded statistics.

---

## 📂 Project Structure

```text
real-estate-dashboard/
│
├── app.py                      # Main Flask application & routes
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
├── data/
│   └── data.csv                # Real estate dataset
│
├── analysis/
│   └── data_analysis.py        # Data loading, cleaning, KPIs, and analysis functions
│
├── utils/
│   └── chart_generator.py      # Seaborn & Matplotlib chart generation module
│
├── templates/
│   ├── base.html               # Base Jinja2 layout template with sidebar navigation
│   ├── index.html              # Main KPI & Visualizations Dashboard
│   ├── properties.html         # Property data table with search and pagination
│   └── analysis.html           # Deep-dive statistical analysis & correlation page
│
└── static/
    ├── css/
    │   └── style.css           # Custom dark dashboard CSS styles
    │
    └── charts/                 # Auto-generated PNG visualization charts
        ├── price_distribution.png
        ├── price_by_city.png
        ├── sqft_price.png
        ├── bedrooms_price.png
        ├── bathrooms_price.png
        ├── condition_price.png
        ├── year_price.png
        ├── waterfront_price.png
        └── correlation_heatmap.png
```

---

## 🚀 Installation & Setup

1. **Clone or Download the repository**:
   Navigate to the project root directory.

2. **Install Required Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access in Browser**:
   Open your browser and navigate to:
   `http://127.0.0.1:5000`

---

## 🔮 Future Improvements

* Machine Learning model integration (Random Forest / XGBoost) for predicting house prices based on user inputs.
* Interactive client-side charting (e.g. Canvas API / Chart JS integration).
* SQL Database integration (PostgreSQL / SQLite) for large-scale data querying.
* User authentication and saved property bookmarking functionality.

---

## 👨‍🎓 Project Credits

Developed as a **BCA Capstone College Project** showcasing Python Data Science, Web Analytics, and Software Architecture.
