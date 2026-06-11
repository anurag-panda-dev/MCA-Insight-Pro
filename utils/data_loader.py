"""Data loading and caching utilities."""
import pandas as pd
import streamlit as st
from pathlib import Path
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize and standardize column names with flexible matching.
    
    Args:
        df: Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with standardized columns
    """
    # Create mapping dictionary for common column name variations
    column_mapping = {}
    df_cols_lower = {col.lower().strip(): col for col in df.columns}
    
    # Exact column name mappings from MCA CSV
    patterns = {
        'company_name': ['company name', 'companyname', 'name', 'company'],
        'cin': ['cin', 'corporate identification number'],
        'registered_state': ['company state', 'state', 'registered state', 'state code', 'reg state'],
        'industry': ['company industrial classification', 'industry', 'industry type', 'industry code'],
        'company_status': ['company status', 'status', 'current status'],
        'authorised_capital': ['authorized capital', 'authorised capital', 'auth capital', 'authorized cap'],
        'paid_up_capital': ['paidup capital', 'paid up capital', 'paid-up capital', 'paid up cap'],
        'company_category': ['company category', 'category', 'company type'],
        'company_sub_category': ['company sub category', 'sub category', 'subcategory', 'sub-category'],
        'roc': ['company roc', 'roc', 'roc code'],
        'registration_date': ['company registration date', 'registration date', 'registration_date', 'reg date'],
        'date_of_incorporation': ['date of incorporation', 'incorporation date', 'doi', 'incorporated date'],
        'registered_address': ['company address', 'address', 'registered address', 'reg address'],
        'pin_code': ['pin code', 'pincode', 'postal code', 'zip code'],
        'email_address': ['email', 'email address', 'company email'],
        'listing_status': ['listing status', 'listing', 'listed status'],
        'class_of_company': ['company class', 'class', 'class of company'],
        'nic_code': ['nic', 'nic code', 'nic2'],
    }
    
    # Map columns
    for standard_name, variations in patterns.items():
        for variation in variations:
            if variation in df_cols_lower:
                original_col = df_cols_lower[variation]
                column_mapping[original_col] = standard_name
                break
    
    # Rename columns
    if column_mapping:
        df = df.rename(columns=column_mapping)
        logger.info(f"Mapped {len(column_mapping)} columns")
    
    # Also standardize unmapped columns
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
    
    return df


@st.cache_data(ttl=3600)
def load_mca_data() -> pd.DataFrame:
    """
    Load MCA Master Data from CSV with caching.
    Handles multiple encodings and column name variations automatically.
    
    Returns:
        pd.DataFrame: The loaded company data
    """
    try:
        data_path = Path(__file__).parent.parent / "company_master_data_2025_06_30.csv"
        
        if not data_path.exists():
            st.error(f"Data file not found: {data_path}")
            return pd.DataFrame()
        
        # Try multiple encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252', 'utf-16', 'ascii']
        df = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(data_path, low_memory=False, encoding=encoding)
                used_encoding = encoding
                logger.info(f"Successfully loaded data with encoding: {encoding}")
                break
            except (UnicodeDecodeError, UnicodeError) as e:
                logger.debug(f"Failed with encoding {encoding}: {e}")
                continue
        
        if df is None:
            # Last resort: try with errors='ignore'
            df = pd.read_csv(data_path, low_memory=False, encoding='utf-8', errors='ignore')
            used_encoding = 'utf-8 (with error handling)'
            logger.info("Loaded data with error handling")
        
        logger.info(f"Loaded {len(df)} records from MCA data using {used_encoding}")
        logger.info(f"Original columns: {list(df.columns[:5])}")
        
        # Normalize column names
        df = normalize_columns(df)
        logger.info(f"Normalized columns: {list(df.columns[:5])}")
        
        return df
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


@st.cache_data
def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics about the dataset.
    
    Args:
        df: Input dataframe
        
    Returns:
        dict: Summary statistics
    """
    summary = {
        'total_companies': len(df),
        'total_states': df['registered_state'].nunique() if 'registered_state' in df.columns else 0,
        'total_industries': df['industry'].nunique() if 'industry' in df.columns else 0,
    }
    
    if 'company_status' in df.columns:
        status_counts = df['company_status'].value_counts()
        summary['active_companies'] = status_counts.get('Active', 0)
        summary['inactive_companies'] = status_counts.get('Inactive', 0)
        summary['strike_off'] = status_counts.get('Strike Off', 0)
        summary['liquidation'] = status_counts.get('Under Liquidation', 0)
    else:
        summary['active_companies'] = 0
        summary['inactive_companies'] = 0
        summary['strike_off'] = 0
        summary['liquidation'] = 0
    
    if 'authorised_capital' in df.columns:
        summary['total_authorized_capital'] = df['authorised_capital'].sum()
        summary['avg_authorized_capital'] = df['authorised_capital'].mean()
    else:
        summary['total_authorized_capital'] = 0
        summary['avg_authorized_capital'] = 0
    
    if 'paid_up_capital' in df.columns:
        summary['total_paid_up_capital'] = df['paid_up_capital'].sum()
        summary['avg_paid_up_capital'] = df['paid_up_capital'].mean()
    else:
        summary['total_paid_up_capital'] = 0
        summary['avg_paid_up_capital'] = 0
    
    return summary


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess data for analysis.
    
    Args:
        df: Input dataframe
        
    Returns:
        pd.DataFrame: Processed dataframe
    """
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Convert date columns
    date_columns = ['date_of_incorporation', 'registration_date', 'doi']
    for col in date_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
            except Exception as e:
                logger.debug(f"Could not convert {col} to datetime: {e}")
    
    # Calculate company age if incorporation date exists
    if 'date_of_incorporation' in df.columns:
        try:
            df['company_age_years'] = (pd.Timestamp.now() - df['date_of_incorporation']).dt.days / 365.25
        except:
            pass
    elif 'registration_date' in df.columns:
        # Use registration date as fallback for company age
        try:
            df['company_age_years'] = (pd.Timestamp.now() - df['registration_date']).dt.days / 365.25
        except:
            pass
    
    # Convert capital columns to numeric
    capital_columns = ['authorised_capital', 'paid_up_capital', 'auth_capital', 'paidup_capital']
    for col in capital_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            except Exception as e:
                logger.debug(f"Could not convert {col} to numeric: {e}")
    
    # Ensure key numeric columns exist with defaults
    if 'authorised_capital' not in df.columns:
        df['authorised_capital'] = 0
    if 'paid_up_capital' not in df.columns:
        df['paid_up_capital'] = 0
    
    # Ensure key string columns exist with defaults
    if 'company_status' not in df.columns:
        df['company_status'] = 'Unknown'
    if 'registered_state' not in df.columns:
        df['registered_state'] = 'Unknown'
    if 'industry' not in df.columns:
        df['industry'] = 'Unknown'
    if 'company_name' not in df.columns:
        df['company_name'] = 'Unknown'
    
    return df
