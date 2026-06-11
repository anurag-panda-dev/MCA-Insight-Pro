"""Capital Intelligence page."""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_mca_data, preprocess_data
from components.ui_components import render_header, format_number, create_top_companies_chart
from components.charts import create_capital_distribution_chart
from utils.insights import generate_capital_insights


def render_capital_intelligence():
    """Render capital intelligence page."""
    
    render_header("Capital Intelligence", "Analyze capital distribution and wealth concentration", "💰")
    
    # Load data
    df = load_mca_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    df = preprocess_data(df)
    
    # Capital metrics
    st.subheader("Capital Metrics")
    
    total_authorized = df['authorised_capital'].sum()
    total_paid_up = df['paid_up_capital'].sum() if 'paid_up_capital' in df.columns else 0
    avg_authorized = df['authorised_capital'].mean()
    avg_paid_up = df['paid_up_capital'].mean() if 'paid_up_capital' in df.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Authorized Capital",
            format_number(total_authorized, 1),
            "₹ Billion"
        )
    
    with col2:
        st.metric(
            "Total Paid-Up Capital",
            format_number(total_paid_up, 1),
            "₹ Billion"
        )
    
    with col3:
        st.metric(
            "Avg Authorized Capital",
            format_number(avg_authorized, 1),
            "Per Company"
        )
    
    with col4:
        efficiency = (total_paid_up / total_authorized * 100) if total_authorized > 0 else 0
        st.metric(
            "Capital Efficiency",
            f"{efficiency:.2f}%",
            "Paid-up / Authorized"
        )
    
    # Insights
    st.subheader("Key Insights")
    insights = generate_capital_insights(df)
    for insight in insights:
        st.info(insight)
    
    # Capital distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Capital Distribution")
        st.plotly_chart(create_capital_distribution_chart(df), use_container_width=True)
    
    with col2:
        st.subheader("Capital Range Analysis")
        # Create capital range buckets
        capital_ranges = {
            '< 1 Lakh': (0, 1e5),
            '1 - 10 Lakh': (1e5, 10e5),
            '10 Lakh - 1 Cr': (10e5, 1e7),
            '1 - 10 Cr': (1e7, 10e7),
            '10 Cr - 100 Cr': (10e7, 100e7),
            '> 100 Cr': (100e7, float('inf'))
        }
        
        range_counts = {}
        for range_name, (low, high) in capital_ranges.items():
            count = len(df[(df['authorised_capital'] >= low) & (df['authorised_capital'] < high)])
            range_counts[range_name] = count
        
        st.bar_chart(range_counts)
    
    # Top companies by capital
    st.subheader("Top 20 Companies by Authorized Capital")
    st.plotly_chart(create_top_companies_chart(df, 'authorised_capital', 20), use_container_width=True)
    
    # Pareto analysis
    st.subheader("Pareto Analysis - Capital Concentration")
    
    sorted_df = df.sort_values('authorised_capital', ascending=False)
    sorted_df['cumulative_capital'] = sorted_df['authorised_capital'].cumsum()
    sorted_df['cumulative_pct'] = (sorted_df['cumulative_capital'] / total_authorized) * 100
    sorted_df['company_rank_pct'] = (range(1, len(sorted_df) + 1) / len(sorted_df)) * 100
    
    # Find concentration points
    top_20_pct_companies = sorted_df[sorted_df['company_rank_pct'] <= 20].copy()
    top_20_capital_pct = top_20_pct_companies['cumulative_pct'].iloc[-1] if len(top_20_pct_companies) > 0 else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Top 20% of Companies",
            f"{top_20_capital_pct:.1f}%",
            "Hold this % of total capital"
        )
    
    with col2:
        top_100_companies = sorted_df.head(100)
        top_100_capital_pct = (top_100_companies['authorised_capital'].sum() / total_authorized) * 100
        st.metric(
            "Top 100 Companies",
            f"{top_100_capital_pct:.1f}%",
            "Hold this % of total capital"
        )
    
    # Top companies data
    st.subheader("Top 50 Companies by Capital")
    top_50 = df.nlargest(50, 'authorised_capital')[
        ['company_name', 'registered_state', 'industry', 'authorised_capital', 'paid_up_capital']
    ].copy()
    top_50['efficiency'] = (top_50['paid_up_capital'] / top_50['authorised_capital'] * 100).round(2)
    
    st.dataframe(top_50, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    render_capital_intelligence()
