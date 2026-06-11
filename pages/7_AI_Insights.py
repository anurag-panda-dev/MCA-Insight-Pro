"""AI Insights page."""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_mca_data, preprocess_data
from components.ui_components import render_header
from utils.insights import (
    generate_dataset_insights, generate_state_insights,
    generate_industry_insights, generate_capital_insights,
    generate_growth_insights
)


def render_ai_insights():
    """Render AI insights page."""
    
    render_header("AI Insights Engine", "Automatic executive-level analysis and observations", "🤖")
    
    # Load data
    df = load_mca_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    df = preprocess_data(df)
    
    # Insight tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dataset Summary",
        "🗺️ State Analysis",
        "🏭 Industry Analysis",
        "💰 Capital Analysis",
        "📈 Growth Analysis"
    ])
    
    # Dataset insights
    with tab1:
        st.subheader("Dataset Summary Insights")
        insights = generate_dataset_insights(df)
        for i, insight in enumerate(insights):
            st.info(insight)
    
    # State insights
    with tab2:
        st.subheader("State-Level Insights")
        
        states = sorted(df['registered_state'].dropna().unique().tolist())
        selected_state = st.selectbox("Select State for Analysis", states)
        
        if selected_state:
            insights = generate_state_insights(df, selected_state)
            for insight in insights:
                st.info(insight)
    
    # Industry insights
    with tab3:
        st.subheader("Industry-Level Insights")
        
        industries = sorted(df['industry'].dropna().unique().tolist())
        selected_industry = st.selectbox("Select Industry for Analysis", industries)
        
        if selected_industry:
            insights = generate_industry_insights(df, selected_industry)
            for insight in insights:
                st.info(insight)
    
    # Capital insights
    with tab4:
        st.subheader("Capital Analysis Insights")
        
        insights = generate_capital_insights(df)
        for insight in insights:
            st.info(insight)
    
    # Growth insights
    with tab5:
        st.subheader("Growth & Trend Insights")
        
        insights = generate_growth_insights(df)
        for insight in insights:
            st.info(insight)
        
        # Additional growth analysis
        if 'date_of_incorporation' in df.columns:
            st.subheader("Yearly Incorporation Trends")
            
            df_copy = df.copy()
            df_copy['incorporation_year'] = pd.to_datetime(df_copy['date_of_incorporation'], errors='coerce').dt.year
            yearly_trends = df_copy['incorporation_year'].value_counts().sort_index()
            
            st.line_chart(yearly_trends)
            
            # Calculate CAGR for last 5 years
            recent_years = yearly_trends.tail(5)
            if len(recent_years) >= 2:
                first_year_value = recent_years.iloc[0]
                last_year_value = recent_years.iloc[-1]
                years = len(recent_years) - 1
                
                cagr = ((last_year_value / first_year_value) ** (1 / years) - 1) * 100 if first_year_value > 0 else 0
                
                st.metric(
                    "CAGR (Last 5 Years)",
                    f"{cagr:.2f}%",
                    "Compound Annual Growth Rate"
                )


if __name__ == "__main__":
    render_ai_insights()
