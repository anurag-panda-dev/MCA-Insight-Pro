"""Industry Intelligence page."""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_mca_data, preprocess_data
from components.ui_components import render_header, format_number
from components.charts import (
    create_industry_distribution_chart, create_industry_capital_chart
)
from services.analyzer import IndustryAnalyzer
from utils.insights import generate_industry_insights


def render_industry_intelligence():
    """Render industry intelligence page."""
    
    render_header("Industry Intelligence", "Explore industry trends and metrics", "🏭")
    
    # Load data
    df = load_mca_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    df = preprocess_data(df)
    
    # Get unique industries
    industries = sorted(df['industry'].dropna().unique().tolist())
    
    # Industry selector
    selected_industry = st.selectbox("Select Industry", industries)
    
    if selected_industry:
        industry_data = df[df['industry'] == selected_industry]
        summary = IndustryAnalyzer.get_industry_summary(df, selected_industry)
        
        # Industry statistics
        st.subheader(f"{selected_industry} - Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Companies", f"{summary.get('total_companies', 0):,}")
        
        with col2:
            st.metric("Active Companies", f"{summary.get('active_companies', 0):,}")
        
        with col3:
            st.metric(
                "Total Capital",
                format_number(summary.get('total_capital', 0), 1)
            )
        
        with col4:
            st.metric(
                "Avg Capital",
                format_number(summary.get('avg_capital', 0), 1)
            )
        
        # Insights
        st.subheader("Key Insights")
        insights = generate_industry_insights(df, selected_industry)
        for insight in insights:
            st.info(insight)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Industry Distribution")
            st.plotly_chart(create_industry_distribution_chart(df, 15), use_container_width=True)
        
        with col2:
            st.subheader("Top Industries by Capital")
            st.plotly_chart(create_industry_capital_chart(df, 15), use_container_width=True)
        
        # State distribution in industry
        st.subheader(f"State Distribution in {selected_industry}")
        if 'registered_state' in industry_data.columns:
            state_dist = industry_data['registered_state'].value_counts().head(10)
            st.bar_chart(state_dist)
        
        # Category distribution in industry
        st.subheader(f"Company Category Distribution in {selected_industry}")
        if 'company_category' in industry_data.columns:
            category_dist = industry_data['company_category'].value_counts().head(10)
            st.bar_chart(category_dist)
        
        # Top companies in industry
        st.subheader(f"Top 10 Companies in {selected_industry}")
        if len(industry_data) > 0:
            top_companies = industry_data.nlargest(10, 'authorised_capital')[
                ['company_name', 'registered_state', 'authorised_capital', 'company_status']
            ]
            st.dataframe(top_companies, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    render_industry_intelligence()
