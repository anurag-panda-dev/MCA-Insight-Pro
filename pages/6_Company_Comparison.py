"""Company Comparison page."""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_mca_data, preprocess_data
from utils.filters import search_companies
from components.ui_components import render_header, format_number
from services.analyzer import compare_companies


def render_company_comparison():
    """Render company comparison page."""
    
    render_header("Company Comparison", "Compare up to 5 companies side-by-side", "⚖️")
    
    # Load data
    df = load_mca_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    df = preprocess_data(df)
    
    # Comparison setup
    st.subheader("Select Companies to Compare")
    
    # Create input for each company
    selected_companies = []
    
    for i in range(5):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            company_search = st.text_input(
                f"Company {i+1}",
                key=f"company_search_{i}",
                placeholder="Search by name or CIN..."
            )
            
            if company_search:
                search_results = search_companies(df, company_search)
                if len(search_results) > 0:
                    selected_company = st.selectbox(
                        f"Select Company {i+1}",
                        options=search_results['company_name'].tolist(),
                        key=f"company_select_{i}"
                    )
                    
                    company_data = search_results[search_results['company_name'] == selected_company].iloc[0]
                    selected_companies.append(company_data)
        
        with col2:
            st.write("")  # Spacing
    
    if len(selected_companies) > 0:
        st.subheader(f"Comparison: {len(selected_companies)} Companies")
        
        # Create comparison dataframe
        comparison_df = compare_companies(selected_companies)
        
        # Display comparison table
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Detailed comparison views
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Capital Comparison")
            capital_comparison = pd.DataFrame({
                'Company': [c.get('company_name', 'N/A') for c in selected_companies],
                'Authorized Capital (₹ Cr)': [c.get('authorised_capital', 0) / 1e7 for c in selected_companies],
                'Paid-Up Capital (₹ Cr)': [c.get('paid_up_capital', 0) / 1e7 for c in selected_companies],
            })
            st.bar_chart(capital_comparison.set_index('Company'))
        
        with col2:
            st.subheader("Company Age Comparison")
            age_comparison = pd.DataFrame({
                'Company': [c.get('company_name', 'N/A') for c in selected_companies],
                'Age (Years)': [c.get('company_age_years', 0) for c in selected_companies],
            })
            st.bar_chart(age_comparison.set_index('Company'))
        
        # Status comparison
        st.subheader("Status Comparison")
        status_data = []
        for company in selected_companies:
            status_data.append({
                'Company': company.get('company_name', 'N/A'),
                'Status': company.get('company_status', 'N/A'),
                'State': company.get('registered_state', 'N/A'),
                'Industry': company.get('industry', 'N/A'),
                'Listing': company.get('listing_status', 'N/A'),
            })
        
        status_df = pd.DataFrame(status_data)
        st.dataframe(status_df, use_container_width=True, hide_index=True)
        
        # Download comparison report
        csv = comparison_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Comparison Report (CSV)",
            data=csv,
            file_name="company_comparison.csv",
            mime="text/csv"
        )
    
    else:
        st.info("👆 Search and select companies above to compare them")


if __name__ == "__main__":
    render_company_comparison()
