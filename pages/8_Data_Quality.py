"""Data Quality page."""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_mca_data, preprocess_data
from components.ui_components import render_header


def render_data_quality():
    """Render data quality page."""
    
    render_header("Data Quality Center", "Analyze data completeness and quality metrics", "✅")
    
    # Load data
    df = load_mca_data()
    if df.empty:
        st.error("Unable to load data")
        return
    
    df = preprocess_data(df)
    
    # Data quality metrics
    st.subheader("Data Quality Metrics")
    
    total_records = len(df)
    total_cells = len(df) * len(df.columns)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", f"{total_records:,}")
    
    with col2:
        st.metric("Total Columns", len(df.columns))
    
    with col3:
        st.metric("Total Cells", f"{total_cells:,}")
    
    # Missing values analysis
    st.subheader("Missing Values Analysis")
    
    missing_analysis = pd.DataFrame({
        'Column': df.columns,
        'Missing Count': df.isnull().sum(),
        'Missing %': (df.isnull().sum() / len(df) * 100).round(2)
    }).sort_values('Missing Count', ascending=False)
    
    missing_analysis = missing_analysis[missing_analysis['Missing Count'] > 0]
    
    if len(missing_analysis) > 0:
        st.dataframe(missing_analysis, use_container_width=True, hide_index=True)
        
        # Visual representation
        st.bar_chart(missing_analysis.set_index('Column')['Missing %'])
    
    else:
        st.success("✅ No missing values detected!")
    
    # Duplicate analysis
    st.subheader("Duplicate Records Analysis")
    
    if 'cin' in df.columns:
        cin_duplicates = df['cin'].value_counts()
        duplicate_cins = cin_duplicates[cin_duplicates > 1]
        
        if len(duplicate_cins) > 0:
            st.warning(f"⚠️ Found {len(duplicate_cins)} duplicate CINs")
            st.dataframe(duplicate_cins, use_container_width=True)
        else:
            st.success("✅ No duplicate CINs found!")
    
    # Data type analysis
    st.subheader("Data Type Analysis")
    
    dtype_analysis = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.count(),
        'Sample Value': [str(df[col].iloc[0])[:50] if df[col].notna().any() else 'N/A' for col in df.columns]
    })
    
    st.dataframe(dtype_analysis, use_container_width=True, hide_index=True)
    
    # Outlier detection
    st.subheader("Outlier Detection")
    
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    if len(numeric_cols) > 0:
        selected_col = st.selectbox("Select Column for Outlier Analysis", numeric_cols)
        
        if selected_col:
            col_data = df[selected_col].dropna()
            Q1 = col_data.quantile(0.25)
            Q3 = col_data.quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Values", len(col_data))
            
            with col2:
                st.metric("Outliers Count", len(outliers))
            
            with col3:
                outlier_pct = (len(outliers) / len(col_data) * 100) if len(col_data) > 0 else 0
                st.metric("Outlier %", f"{outlier_pct:.2f}%")
            
            # Box plot
            st.plotly_chart(
                {
                    'data': [{
                        'y': col_data,
                        'type': 'box'
                    }],
                    'layout': {
                        'title': f'Box Plot - {selected_col}',
                        'height': 400
                    }
                },
                use_container_width=True
            )
    
    # Data quality score
    st.subheader("Overall Data Quality Score")
    
    # Calculate quality score
    completeness = (1 - (df.isnull().sum().sum() / total_cells)) * 100
    uniqueness = 100 - (len(df) - df['cin'].nunique()) / len(df) * 100 if 'cin' in df.columns else 100
    
    quality_score = (completeness + uniqueness) / 2
    
    # Color based on score
    if quality_score >= 90:
        color = "#22c55e"
        status = "Excellent"
    elif quality_score >= 75:
        color = "#f59e0b"
        status = "Good"
    else:
        color = "#ef4444"
        status = "Fair"
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color}15 0%, {color}05 100%); 
                    border-left: 4px solid {color}; padding: 20px; border-radius: 8px;'>
            <div style='font-size: 14px; color: #666; font-weight: 500;'>Data Quality Score</div>
            <div style='font-size: 36px; color: {color}; font-weight: bold; margin-top: 8px;'>{quality_score:.1f}%</div>
            <div style='font-size: 14px; color: {color}; margin-top: 8px;'>{status}</div>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_data_quality()
