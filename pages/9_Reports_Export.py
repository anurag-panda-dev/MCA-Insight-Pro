"""Reports & Export page."""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_mca_data, preprocess_data, get_data_summary
from utils.filters import apply_filters, get_filter_options
from components.ui_components import render_header
from services.reports import generate_excel_report, generate_csv_report, generate_summary_text_report


def render_reports_export():
    """Render reports and export page."""
    
    render_header("Reports & Export", "Generate and export analysis reports", "📄")
    
    # Load data
    df = load_mca_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    df = preprocess_data(df)
    
    # Export options
    tab1, tab2, tab3 = st.tabs(["Export Data", "Generate Reports", "Filtered Export"])
    
    # Export Data tab
    with tab1:
        st.subheader("Export Full Dataset")
        
        export_format = st.radio("Select Export Format", ["CSV", "Excel"], horizontal=True)
        
        if st.button("📥 Export", key="export_full"):
            if export_format == "CSV":
                csv_data = generate_csv_report(df)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="mca_companies_full.csv",
                    mime="text/csv"
                )
            else:
                excel_data = generate_excel_report(df, "mca_companies_full")
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name="mca_companies_full.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    # Generate Reports tab
    with tab2:
        st.subheader("Generate Analysis Report")
        
        report_type = st.selectbox(
            "Select Report Type",
            ["Summary Report", "Executive Summary", "Top Companies Report"]
        )
        
        if st.button("📊 Generate Report"):
            summary = get_data_summary(df)
            
            if report_type == "Summary Report":
                report_text = generate_summary_text_report(summary, len(df))
                st.text(report_text)
                
                st.download_button(
                    label="📥 Download Report (TXT)",
                    data=report_text,
                    file_name="mca_summary_report.txt",
                    mime="text/plain"
                )
            
            elif report_type == "Executive Summary":
                exec_summary = f"""
MCA CORPORATE INTELLIGENCE - EXECUTIVE SUMMARY
Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

KEY METRICS
===========
Total Companies: {summary['total_companies']:,}
Active Companies: {summary['active_companies']:,} ({(summary['active_companies']/summary['total_companies']*100):.1f}%)
States: {summary['total_states']}
Industries: {summary['total_industries']}

CAPITAL SUMMARY
===============
Total Authorized Capital: ₹{summary['total_authorized_capital']/1e9:.2f}B
Average Per Company: ₹{summary['avg_authorized_capital']/1e7:.2f}Cr

TOP ENTITIES
============
- Top States, Industries, and Companies by Capital
                """
                st.text(exec_summary)
                
                st.download_button(
                    label="📥 Download Report (TXT)",
                    data=exec_summary,
                    file_name="mca_executive_summary.txt",
                    mime="text/plain"
                )
            
            elif report_type == "Top Companies Report":
                top_100 = df.nlargest(100, 'authorised_capital')[
                    ['company_name', 'registered_state', 'industry', 'authorised_capital', 'company_status']
                ]
                
                csv_data = top_100.to_csv(index=False)
                st.download_button(
                    label="📥 Download Top 100 Companies (CSV)",
                    data=csv_data,
                    file_name="top_100_companies.csv",
                    mime="text/csv"
                )
    
    # Filtered Export tab
    with tab3:
        st.subheader("Export Filtered Data")
        
        # Filter options
        filter_options = get_filter_options(df)
        
        filters = {}
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'states' in filter_options:
                filters['state'] = st.multiselect("States", filter_options['states'])
            
            if 'company_status' in filter_options:
                filters['company_status'] = st.multiselect("Company Status", filter_options['company_status'])
            
            if 'industries' in filter_options:
                filters['industry'] = st.multiselect("Industries", filter_options['industries'][:20])
        
        with col2:
            if 'company_category' in filter_options:
                filters['company_category'] = st.multiselect("Category", filter_options['company_category'][:10])
            
            cap_range = st.slider("Authorized Capital Range", 0, 1000000000, (0, 1000000000))
            filters['authorized_capital_range'] = cap_range
        
        # Apply filters
        filtered_df = apply_filters(df, filters)
        
        st.info(f"📊 {len(filtered_df)} companies match the filters")
        
        if len(filtered_df) > 0:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📥 Export CSV"):
                    csv_data = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="Download Filtered CSV",
                        data=csv_data,
                        file_name="filtered_companies.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("📥 Export Excel"):
                    excel_data = generate_excel_report(filtered_df, "filtered_companies")
                    st.download_button(
                        label="Download Filtered Excel",
                        data=excel_data,
                        file_name="filtered_companies.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            with col3:
                st.metric("Records to Export", f"{len(filtered_df):,}")
            
            # Preview
            st.subheader("Preview")
            st.dataframe(filtered_df.head(20), use_container_width=True)


if __name__ == "__main__":
    render_reports_export()
