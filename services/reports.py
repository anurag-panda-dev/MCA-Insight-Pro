"""Report generation services."""
import pandas as pd
from typing import List, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_excel_report(df: pd.DataFrame, filename: str = "mca_report") -> bytes:
    """
    Generate Excel report.
    
    Args:
        df: Dataframe to export
        filename: Output filename
        
    Returns:
        bytes: Excel file bytes
    """
    from io import BytesIO
    
    excel_buffer = BytesIO()
    
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Data', index=False)
    
    excel_buffer.seek(0)
    return excel_buffer.getvalue()


def generate_csv_report(df: pd.DataFrame) -> bytes:
    """
    Generate CSV report.
    
    Args:
        df: Dataframe to export
        
    Returns:
        bytes: CSV file bytes
    """
    from io import BytesIO
    
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer.getvalue()


def generate_summary_text_report(data_summary: dict, filtered_count: int) -> str:
    """
    Generate summary text report.
    
    Args:
        data_summary: Summary statistics dict
        filtered_count: Count of filtered records
        
    Returns:
        str: Report text
    """
    report = f"""
MCA CORPORATE INTELLIGENCE REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DATA OVERVIEW
=============
Total Companies: {data_summary.get('total_companies', 0):,}
Filtered Companies: {filtered_count:,}
Total States: {data_summary.get('total_states', 0)}
Total Industries: {data_summary.get('total_industries', 0)}

COMPANY STATUS
==============
Active Companies: {data_summary.get('active_companies', 0):,}
Inactive Companies: {data_summary.get('inactive_companies', 0):,}
Strike Off Companies: {data_summary.get('strike_off', 0):,}
Under Liquidation: {data_summary.get('liquidation', 0):,}

CAPITAL METRICS
===============
Total Authorized Capital: ₹{data_summary.get('total_authorized_capital', 0)/1e9:.2f}B
Average Authorized Capital: ₹{data_summary.get('avg_authorized_capital', 0)/1e7:.2f}Cr
Total Paid-Up Capital: ₹{data_summary.get('total_paid_up_capital', 0)/1e9:.2f}B
Average Paid-Up Capital: ₹{data_summary.get('avg_paid_up_capital', 0)/1e7:.2f}Cr
    """
    
    return report
