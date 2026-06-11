# MCA INSIGHT PRO - QUICK START GUIDE

This is a complete production-grade Streamlit application for analyzing MCA Master Data.

## Installation & Execution

### Option 1: Quick Start (Windows PowerShell)

```powershell
# 1. Navigate to project directory
cd e:\MCA_COMPANY_VISU

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
.\venv\Scripts\Activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run application
streamlit run app.py
```

### Option 2: Using Python Command

```bash
# Install dependencies
pip install streamlit pandas numpy plotly duckdb pyarrow scikit-learn streamlit-option-menu streamlit-extras openpyxl reportlab rapidfuzz

# Run application
streamlit run app.py
```

### Option 3: Docker (if you have Docker installed)

```bash
docker-compose up
```

## Application Structure

```
📊 MCA INSIGHT PRO
├── 📄 Executive Dashboard (Home)
├── 🔍 Company Explorer
├── 🗺️ State Intelligence
├── 🏭 Industry Intelligence
├── 💰 Capital Intelligence
├── ⚖️ Company Comparison
├── 🤖 AI Insights
├── ✅ Data Quality
├── 📄 Reports & Export
└── ⭐ Watchlist
```

## Features at a Glance

✅ 10 interactive pages
✅ 50+ visualizations
✅ Advanced company search
✅ Multi-dimensional filtering
✅ Export in CSV/Excel
✅ AI-generated insights
✅ Data quality validation
✅ Company comparison tools
✅ State & industry analytics
✅ Capital distribution analysis

## Data File

The application loads data from:
`company_master_data_2025_06_30.csv`

This file should be in the project root directory.

## Browser Access

After running `streamlit run app.py`:
- Application opens at: `http://localhost:8501`
- If not automatic, manually visit the URL shown in terminal

## System Requirements

- Python 3.9 or higher
- 4GB+ RAM recommended
- 500MB+ disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Troubleshooting

**Issue**: Command not found
- Solution: Ensure Python is in PATH, or use full path

**Issue**: "Data file not found"
- Solution: Place CSV in same directory as app.py

**Issue**: Port 8501 already in use
- Solution: Run with different port: `streamlit run app.py --server.port=8502`

**Issue**: Slow loading
- Solution: First load caches data, subsequent loads are faster

## Key Capabilities

### Executive Dashboard
- KPI cards with key metrics
- Status distribution charts
- Incorporation trends
- Top states and industries

### Company Explorer
- Instant search by name, CIN, registration number
- Detailed company profiles
- Financial metrics
- Status tracking

### Regional & Sectoral Analysis
- State-level insights
- Industry deep dives
- Geographic distribution
- Comparative metrics

### Advanced Analytics
- Capital concentration analysis
- Wealth distribution metrics
- Top companies leaderboards
- Trend forecasting

### Data Management
- Quality metrics
- Missing value analysis
- Duplicate detection
- Export capabilities

## Tips for Best Results

1. **Search**: Use CIN for most accurate results
2. **Filters**: Apply multiple filters for targeted analysis
3. **Export**: Use filtered exports for large datasets
4. **Charts**: Hover over charts for detailed information
5. **Insights**: Check AI Insights for quick analysis

## Support

For detailed documentation, see README.md

## Version

MCA Insight Pro v1.0
Data Updated: June 30, 2025
Status: Production Ready

---

**Built with**: Streamlit | Python | Plotly | Pandas
**For**: Business Intelligence & Corporate Analysis
