"""AI Insights generation utilities."""
import pandas as pd
from typing import List
import logging

logger = logging.getLogger(__name__)


def generate_dataset_insights(df: pd.DataFrame) -> List[str]:
    """
    Generate dataset-level insights.
    
    Args:
        df: Input dataframe
        
    Returns:
        List[str]: List of insights
    """
    insights = []
    
    # Total companies insight
    insights.append(f"📊 The dataset contains {len(df):,} companies registered with MCA.")
    
    # Status distribution
    if 'company_status' in df.columns:
        status_dist = df['company_status'].value_counts()
        active_pct = (status_dist.get('Active', 0) / len(df) * 100)
        insights.append(f"✅ {active_pct:.1f}% of companies have Active status.")
    
    # Capital distribution
    if 'authorised_capital' in df.columns:
        total_capital = df['authorised_capital'].sum()
        avg_capital = df['authorised_capital'].mean()
        insights.append(f"💰 Total authorized capital: ₹{total_capital/1e9:.2f} Billion (Avg: ₹{avg_capital/1e7:.2f} Crore)")
    
    # State distribution
    if 'registered_state' in df.columns:
        top_state = df['registered_state'].value_counts().index[0]
        top_state_count = df['registered_state'].value_counts().iloc[0]
        insights.append(f"🏢 {top_state} leads with {top_state_count:,} registered companies.")
    
    # Industry distribution
    if 'industry' in df.columns:
        top_industry = df['industry'].value_counts().index[0]
        top_industry_count = df['industry'].value_counts().iloc[0]
        insights.append(f"🏭 {top_industry} is the largest industry with {top_industry_count:,} companies.")
    
    return insights


def generate_state_insights(df: pd.DataFrame, state: str) -> List[str]:
    """
    Generate state-level insights.
    
    Args:
        df: Input dataframe
        state: State name
        
    Returns:
        List[str]: List of state insights
    """
    insights = []
    state_data = df[df['registered_state'] == state]
    
    if len(state_data) == 0:
        return [f"No data available for {state}"]
    
    insights.append(f"📍 {state} has {len(state_data):,} registered companies.")
    
    if 'company_status' in state_data.columns:
        active = len(state_data[state_data['company_status'] == 'Active'])
        insights.append(f"✅ {active:,} active companies in {state}.")
    
    if 'industry' in state_data.columns:
        top_ind = state_data['industry'].value_counts().index[0]
        insights.append(f"🏢 Top industry in {state}: {top_ind}")
    
    return insights


def generate_industry_insights(df: pd.DataFrame, industry: str) -> List[str]:
    """
    Generate industry-level insights.
    
    Args:
        df: Input dataframe
        industry: Industry name
        
    Returns:
        List[str]: List of industry insights
    """
    insights = []
    ind_data = df[df['industry'] == industry]
    
    if len(ind_data) == 0:
        return [f"No data available for {industry}"]
    
    insights.append(f"🏭 {industry} has {len(ind_data):,} companies.")
    
    if 'registered_state' in ind_data.columns:
        top_state = ind_data['registered_state'].value_counts().index[0]
        insights.append(f"📍 {top_state} has the most {industry} companies.")
    
    if 'authorised_capital' in ind_data.columns:
        total_cap = ind_data['authorised_capital'].sum()
        insights.append(f"💰 Total capital in {industry}: ₹{total_cap/1e9:.2f}B")
    
    return insights


def generate_capital_insights(df: pd.DataFrame) -> List[str]:
    """
    Generate capital-related insights.
    
    Args:
        df: Input dataframe
        
    Returns:
        List[str]: List of capital insights
    """
    insights = []
    
    if 'authorised_capital' not in df.columns:
        return insights
    
    auth_capital = df['authorised_capital'].sum()
    paid_capital = df['paid_up_capital'].sum() if 'paid_up_capital' in df.columns else 0
    
    insights.append(f"💰 Total Authorized Capital: ₹{auth_capital/1e9:.2f} Billion")
    insights.append(f"💵 Total Paid-Up Capital: ₹{paid_capital/1e9:.2f} Billion")
    
    # Capital efficiency
    if paid_capital > 0:
        efficiency = (paid_capital / auth_capital) * 100
        insights.append(f"📈 Capital Efficiency: {efficiency:.2f}%")
    
    # Top companies by capital
    top_company = df.loc[df['authorised_capital'].idxmax()]
    insights.append(f"🏆 Top company by capital: {top_company.get('company_name', 'N/A')}")
    
    return insights


def generate_growth_insights(df: pd.DataFrame) -> List[str]:
    """
    Generate growth and trend insights.
    
    Args:
        df: Input dataframe
        
    Returns:
        List[str]: List of growth insights
    """
    insights = []
    
    if 'date_of_incorporation' not in df.columns:
        return insights
    
    df_copy = df.copy()
    df_copy['incorporation_year'] = pd.to_datetime(df_copy['date_of_incorporation'], errors='coerce').dt.year
    
    yearly_counts = df_copy['incorporation_year'].value_counts().sort_index()
    
    if len(yearly_counts) > 1:
        recent_year = yearly_counts.index[-1]
        prev_year = yearly_counts.index[-2]
        recent_count = yearly_counts.iloc[-1]
        prev_count = yearly_counts.iloc[-2]
        
        growth = ((recent_count - prev_count) / prev_count * 100) if prev_count > 0 else 0
        insights.append(f"📊 {recent_year} incorporations: {recent_count:,} ({growth:+.1f}% vs {prev_year})")
    
    return insights
