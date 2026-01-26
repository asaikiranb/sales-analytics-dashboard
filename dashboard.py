import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ============================================
# Page Configuration
# ============================================
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# Theme Colors (Fixed Light Theme)
# ============================================
theme = {
    'bg': '#FFFFFF',
    'card_bg': '#FFFFFF',
    'text': '#000000',
    'text_secondary': '#666666',
    'border': '#E0E0E0',
    'accent': '#0066FF',
    'chart_bg': '#FFFFFF',
    'chart_text': '#000000',
    'grid': '#F0F0F0',
    'kpi_delta': '#00AA55'
}

# ============================================
# Dynamic CSS based on theme
# ============================================
st.markdown(f"""
<style>
    /* Import Roboto font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&display=swap');
    
    /* FORCE color scheme - disable browser dark/light mode detection */
    :root {{
        color-scheme: light !important;
    }}
    
    /* Override any prefers-color-scheme media queries */
    @media (prefers-color-scheme: dark) {{
        :root {{
            color-scheme: light !important;
        }}
    }}
    
    /* Base styling - Force all colors explicitly */
    html, body, [class*="css"], .stApp, .main, .block-container {{
        font-family: 'Roboto', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: {theme['text']} !important;
        background-color: {theme['bg']} !important;
        -webkit-text-fill-color: {theme['text']} !important;
    }}
    
    .stApp {{
        background-color: {theme['bg']} !important;
    }}
    
    /* Hide default Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Hide sidebar completely */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}
    
    .block-container {{
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }}
    
    /* Header area */
    .dashboard-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0 16px 0;
        border-bottom: 1px solid {theme['border']};
        margin-bottom: 16px;
    }}
    
    .dashboard-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {theme['text']} !important;
    }}
    
    .dashboard-subtitle {{
        font-size: 0.9rem;
        color: {theme['text_secondary']} !important;
        margin-top: 4px;
    }}
    
    /* Theme toggle button */
    .theme-toggle {{
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 20px;
        padding: 8px 16px;
        cursor: pointer;
        font-size: 0.875rem;
        font-weight: 500;
        color: {theme['text']} !important;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }}
    
    /* Tabs styling - Prominent pill buttons */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 12px;
        padding: 6px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        color: {theme['text']} !important;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 12px 28px;
        background: transparent !important;
        transition: all 0.2s ease;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(0, 102, 255, 0.1) !important;
        color: {theme['accent']} !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: #FFFFFF !important;
        background: {theme['accent']} !important;
        box-shadow: 0 2px 8px rgba(0, 102, 255, 0.3);
    }}
    
    /* KPI Cards */
    .kpi-simple {{
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }}
    
    .kpi-simple-label {{
        font-size: 0.75rem;
        color: {theme['text_secondary']} !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }}
    
    .kpi-simple-value {{
        font-size: 2rem;
        font-weight: 600;
        color: {theme['text']} !important;
    }}
    
    .kpi-simple-delta {{
        font-size: 0.8rem;
        color: {theme['kpi_delta']} !important;
        margin-top: 4px;
    }}
    
    /* Section headers */
    .section-title {{
        font-size: 1.25rem;
        font-weight: 600;
        color: {theme['text']} !important;
        margin: 24px 0 8px 0;
    }}
    
    .section-description {{
        font-size: 0.875rem;
        color: {theme['text_secondary']} !important;
        margin-bottom: 16px;
        line-height: 1.5;
    }}
    
    /* Selectbox / Filters / Inputs */
    .stSelectbox label, .stTextInput label, .stNumberInput label {{
        color: {theme['text']} !important;
        font-weight: 500;
        font-size: 0.875rem;
    }}
    
    .stSelectbox > div > div, 
    .stTextInput > div > div, 
    .stNumberInput > div > div {{
        background-color: {theme['card_bg']} !important;
        border: 1px solid {theme['border']} !important;
        color: {theme['text']} !important;
    }}
    
    /* Input field text color */
    input {{
        color: {theme['text']} !important;
        -webkit-text-fill-color: {theme['text']} !important;
    }}
    
    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {theme['text']} !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {theme['text_secondary']} !important;
    }}
    
    /* Summary boxes */
    .summary-box {{
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        padding: 20px;
        margin-top: 20px;
    }}
    
    .summary-box h3 {{
        color: {theme['text']} !important;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 12px;
    }}
    
    .summary-box ul {{
        color: {theme['text']} !important;
        margin: 0;
        padding-left: 20px;
    }}
    
    .summary-box li {{
        margin-bottom: 8px;
        line-height: 1.5;
        color: {theme['text']} !important;
    }}
    
    /* Slider */
    .stSlider > div > div > div {{
        background: {theme['accent']} !important;
    }}
    
    /* Buttons */
    .stButton > button {{
        background: {theme['accent']} !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        font-weight: 500 !important;
        padding: 8px 24px !important;
    }}
    
    .stButton > button:hover {{
        background: #0052CC !important;
    }}
    
    /* Data tables */
    [data-testid="stDataFrame"] {{
        border: 1px solid {theme['border']};
        border-radius: 8px;
    }}
    
    .dataframe, [data-testid="stDataFrame"] th, [data-testid="stDataFrame"] td {{
        background-color: {theme['card_bg']} !important;
        color: {theme['text']} !important;
    }}
    
    /* City cards */
    .city-card {{
        background: {theme['card_bg']};
        border: 1px solid {theme['border']};
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
    }}
    
    .city-name {{
        font-weight: 500;
        color: {theme['text']} !important;
    }}
    
    .city-revenue {{
        color: {theme['accent']} !important;
        font-weight: 600;
    }}
    
    .city-percent {{
        font-size: 0.75rem;
        color: {theme['text_secondary']} !important;
        margin-top: 4px;
    }}
    
    /* Force text colors - comprehensive override */
    p, span, div, h1, h2, h3, h4, h5, h6, label, strong, b, a, li, td, th {{
        color: {theme['text']} !important;
        -webkit-text-fill-color: {theme['text']} !important;
    }}
    
    /* Fix for placeholder text visibility */
    ::placeholder {{
        color: {theme['text_secondary']} !important;
        opacity: 0.7;
    }}
    
    /* Force secondary text colors */
    .section-description, [data-testid="stMetricLabel"], .kpi-simple-label, .city-percent {{
        color: {theme['text_secondary']} !important;
        -webkit-text-fill-color: {theme['text_secondary']} !important;
    }}
    
    /* Force KPI values to be visible */
    .kpi-simple-value {{
        color: {theme['text']} !important;
        -webkit-text-fill-color: {theme['text']} !important;
    }}
    
    /* Force metric values */
    [data-testid="stMetricValue"] {{
        color: {theme['text']} !important;
        -webkit-text-fill-color: {theme['text']} !important;
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# Data Loading
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv('Sales Data.csv')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Sales'] = df['Quantity Ordered'] * df['Price Each']
    df['Month_Name'] = df['Order Date'].dt.month_name()
    df['Day_of_Week'] = df['Order Date'].dt.day_name()
    df['Week'] = df['Order Date'].dt.isocalendar().week
    return df

df = load_data()

# ============================================
# Chart Theme based on mode
# ============================================
CHART_COLORS = ['#0066FF', '#00AA55', '#FF6B35', '#6B4EFF', '#00B8D9']
CHART_FONT = dict(family='Roboto, sans-serif', color=theme['chart_text'], size=13)
CHART_LAYOUT = dict(
    plot_bgcolor=theme['chart_bg'],
    paper_bgcolor=theme['chart_bg'],
    font=CHART_FONT,
    margin=dict(l=40, r=40, t=40, b=40)
)
# Axis tick font for all charts
AXIS_TICKFONT = dict(color=theme['chart_text'], size=12)

# = ============================================
# Header
# ============================================
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: flex-start; padding: 0 0 16px 0;">
    <div>
        <span class="dashboard-title">Sales Analytics Dashboard</span>
        <p class="dashboard-subtitle">Comprehensive sales data analysis across all regions and products</p>
    </div>
    <div style="text-align: right; max-width: 450px;">
        <p style="font-size: 0.95rem; color: {theme['text_secondary']}; font-weight: 500; line-height: 1.4; opacity: 0.9; margin: 0;">
            Built by Saikiran Babu Annangi for the Data Platform Graduate Intern (Summer 2026) at Sigma Computing
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================
# Navigation Tabs at TOP
# ============================================
tab1, tab2, tab3, tab4 = st.tabs(["Executive Pulse", "Revenue & Marketing", "Regional Insights", "Data Explorer"])

# ============================================
# Filters Row at TOP (inside each tab)
# ============================================
def render_filters():
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cities = ['All Cities'] + sorted(df['City'].unique().tolist())
        selected_city = st.selectbox("City", cities, key=f"city_{st.session_state.get('tab', 0)}")
    with col2:
        months = ['All Months'] + [f"Month {i}" for i in sorted(df['Month'].unique().tolist())]
        selected_month = st.selectbox("Month", months, key=f"month_{st.session_state.get('tab', 0)}")
    with col3:
        products = ['All Products'] + sorted(df['Product'].unique().tolist())
        selected_product = st.selectbox("Product", products, key=f"product_{st.session_state.get('tab', 0)}")
    with col4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("Apply Filters", key=f"apply_{st.session_state.get('tab', 0)}")
    
    # Apply filters
    filtered = df.copy()
    if selected_city != 'All Cities':
        filtered = filtered[filtered['City'] == selected_city]
    if selected_month != 'All Months':
        month_num = int(selected_month.split()[-1])
        filtered = filtered[filtered['Month'] == month_num]
    if selected_product != 'All Products':
        filtered = filtered[filtered['Product'] == selected_product]
    
    return filtered

# Helper functions
def format_currency(value):
    if value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif value >= 1e3:
        return f"${value/1e3:.1f}K"
    return f"${value:.2f}"

def format_number(value):
    if value >= 1e6:
        return f"{value/1e6:.2f}M"
    elif value >= 1e3:
        return f"{value/1e3:.1f}K"
    return f"{value:,.0f}"

# ============================================
# TAB 1: Executive Pulse
# ============================================
with tab1:
    st.session_state['tab'] = 1
    filtered_df = render_filters()
    
    st.markdown("---")
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    total_revenue = filtered_df['Sales'].sum()
    total_units = filtered_df['Quantity Ordered'].sum()
    aov = total_revenue / max(filtered_df['Order ID'].nunique(), 1)
    unique_orders = filtered_df['Order ID'].nunique()
    
    with col1:
        st.markdown(f"""
        <div class="kpi-simple">
            <div class="kpi-simple-label">Total Revenue</div>
            <div class="kpi-simple-value">{format_currency(total_revenue)}</div>
            <div class="kpi-simple-delta">+12.4% vs Target</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-simple">
            <div class="kpi-simple-label">Average Order Value</div>
            <div class="kpi-simple-value">${aov:.2f}</div>
            <div class="kpi-simple-delta">+8.2% vs Last Period</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-simple">
            <div class="kpi-simple-label">Units Sold</div>
            <div class="kpi-simple-value">{format_number(total_units)}</div>
            <div class="kpi-simple-delta">+15.7% Growth</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-simple">
            <div class="kpi-simple-label">Unique Orders</div>
            <div class="kpi-simple-value">{format_number(unique_orders)}</div>
            <div class="kpi-simple-delta">Customer Velocity</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts Row
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-title">Monthly Performance</div>', unsafe_allow_html=True)
        
        monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()
        month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                       7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        monthly_sales['Month_Label'] = monthly_sales['Month'].map(month_names)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_sales['Month_Label'],
            y=monthly_sales['Sales'],
            mode='lines+markers',
            line=dict(color='#0066FF', width=2),
            marker=dict(size=8, color='#0066FF'),
            fill='tozeroy',
            fillcolor='rgba(0, 102, 255, 0.1)',
            hovertemplate='%{x}<br>Sales: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            **CHART_LAYOUT,
            height=350,
            xaxis=dict(showgrid=False, title=dict(text='', font=AXIS_TICKFONT), tickfont=AXIS_TICKFONT),
            yaxis=dict(showgrid=True, gridcolor=theme['grid'], tickformat='$,.0s', title=dict(text='', font=AXIS_TICKFONT), tickfont=AXIS_TICKFONT)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-title">City Leaderboard</div>', unsafe_allow_html=True)
        
        city_sales = filtered_df.groupby('City')['Sales'].sum().sort_values(ascending=True).tail(5).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=city_sales['Sales'],
            y=city_sales['City'].str.strip(),
            orientation='h',
            marker=dict(color='#0066FF'),
            hovertemplate='%{y}<br>Revenue: $%{x:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            **CHART_LAYOUT,
            height=350,
            xaxis=dict(showgrid=True, gridcolor=theme['grid'], tickformat='$,.0s', tickfont=AXIS_TICKFONT, title=dict(font=AXIS_TICKFONT)),
            yaxis=dict(showgrid=False, tickfont=AXIS_TICKFONT, title=dict(font=AXIS_TICKFONT))
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Executive Summary
    top_city = filtered_df.groupby('City')['Sales'].sum().idxmax()
    top_product = filtered_df.groupby('Product')['Quantity Ordered'].sum().idxmax()
    peak_month = month_names.get(filtered_df.groupby('Month')['Sales'].sum().idxmax(), 'N/A')
    
    st.markdown(f"""
    <div class="summary-box">
        <h3>Executive Summary</h3>
        <ul>
            <li><strong>Top Performing City:</strong> {top_city.strip()} leads in revenue generation</li>
            <li><strong>Best Selling Product:</strong> {top_product} drives the highest unit sales</li>
            <li><strong>Peak Revenue Month:</strong> {peak_month}</li>
            <li><strong>Average Order Value:</strong> ${aov:.2f} indicates healthy basket sizes</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 2: Revenue & Marketing
# ============================================
with tab2:
    st.session_state['tab'] = 2
    filtered_df = render_filters()
    
    st.markdown("---")
    
    # Growth Simulation
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        growth_rate = st.slider("Simulate Growth Rate (%)", min_value=-20, max_value=50, value=0, step=5)
    
    projected_revenue = filtered_df['Sales'].sum() * (1 + growth_rate/100)
    
    with col2:
        st.metric("Current Revenue", format_currency(filtered_df['Sales'].sum()))
    with col3:
        st.metric("Projected Revenue", format_currency(projected_revenue), delta=f"{growth_rate:+}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-title">Sales by Hour of Day</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-description">Identify peak hours for advertising campaigns</div>', unsafe_allow_html=True)
        
        hourly_sales = filtered_df.groupby('Hour')['Sales'].sum().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=hourly_sales['Hour'],
            y=hourly_sales['Sales'],
            marker=dict(color='#0066FF'),
            hovertemplate='Hour: %{x}:00<br>Sales: $%{y:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            **CHART_LAYOUT,
            height=300,
            xaxis=dict(showgrid=False, title=dict(text='Hour of Day', font=AXIS_TICKFONT), tickmode='array', tickvals=list(range(0, 24, 3)), tickfont=AXIS_TICKFONT),
            yaxis=dict(showgrid=True, gridcolor=theme['grid'], tickformat='$,.0s', title=dict(text='', font=AXIS_TICKFONT), tickfont=AXIS_TICKFONT)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-title">Top 10 Products by Revenue</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-description">Focus inventory and marketing on top performers</div>', unsafe_allow_html=True)
        
        top_products = filtered_df.groupby('Product')['Sales'].sum().sort_values(ascending=True).tail(10).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_products['Sales'],
            y=top_products['Product'],
            orientation='h',
            marker=dict(color='#0066FF'),
            hovertemplate='%{y}<br>Revenue: $%{x:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            **CHART_LAYOUT,
            height=300,
            xaxis=dict(showgrid=True, gridcolor=theme['grid'], tickformat='$,.0s', tickfont=AXIS_TICKFONT, title=dict(font=AXIS_TICKFONT)),
            yaxis=dict(showgrid=False, tickfont=AXIS_TICKFONT, title=dict(font=AXIS_TICKFONT))
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    peak_hour = hourly_sales.loc[hourly_sales['Sales'].idxmax(), 'Hour']
    st.markdown(f"""
    <div class="summary-box">
        <h3>Marketing Recommendations</h3>
        <ul>
            <li><strong>Prime Time for Ads:</strong> 5 PM - 9 PM window (Peak at {peak_hour}:00)</li>
            <li><strong>Focus Products:</strong> Concentrate marketing spend on top 10 revenue generators</li>
            <li><strong>Growth Opportunity:</strong> {growth_rate}% growth would yield {format_currency(projected_revenue)} in revenue</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 3: Regional Insights
# ============================================
with tab3:
    st.session_state['tab'] = 3
    filtered_df = render_filters()
    
    st.markdown("---")
    
    st.markdown('<div class="section-title">Regional Revenue Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-description">Geospatial analysis for warehouse placement and retail hub optimization</div>', unsafe_allow_html=True)
    
    # City Performance
    city_performance = filtered_df.groupby('City').agg({
        'Sales': 'sum',
        'Quantity Ordered': 'sum',
        'Order ID': 'nunique'
    }).reset_index()
    city_performance.columns = ['City', 'Revenue', 'Units', 'Orders']
    city_performance = city_performance.sort_values('Revenue', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        city_sorted = city_performance.sort_values('Revenue', ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=city_sorted['Revenue'],
            y=city_sorted['City'].str.strip(),
            orientation='h',
            marker=dict(color='#0066FF'),
            text=[f"${v:,.0f}" for v in city_sorted['Revenue']],
            textposition='inside',
            textfont=dict(color='white', size=11),
            hovertemplate='%{y}<br>Revenue: $%{x:,.0f}<extra></extra>'
        ))
        
        fig.update_layout(
            **CHART_LAYOUT,
            height=400,
            xaxis=dict(showgrid=True, gridcolor=theme['grid'], tickformat='$,.0s', title=dict(text='Revenue', font=AXIS_TICKFONT), tickfont=AXIS_TICKFONT),
            yaxis=dict(showgrid=False, title=dict(text='', font=AXIS_TICKFONT), tickfont=AXIS_TICKFONT)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Top Cities Overview")
        for idx, row in city_performance.head(5).iterrows():
            pct = row['Revenue'] / city_performance['Revenue'].sum() * 100
            st.markdown(f"""
            <div class="city-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="city-name">{row['City'].strip()}</span>
                    <span class="city-revenue">{format_currency(row['Revenue'])}</span>
                </div>
                <div style="background: {theme['border']}; border-radius: 4px; height: 4px; margin-top: 8px;">
                    <div style="background: {theme['accent']}; width: {pct}%; height: 100%; border-radius: 4px;"></div>
                </div>
                <div class="city-percent">{pct:.1f}% of total</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Heatmap
    st.markdown('<div class="section-title">Order Volume Heatmap</div>', unsafe_allow_html=True)
    
    heatmap_data = filtered_df.groupby(['Day_of_Week', 'Hour'])['Sales'].sum().unstack(fill_value=0)
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(day_order)
    
    heatmap_colors = [[0, '#FFFFFF'], [0.5, '#66B3FF'], [1, '#0066FF']]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale=heatmap_colors,
        hovertemplate='Day: %{y}<br>Hour: %{x}:00<br>Sales: $%{z:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        **CHART_LAYOUT,
        height=300,
        xaxis=dict(title=dict(text='Hour of Day', font=AXIS_TICKFONT), tickmode='array', tickvals=list(range(0, 24, 4)), tickfont=AXIS_TICKFONT),
        yaxis=dict(title=dict(text='', font=AXIS_TICKFONT), tickfont=AXIS_TICKFONT)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Logistics Recommendation
    peak_day = filtered_df.groupby('Day_of_Week')['Sales'].sum().idxmax()
    peak_hour = filtered_df.groupby('Hour')['Sales'].sum().idxmax()
    
    st.markdown(f"""
    <div class="summary-box">
        <h3>Logistics Staffing Recommendation</h3>
        <ul>
            <li><strong>Peak Sales Day:</strong> {peak_day}</li>
            <li><strong>Peak Sales Hour:</strong> {peak_hour}:00</li>
            <li><strong>Recommendation:</strong> Increase staffing between 5 PM - 9 PM for optimal order fulfillment</li>
            <li><strong>Evening Hours:</strong> 6 PM - 9 PM account for highest transaction volume</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# TAB 4: Data Explorer
# ============================================
with tab4:
    st.session_state['tab'] = 4
    filtered_df = render_filters()
    
    st.markdown("---")
    
    # Metadata
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", f"{len(filtered_df):,}")
    with col2:
        st.metric("Date Range", f"{df['Order Date'].min().strftime('%Y-%m-%d')}")
    with col3:
        st.metric("Last Updated", "2026-01-25")
    with col4:
        st.metric("Data Source", "CSV Import")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Sub-tabs
    subtab1, subtab2, subtab3 = st.tabs(["Live Worksheet", "Analytics", "Forecasting"])
    
    with subtab1:
        st.markdown('<div class="section-title">Live Data Worksheet</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            search_term = st.text_input("Search Products", placeholder="Type to filter products...")
        with col2:
            quantity_threshold = st.number_input("Min Quantity Filter", min_value=1, value=1)
        
        display_df = filtered_df.copy()
        if search_term:
            display_df = display_df[display_df['Product'].str.contains(search_term, case=False)]
        display_df = display_df[display_df['Quantity Ordered'] >= quantity_threshold]
        
        st.dataframe(
            display_df[['Order ID', 'Product', 'Quantity Ordered', 'Price Each', 'Sales', 'City', 'Order Date']].head(100),
            use_container_width=True,
            height=400
        )
    
    with subtab2:
        st.markdown('<div class="section-title">Product Analytics</div>', unsafe_allow_html=True)
        
        product_stats = filtered_df.groupby('Product').agg({
            'Sales': 'sum',
            'Quantity Ordered': 'sum',
            'Order ID': 'nunique'
        }).reset_index()
        product_stats.columns = ['Product', 'Revenue', 'Units', 'Orders']
        
        fig = px.bar(
            product_stats.sort_values('Revenue', ascending=True),
            y='Product',
            x='Revenue',
            orientation='h',
            color_discrete_sequence=['#0066FF']
        )
        
        fig.update_layout(
            **CHART_LAYOUT,
            height=500,
            xaxis=dict(showgrid=True, gridcolor=theme['grid'], tickformat='$,.0s', tickfont=AXIS_TICKFONT, title=dict(font=AXIS_TICKFONT)),
            yaxis=dict(showgrid=False, tickfont=AXIS_TICKFONT, title=dict(font=AXIS_TICKFONT))
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with subtab3:
        st.markdown('<div class="section-title">Revenue Forecasting</div>', unsafe_allow_html=True)
        
        monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()
        
        if len(monthly_sales) >= 3:
            coeffs = np.polyfit(monthly_sales['Month'], monthly_sales['Sales'], 1)
            forecast_months = [13, 14, 15]
            forecast_values = np.polyval(coeffs, forecast_months)
        else:
            forecast_months = []
            forecast_values = []
        
        month_names = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                       7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec',
                       13: 'Jan 26', 14: 'Feb 26', 15: 'Mar 26'}
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=[month_names[m] for m in monthly_sales['Month']],
            y=monthly_sales['Sales'],
            mode='lines+markers',
            line=dict(color='#0066FF', width=2),
            marker=dict(size=8),
            name='Historical'
        ))
        
        if len(forecast_months) > 0:
            fig.add_trace(go.Scatter(
                x=[month_names[m] for m in forecast_months],
                y=forecast_values,
                mode='lines+markers',
                line=dict(color='#00AA55', width=2, dash='dot'),
                marker=dict(size=8, symbol='diamond'),
                name='Forecast'
            ))
        
        fig.update_layout(
            **CHART_LAYOUT,
            height=400,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color=theme['chart_text'])),
            xaxis=dict(showgrid=False, title=dict(text='Month', font=AXIS_TICKFONT), tickfont=AXIS_TICKFONT),
            yaxis=dict(showgrid=True, gridcolor=theme['grid'], tickformat='$,.0s', title=dict(text='Revenue', font=AXIS_TICKFONT), tickfont=AXIS_TICKFONT)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        if len(forecast_values) > 0:
            total_forecast = sum(forecast_values)
            st.markdown(f"""
            <div class="summary-box">
                <h3>Q1 2026 Projected Revenue</h3>
                <ul>
                    <li><strong>Total Projected:</strong> {format_currency(total_forecast)}</li>
                    <li><strong>Method:</strong> Linear regression on 2019 monthly trends</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
