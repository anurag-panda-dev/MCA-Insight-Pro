"""Favorites & Watchlist page."""
import streamlit as st
import pandas as pd
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_mca_data, preprocess_data
from utils.filters import search_companies
from components.ui_components import render_header, render_company_card, format_number


def render_watchlist():
    """Render favorites and watchlist page."""
    
    render_header("Favorites & Watchlist", "Bookmark and track your favorite companies", "⭐")
    
    # Initialize session state for watchlist
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []
    
    # Load data
    df = load_mca_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    df = preprocess_data(df)
    
    # Add to watchlist
    st.subheader("Add to Watchlist")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("Search company to add to watchlist")
    
    with col2:
        st.write("")  # Spacing
    
    if search_query:
        search_results = search_companies(df, search_query)
        
        if len(search_results) > 0:
            selected_company = st.selectbox(
                "Select company",
                options=search_results['company_name'].tolist(),
                key="watchlist_add"
            )
            
            if st.button("➕ Add to Watchlist"):
                company_data = search_results[search_results['company_name'] == selected_company].iloc[0]
                
                # Check if already in watchlist
                if company_data['cin'] not in st.session_state.watchlist:
                    st.session_state.watchlist.append({
                        'cin': company_data.get('cin'),
                        'company_name': company_data.get('company_name'),
                        'added_date': pd.Timestamp.now().strftime('%Y-%m-%d')
                    })
                    st.success(f"✅ Added {company_data.get('company_name')} to watchlist!")
                else:
                    st.warning("ℹ️ This company is already in your watchlist")
    
    # Display watchlist
    st.subheader(f"Your Watchlist ({len(st.session_state.watchlist)} companies)")
    
    if len(st.session_state.watchlist) > 0:
        watchlist_df = pd.DataFrame(st.session_state.watchlist)
        
        # Display as table
        st.dataframe(watchlist_df, use_container_width=True, hide_index=True)
        
        # Detailed view
        st.subheader("Watchlist Details")
        
        for idx, item in enumerate(st.session_state.watchlist):
            company = df[df['cin'] == item['cin']]
            
            if len(company) > 0:
                company_data = company.iloc[0]
                
                with st.expander(f"📋 {company_data.get('company_name', 'N/A')}", expanded=(idx == 0)):
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Status", company_data.get('company_status', 'N/A'))
                    
                    with col2:
                        st.metric("State", company_data.get('registered_state', 'N/A'))
                    
                    with col3:
                        st.metric(
                            "Authorized Capital",
                            format_number(company_data.get('authorised_capital', 0), 1)
                        )
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Industry:** {company_data.get('industry', 'N/A')}")
                        st.write(f"**Category:** {company_data.get('company_category', 'N/A')}")
                    
                    with col2:
                        st.write(f"**CIN:** {company_data.get('cin', 'N/A')}")
                        st.write(f"**Incorporated:** {company_data.get('date_of_incorporation', 'N/A')}")
                    
                    # Remove button
                    if st.button(f"🗑️ Remove from Watchlist", key=f"remove_{idx}"):
                        st.session_state.watchlist.pop(idx)
                        st.rerun()
        
        # Export watchlist
        st.subheader("Export Watchlist")
        
        watchlist_csv = watchlist_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Watchlist (CSV)",
            data=watchlist_csv,
            file_name="watchlist.csv",
            mime="text/csv"
        )
    
    else:
        st.info("👆 Search and add companies above to create your watchlist")
    
    # Search history
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    st.subheader("Recent Searches")
    
    recent_searches = st.text_input("View recent searches (for future reference)")
    
    if recent_searches:
        st.info("Search history feature - Saved searches will appear here")


if __name__ == "__main__":
    render_watchlist()
