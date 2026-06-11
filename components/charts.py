"""Data visualization components."""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, List


def create_state_distribution_chart(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Create state distribution bar chart."""
    # Check if column exists
    if 'registered_state' not in df.columns:
        return go.Figure().add_annotation(text="State column not found")
    
    state_counts = df['registered_state'].value_counts().head(top_n).sort_values(ascending=True)
    
    if len(state_counts) == 0:
        return go.Figure().add_annotation(text="No state data available")
    
    fig = go.Figure(data=[
        go.Bar(
            y=state_counts.index,
            x=state_counts.values,
            orientation='h',
            marker=dict(color='#667eea'),
            hovertemplate='<b>%{y}</b><br>%{x} companies<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f'Top {top_n} States by Company Count',
        xaxis_title='Number of Companies',
        yaxis_title='State',
        height=400,
        margin=dict(l=150, r=20, t=40, b=20),
        showlegend=False
    )
    
    return fig


def create_industry_distribution_chart(df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """Create industry distribution pie chart."""
    # Check if column exists
    if 'industry' not in df.columns:
        return go.Figure().add_annotation(text="Industry column not found")
    
    industry_counts = df['industry'].value_counts().head(top_n)
    others = df['industry'].value_counts()[top_n:].sum() if len(df['industry'].value_counts()) > top_n else 0
    
    if others > 0:
        industry_counts['Others'] = others
    
    if len(industry_counts) == 0:
        return go.Figure().add_annotation(text="No industry data available")
    
    fig = go.Figure(data=[
        go.Pie(
            labels=industry_counts.index,
            values=industry_counts.values,
            hovertemplate='<b>%{label}</b><br>%{value} companies<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f'Industry Distribution (Top {top_n})',
        height=450,
        showlegend=True
    )
    
    return fig


def create_status_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Create company status distribution."""
    # Check if column exists
    if 'company_status' not in df.columns:
        return go.Figure().add_annotation(text="Status column not found")
    
    status_counts = df['company_status'].value_counts()
    
    if len(status_counts) == 0:
        return go.Figure().add_annotation(text="No status data available")
    
    colors = {
        'Active': '#22c55e',
        'Inactive': '#ef4444',
        'Strike Off': '#000000',
        'Under Liquidation': '#f97316'
    }
    
    color_list = [colors.get(status, '#999') for status in status_counts.index]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            marker=dict(colors=color_list),
            hovertemplate='<b>%{label}</b><br>%{value} companies<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Company Status Distribution',
        height=400,
        showlegend=True
    )
    
    return fig


def create_capital_distribution_chart(df: pd.DataFrame) -> go.Figure:
    """Create authorized capital distribution."""
    if 'authorised_capital' not in df.columns:
        return go.Figure().add_annotation(text="Capital column not found")
    
    capital_data = df['authorised_capital'].dropna()
    capital_data = capital_data[capital_data > 0]
    
    if len(capital_data) == 0:
        return go.Figure().add_annotation(text="No capital data available")
    
    fig = go.Figure(data=[
        go.Histogram(
            x=capital_data,
            nbinsx=50,
            marker=dict(color='#667eea'),
            hovertemplate='Capital Range: %{x}<br>Companies: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Authorized Capital Distribution',
        xaxis_title='Authorized Capital (₹)',
        yaxis_title='Number of Companies',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_incorporation_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Create incorporation year trend."""
    if 'date_of_incorporation' not in df.columns:
        return go.Figure().add_annotation(text="Incorporation date column not found")
    
    df_copy = df.copy()
    df_copy['year'] = pd.to_datetime(df_copy['date_of_incorporation'], errors='coerce').dt.year
    
    yearly_counts = df_copy['year'].value_counts().sort_index().tail(20)
    
    if len(yearly_counts) == 0:
        return go.Figure().add_annotation(text="No incorporation data available")
    
    fig = go.Figure(data=[
        go.Scatter(
            x=yearly_counts.index,
            y=yearly_counts.values,
            mode='lines+markers',
            line=dict(color='#667eea', width=2),
            marker=dict(size=6),
            fill='tozeroy',
            hovertemplate='Year: %{x}<br>Companies: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Company Incorporation Trend (Last 20 Years)',
        xaxis_title='Year',
        yaxis_title='Number of Companies',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def create_state_capital_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Create total capital by state."""
    if 'registered_state' not in df.columns or 'authorised_capital' not in df.columns:
        return go.Figure().add_annotation(text="Required columns not found")
    
    state_capital = df.groupby('registered_state')['authorised_capital'].sum().nlargest(top_n).sort_values()
    
    if len(state_capital) == 0:
        return go.Figure().add_annotation(text="No state capital data available")
    
    fig = go.Figure(data=[
        go.Bar(
            y=state_capital.index,
            x=state_capital.values,
            orientation='h',
            marker=dict(color='#764ba2'),
            hovertemplate='<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f'Top {top_n} States by Total Authorized Capital',
        xaxis_title='Total Authorized Capital (₹)',
        yaxis_title='State',
        height=400,
        margin=dict(l=150, r=20, t=40, b=20),
        showlegend=False
    )
    
    return fig


def create_industry_capital_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """Create total capital by industry."""
    if 'industry' not in df.columns or 'authorised_capital' not in df.columns:
        return go.Figure().add_annotation(text="Required columns not found")
    
    industry_capital = df.groupby('industry')['authorised_capital'].sum().nlargest(top_n).sort_values()
    
    if len(industry_capital) == 0:
        return go.Figure().add_annotation(text="No industry capital data available")
    
    fig = go.Figure(data=[
        go.Bar(
            y=industry_capital.index,
            x=industry_capital.values,
            orientation='h',
            marker=dict(color='#f59e0b'),
            hovertemplate='<b>%{y}</b><br>₹%{x:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f'Top {top_n} Industries by Total Authorized Capital',
        xaxis_title='Total Authorized Capital (₹)',
        yaxis_title='Industry',
        height=400,
        margin=dict(l=200, r=20, t=40, b=20),
        showlegend=False
    )
    
    return fig


def create_comparison_radar_chart(companies: List[pd.Series]) -> go.Figure:
    """Create radar chart for company comparison."""
    if not companies:
        return go.Figure()
    
    categories = ['Authorized Capital', 'Age (Years)', 'Capital Efficiency']
    
    fig = go.Figure()
    
    for company in companies:
        capital = company.get('authorised_capital', 0) / 1e7  # Scale down
        age = company.get('company_age_years', 0) if 'company_age_years' in company else 0
        efficiency = 50  # Placeholder
        
        fig.add_trace(go.Scatterpolar(
            r=[capital, age, efficiency],
            theta=categories,
            fill='toself',
            name=company.get('company_name', 'Company')
        ))
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title='Company Comparison',
        height=500,
        showlegend=True
    )
    
    return fig
