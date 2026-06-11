"""Data analysis services."""
import pandas as pd
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)


class CompanyAnalyzer:
    """Analyzes company data."""
    
    @staticmethod
    def get_company_profile(company: pd.Series) -> Dict:
        """
        Get detailed company profile.
        
        Args:
            company: Company data series
            
        Returns:
            dict: Company profile information
        """
        return {
            'basic': {
                'company_name': company.get('company_name', 'N/A'),
                'cin': company.get('cin', 'N/A'),
                'roc': company.get('roc', 'N/A'),
                'registration_number': company.get('registration_number', 'N/A'),
                'incorporation_date': company.get('date_of_incorporation', 'N/A'),
                'company_age_years': company.get('company_age_years', 'N/A'),
            },
            'legal': {
                'company_status': company.get('company_status', 'N/A'),
                'listing_status': company.get('listing_status', 'N/A'),
            },
            'classification': {
                'category': company.get('company_category', 'N/A'),
                'sub_category': company.get('company_sub_category', 'N/A'),
                'class': company.get('class_of_company', 'N/A'),
                'industry': company.get('industry', 'N/A'),
                'nic_code': company.get('nic_code', 'N/A'),
            },
            'location': {
                'state': company.get('registered_state', 'N/A'),
                'address': company.get('registered_address', 'N/A'),
                'email': company.get('email_address', 'N/A'),
            },
            'financial': {
                'authorized_capital': company.get('authorised_capital', 0),
                'paid_up_capital': company.get('paid_up_capital', 0),
            }
        }
    
    @staticmethod
    def get_company_metrics(df: pd.DataFrame, company: pd.Series) -> Dict:
        """
        Get company metrics and rankings.
        
        Args:
            df: Full dataset
            company: Company data series
            
        Returns:
            dict: Company metrics
        """
        metrics = {}
        
        # Capital ranking
        if 'authorised_capital' in df.columns:
            capital_rank = (df['authorised_capital'] >= company.get('authorised_capital', 0)).sum()
            metrics['capital_rank'] = capital_rank
            metrics['capital_percentile'] = (capital_rank / len(df)) * 100
        
        # State ranking
        if 'registered_state' in df.columns:
            state = company.get('registered_state')
            state_df = df[df['registered_state'] == state]
            if 'authorised_capital' in state_df.columns:
                state_rank = (state_df['authorised_capital'] >= company.get('authorised_capital', 0)).sum()
                metrics['state_rank'] = state_rank
        
        # Industry ranking
        if 'industry' in df.columns:
            industry = company.get('industry')
            industry_df = df[df['industry'] == industry]
            if 'authorised_capital' in industry_df.columns:
                industry_rank = (industry_df['authorised_capital'] >= company.get('authorised_capital', 0)).sum()
                metrics['industry_rank'] = industry_rank
        
        return metrics


class StateAnalyzer:
    """Analyzes state-level data."""
    
    @staticmethod
    def get_state_summary(df: pd.DataFrame, state: str) -> Dict:
        """Get state summary."""
        state_data = df[df['registered_state'] == state]
        
        if state_data.empty:
            return {}
        
        summary = {
            'total_companies': len(state_data),
            'active_companies': len(state_data[state_data['company_status'] == 'Active']) if 'company_status' in state_data.columns else 0,
            'total_capital': state_data['authorised_capital'].sum() if 'authorised_capital' in state_data.columns else 0,
            'avg_capital': state_data['authorised_capital'].mean() if 'authorised_capital' in state_data.columns else 0,
            'top_industry': state_data['industry'].value_counts().index[0] if 'industry' in state_data.columns else 'N/A',
            'top_category': state_data['company_category'].value_counts().index[0] if 'company_category' in state_data.columns else 'N/A',
        }
        
        return summary


class IndustryAnalyzer:
    """Analyzes industry-level data."""
    
    @staticmethod
    def get_industry_summary(df: pd.DataFrame, industry: str) -> Dict:
        """Get industry summary."""
        industry_data = df[df['industry'] == industry]
        
        if industry_data.empty:
            return {}
        
        summary = {
            'total_companies': len(industry_data),
            'active_companies': len(industry_data[industry_data['company_status'] == 'Active']) if 'company_status' in industry_data.columns else 0,
            'total_capital': industry_data['authorised_capital'].sum() if 'authorised_capital' in industry_data.columns else 0,
            'avg_capital': industry_data['authorised_capital'].mean() if 'authorised_capital' in industry_data.columns else 0,
            'top_state': industry_data['registered_state'].value_counts().index[0] if 'registered_state' in industry_data.columns else 'N/A',
            'top_category': industry_data['company_category'].value_counts().index[0] if 'company_category' in industry_data.columns else 'N/A',
        }
        
        return summary


def compare_companies(companies: List[pd.Series]) -> pd.DataFrame:
    """
    Create comparison dataframe for multiple companies.
    
    Args:
        companies: List of company series
        
    Returns:
        pd.DataFrame: Comparison dataframe
    """
    comparison_data = []
    
    for company in companies:
        comparison_data.append({
            'Company Name': company.get('company_name', 'N/A'),
            'State': company.get('registered_state', 'N/A'),
            'Industry': company.get('industry', 'N/A'),
            'Status': company.get('company_status', 'N/A'),
            'Authorized Capital': company.get('authorised_capital', 0),
            'Paid-Up Capital': company.get('paid_up_capital', 0),
            'Age (Years)': company.get('company_age_years', 0),
        })
    
    return pd.DataFrame(comparison_data)
