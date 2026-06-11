"""Filter utilities for data manipulation."""
import pandas as pd
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply multiple filters to dataframe.
    
    Args:
        df: Input dataframe
        filters: Dictionary of filter criteria
        
    Returns:
        pd.DataFrame: Filtered dataframe
    """
    filtered_df = df.copy()
    
    # State filter
    if 'state' in filters and filters['state']:
        filtered_df = filtered_df[filtered_df['registered_state'].isin(filters['state'])]
    
    # Company status filter
    if 'company_status' in filters and filters['company_status']:
        filtered_df = filtered_df[filtered_df['company_status'].isin(filters['company_status'])]
    
    # Category filter
    if 'company_category' in filters and filters['company_category']:
        filtered_df = filtered_df[filtered_df['company_category'].isin(filters['company_category'])]
    
    # Industry filter
    if 'industry' in filters and filters['industry']:
        filtered_df = filtered_df[filtered_df['industry'].isin(filters['industry'])]
    
    # Capital range filter
    if 'authorized_capital_range' in filters and filters['authorized_capital_range']:
        min_cap, max_cap = filters['authorized_capital_range']
        filtered_df = filtered_df[
            (filtered_df['authorised_capital'] >= min_cap) & 
            (filtered_df['authorised_capital'] <= max_cap)
        ]
    
    # Incorporation year filter
    if 'incorporation_year' in filters and filters['incorporation_year']:
        filtered_df = filtered_df[
            filtered_df['date_of_incorporation'].dt.year.isin(filters['incorporation_year'])
        ]
    
    # Listing status filter
    if 'listing_status' in filters and filters['listing_status']:
        filtered_df = filtered_df[filtered_df['listing_status'].isin(filters['listing_status'])]
    
    logger.info(f"Applied filters, result: {len(filtered_df)} records")
    return filtered_df


def search_companies(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """
    Search companies using fuzzy matching.
    
    Args:
        df: Input dataframe
        query: Search query string
        
    Returns:
        pd.DataFrame: Search results
    """
    if not query or query.strip() == "":
        return df
    
    query = query.lower().strip()
    
    # Search in company name
    mask = df['company_name'].str.lower().str.contains(query, na=False, regex=False)
    
    # Search in CIN if applicable
    if 'cin' in df.columns:
        mask = mask | df['cin'].str.contains(query, na=False, regex=False, case=False)
    
    # Search in registration number
    if 'registration_number' in df.columns:
        mask = mask | df['registration_number'].astype(str).str.contains(query, na=False, regex=False)
    
    return df[mask]


def get_filter_options(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Get available filter options from data.
    
    Args:
        df: Input dataframe
        
    Returns:
        dict: Filter options
    """
    options = {}
    
    if 'registered_state' in df.columns:
        options['states'] = sorted(df['registered_state'].dropna().unique().tolist())
    
    if 'company_status' in df.columns:
        options['company_status'] = sorted(df['company_status'].dropna().unique().tolist())
    
    if 'company_category' in df.columns:
        options['company_category'] = sorted(df['company_category'].dropna().unique().tolist())
    
    if 'industry' in df.columns:
        options['industries'] = sorted(df['industry'].dropna().unique().tolist())
    
    if 'listing_status' in df.columns:
        options['listing_status'] = sorted(df['listing_status'].dropna().unique().tolist())
    
    if 'class_of_company' in df.columns:
        options['class_of_company'] = sorted(df['class_of_company'].dropna().unique().tolist())
    
    return options
