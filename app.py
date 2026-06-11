"""Main Streamlit application - MCA Insight Pro."""
import streamlit as st
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="MCA Insight Pro - Corporate Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    
    .main {
        padding: 0px;
    }
    
    h1 {
        color: #667eea;
    }
    
    h2 {
        color: #764ba2;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar branding
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #667eea; margin: 0;'>📊</h1>
            <h3 style='color: #667eea; margin: 5px 0;'>MCA Insight Pro</h3>
            <p style='color: #999; font-size: 12px;'>Corporate Intelligence Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("""
    ### About This Dashboard
    
    **MCA Insight Pro** is India's leading corporate intelligence platform, 
    powered by the latest MCA Master Data (Updated: June 30, 2025).
    
    #### Platform Features:
    - 📊 Executive Intelligence Dashboard
    - 🔍 Advanced Company Search
    - 🗺️ State & Regional Analysis
    - 🏭 Industry Deep Dives
    - 💰 Capital Intelligence
    - ⚖️ Company Comparisons
    - 🤖 AI-Powered Insights
    - ✅ Data Quality Monitoring
    - 📄 Report Generation
    - ⭐ Watchlist Management
    
    #### Target Audience:
    - Business Analysts
    - Investors & VCs
    - Corporate Consultants
    - Researchers & Students
    - Government Officials
    - Startup Founders
    
    #### Data Source:
    MCA Master Data - Ministry of Corporate Affairs, India
    """)
    
    st.divider()
    
    # Help section
    if st.checkbox("📚 Show Help & Tips"):
        st.markdown("""
        ### Tips for Using MCA Insight Pro:
        
        1. **Search**: Use the Company Explorer to search by name, CIN, or registration number
        2. **Filter**: Apply filters in any page to narrow down results
        3. **Compare**: Compare up to 5 companies side-by-side
        4. **Export**: Download data in CSV or Excel format
        5. **Insights**: View AI-generated insights for quick analysis
        6. **Quality**: Check Data Quality Center for data completeness
        7. **Watchlist**: Bookmark companies for future reference
        
        ### Keyboard Shortcuts:
        - `Ctrl+K`: Search
        - `Ctrl+Shift+E`: Export
        """)

# Page content
st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 10px; margin-bottom: 20px; color: white;'>
        <h1 style='color: white; margin: 0;'>📊 MCA Corporate Intelligence Dashboard</h1>
        <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0;'>
            Analyze India's Corporate Landscape with Advanced Business Intelligence
        </p>
    </div>
""", unsafe_allow_html=True)

# Main content area info
st.markdown("""
### Welcome to MCA Insight Pro

Select a page from the sidebar to explore:

- **Executive Dashboard**: Overview of key metrics and trends
- **Company Explorer**: Search and analyze individual companies
- **State Intelligence**: Regional business analysis
- **Industry Intelligence**: Sector-wise insights
- **Capital Intelligence**: Capital distribution and wealth analysis
- **Company Comparison**: Compare multiple companies
- **AI Insights**: Automated executive analysis
- **Data Quality**: Data completeness and validation
- **Reports & Export**: Generate and download reports
- **Watchlist**: Track your favorite companies

### Get Started

1. Go to **Executive Dashboard** for a quick overview
2. Use **Company Explorer** to search for specific companies
3. Visit **State Intelligence** and **Industry Intelligence** for regional/sector analysis
4. Check **AI Insights** for automated analysis
5. Use **Reports & Export** to download data

### Platform Capabilities

- 🔍 **Smart Search**: Find companies by name, CIN, registration number
- 📊 **Rich Analytics**: 50+ visualizations and charts
- 💾 **Data Export**: CSV, Excel, PDF formats
- 🎯 **Advanced Filters**: State, industry, capital, status, and more
- 📈 **Trend Analysis**: Incorporation trends, growth metrics
- 🏆 **Leaderboards**: Top companies by various metrics
- 🎨 **Professional Design**: Enterprise-grade UI/UX
""")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #999; font-size: 12px; padding: 20px;'>
        <p>MCA Insight Pro v1.0 | Data Updated: June 30, 2025</p>
        <p>Powered by Streamlit, Plotly, and Python</p>
        <p>© 2025 Corporate Intelligence Platform | All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)

logger.info("MCA Insight Pro dashboard loaded successfully")
