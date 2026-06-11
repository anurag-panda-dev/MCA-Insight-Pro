"""Company Explorer page."""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_mca_data, preprocess_data
from utils.filters import search_companies
from components.ui_components import render_header, render_company_card, format_number
from services.analyzer import CompanyAnalyzer


def render_company_explorer():
    """Render company explorer page."""
    
    render_header("Company Explorer", "Search and analyze individual companies", "🔍")
    
    # Load data
    df = load_mca_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    df = preprocess_data(df)
    
    # Search box
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("Search by Company Name, CIN, or Registration Number", "")
    
    with col2:
        search_type = st.selectbox("Search Type", ["All", "Company Name", "CIN", "Registration Number"])
    
    with col3:
        max_results = st.slider("Max Results", 5, 100, 20)
    
    # Perform search
    if search_query:
        results = search_companies(df, search_query)
        results = results.head(max_results)
        
        st.success(f"Found {len(results)} companies")
        
        # Display results
        for idx, (_, company) in enumerate(results.iterrows()):
            with st.expander(f"📋 {company.get('company_name', 'N/A')}", expanded=(idx == 0)):
                
                # Company card
                render_company_card(company)
                
                # Detailed information
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Basic Information")
                    st.write(f"**CIN:** {company.get('cin', 'N/A')}")
                    st.write(f"**ROC:** {company.get('roc', 'N/A')}")
                    st.write(f"**Incorporation Date:** {company.get('date_of_incorporation', 'N/A')}")
                    if 'company_age_years' in company:
                        st.write(f"**Company Age:** {company['company_age_years']:.1f} years")
                
                with col2:
                    st.subheader("Classification")
                    st.write(f"**Category:** {company.get('company_category', 'N/A')}")
                    st.write(f"**Industry:** {company.get('industry', 'N/A')}")
                    st.write(f"**NIC Code:** {company.get('nic_code', 'N/A')}")
                
                # Financial information
                st.subheader("Financial Information")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Authorized Capital",
                        format_number(company.get('authorised_capital', 0), 1)
                    )
                
                with col2:
                    st.metric(
                        "Paid-Up Capital",
                        format_number(company.get('paid_up_capital', 0), 1)
                    )
                
                with col3:
                    if company.get('authorised_capital', 0) > 0:
                        efficiency = (company.get('paid_up_capital', 0) / company.get('authorised_capital', 1)) * 100
                        st.metric("Capital Efficiency", f"{efficiency:.1f}%")
                
                # Location
                st.subheader("Location & Contact")
                st.write(f"**State:** {company.get('registered_state', 'N/A')}")
                st.write(f"**Address:** {company.get('registered_address', 'N/A')}")
                st.write(f"**Email:** {company.get('email_address', 'N/A')}")
                
                # Status
                st.subheader("Status")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Company Status:** {company.get('company_status', 'N/A')}")
                
                with col2:
                    st.write(f"**Listing Status:** {company.get('listing_status', 'N/A')}")
                
                with col3:
                    st.write(f"**Class:** {company.get('class_of_company', 'N/A')}")
    
    else:
        st.info("👆 Enter a search query above to find companies")


if __name__ == "__main__":
    render_company_explorer()
