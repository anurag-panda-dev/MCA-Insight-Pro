"""State Intelligence page."""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_mca_data, preprocess_data
from components.ui_components import render_header, format_number, render_kpi_card
from components.charts import (
    create_state_distribution_chart, create_state_capital_chart,
    create_incorporation_trend_chart
)
from services.analyzer import StateAnalyzer
from utils.insights import generate_state_insights


def render_state_intelligence():
    """Render state intelligence page."""
    
    render_header("State Intelligence", "Analyze corporate landscape by states", "🗺️")
    
    # Load data
    df = load_mca_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    df = preprocess_data(df)
    
    # Get unique states
    states = sorted(df['registered_state'].dropna().unique().tolist())
    
    # State selector
    selected_state = st.selectbox("Select State", states)
    
    if selected_state:
        state_data = df[df['registered_state'] == selected_state]
        summary = StateAnalyzer.get_state_summary(df, selected_state)
        
        # State statistics
        st.subheader(f"{selected_state} - Statistics")
        
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
        insights = generate_state_insights(df, selected_state)
        for insight in insights:
            st.info(insight)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 States by Company Count")
            st.plotly_chart(create_state_distribution_chart(df, 10), use_container_width=True)
        
        with col2:
            st.subheader("Top 10 States by Capital")
            st.plotly_chart(create_state_capital_chart(df, 10), use_container_width=True)
        
        # Industry distribution in state
        st.subheader(f"Industry Distribution in {selected_state}")
        if 'industry' in state_data.columns:
            industry_dist = state_data['industry'].value_counts().head(10)
            st.bar_chart(industry_dist)
        
        # Company status in state
        st.subheader(f"Company Status in {selected_state}")
        if 'company_status' in state_data.columns:
            status_dist = state_data['company_status'].value_counts()
            st.bar_chart(status_dist)
        
        # Top companies by capital in state
        st.subheader(f"Top 10 Companies by Capital in {selected_state}")
        if len(state_data) > 0:
            top_companies = state_data.nlargest(10, 'authorised_capital')[
                ['company_name', 'authorised_capital', 'industry', 'company_status']
            ]
            st.dataframe(top_companies, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    render_state_intelligence()
