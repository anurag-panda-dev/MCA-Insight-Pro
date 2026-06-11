"""Components for UI rendering."""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List


def render_kpi_card(label: str, value: str, icon: str, color: str = "#1f77b4", delta: str = None):
    """
    Render a KPI card.
    
    Args:
        label: Card label
        value: Card value
        icon: Emoji icon
        color: Card color
        delta: Change indicator
    """
    delta_html = f"<small style='color: #666;'>{delta}</small>" if delta else ""
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, {color}15 0%, {color}05 100%); 
                    border-left: 4px solid {color}; padding: 20px; border-radius: 8px; margin: 10px 0;'>
            <div style='font-size: 14px; color: #666; font-weight: 500;'>{icon} {label}</div>
            <div style='font-size: 28px; color: {color}; font-weight: bold; margin-top: 8px;'>{value}</div>
            {delta_html}
        </div>
    """, unsafe_allow_html=True)


def render_metric_row(metrics: List[Dict[str, str]]):
    """
    Render a row of metrics.
    
    Args:
        metrics: List of metric dictionaries with 'label', 'value', 'icon', 'color'
    """
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            render_kpi_card(
                metric.get('label', ''),
                metric.get('value', ''),
                metric.get('icon', '📊'),
                metric.get('color', '#1f77b4'),
                metric.get('delta', None)
            )


def render_header(title: str, subtitle: str = "", icon: str = "📊"):
    """
    Render page header with styling.
    
    Args:
        title: Header title
        subtitle: Header subtitle
        icon: Header icon
    """
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: white; margin: 0;'>{icon} {title}</h1>
            <p style='color: rgba(255,255,255,0.8); margin: 10px 0 0 0;'>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def format_number(num: float, decimals: int = 0) -> str:
    """
    Format large numbers for display.
    
    Args:
        num: Number to format
        decimals: Decimal places
        
    Returns:
        str: Formatted number
    """
    if num >= 1e9:
        return f"₹{num/1e9:.{decimals}f}B"
    elif num >= 1e7:
        return f"₹{num/1e7:.{decimals}f}Cr"
    elif num >= 1e5:
        return f"₹{num/1e5:.{decimals}f}L"
    else:
        return f"₹{num:,.0f}"


def render_company_card(company: pd.Series):
    """
    Render a company information card.
    
    Args:
        company: Company data series
    """
    status_color = {
        'Active': '🟢',
        'Inactive': '🔴',
        'Strike Off': '⚫',
        'Under Liquidation': '🟠'
    }
    
    status = company.get('company_status', 'Unknown')
    status_badge = status_color.get(status, '⚪')
    
    st.markdown(f"""
        <div style='background: white; border: 1px solid #e0e0e0; padding: 15px; 
                    border-radius: 8px; margin: 10px 0;'>
            <h4 style='margin: 0 0 10px 0;'>{status_badge} {company.get('company_name', 'N/A')}</h4>
            <table style='width: 100%; font-size: 14px; color: #666;'>
                <tr>
                    <td><strong>CIN:</strong></td>
                    <td>{company.get('cin', 'N/A')}</td>
                </tr>
                <tr>
                    <td><strong>State:</strong></td>
                    <td>{company.get('registered_state', 'N/A')}</td>
                </tr>
                <tr>
                    <td><strong>Industry:</strong></td>
                    <td>{company.get('industry', 'N/A')}</td>
                </tr>
                <tr>
                    <td><strong>Authorized Capital:</strong></td>
                    <td>{format_number(company.get('authorised_capital', 0))}</td>
                </tr>
            </table>
        </div>
    """, unsafe_allow_html=True)


def create_top_companies_chart(df: pd.DataFrame, metric: str = 'authorised_capital', top_n: int = 10) -> go.Figure:
    """
    Create a horizontal bar chart of top companies.
    
    Args:
        df: Input dataframe
        metric: Metric to rank by
        top_n: Number of top companies
        
    Returns:
        go.Figure: Plotly figure
    """
    if metric not in df.columns or 'company_name' not in df.columns:
        fig = go.Figure()
        fig.add_annotation(text=f"Required columns not found")
        return fig
    
    top_companies = df.nlargest(top_n, metric)[['company_name', metric]].sort_values(metric)
    
    if len(top_companies) == 0:
        fig = go.Figure()
        fig.add_annotation(text="No data available")
        return fig
    
    fig = go.Figure(data=[
        go.Bar(
            y=top_companies['company_name'],
            x=top_companies[metric],
            orientation='h',
            marker=dict(color='#667eea'),
            hovertemplate='<b>%{y}</b><br>%{x:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f'Top {top_n} Companies by {metric.replace("_", " ").title()}',
        xaxis_title=metric.replace("_", " ").title(),
        yaxis_title='Company Name',
        height=400,
        hovermode='y unified',
        showlegend=False,
        margin=dict(l=200, r=20, t=40, b=20)
    )
    
    return fig
