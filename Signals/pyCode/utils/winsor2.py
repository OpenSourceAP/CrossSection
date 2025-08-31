# ABOUTME: winsor2.py - Python implementation of Stata's winsor2 command
# ABOUTME: Provides winsorization and trimming functionality with exact Stata replication

"""
Python implementation of Stata's winsor2 command.

Usage:
    from utils.winsor2 import winsor2
    
    # Basic trimming (set extreme values to NaN)
    df = winsor2(df, ['variable'], trim=True, replace=True)
    
    # Trimming with custom cuts and grouping
    df = winsor2(df, ['var1', 'var2'], trim=True, replace=True, cuts=[1, 99], by=['group_var'])
    
    # Winsorizing (clamp to percentiles)
    df = winsor2(df, ['variable'], trim=False, replace=True, cuts=[5, 95])

Inputs:
    - DataFrame with variables to process
    - Variable list, cuts, grouping options
    
Outputs:
    - DataFrame with winsorized/trimmed variables
"""

import polars as pl
import pandas as pd
from typing import Union, List, Optional


def winsor2(
    df: Union[pl.DataFrame, pd.DataFrame], 
    varlist: List[str], 
    replace: bool = False, 
    trim: bool = False, 
    cuts: List[float] = [1, 99], 
    by: Optional[Union[str, List[str]]] = None, 
    suffix: str = "_w"
) -> Union[pl.DataFrame, pd.DataFrame]:
    """
    Replicate Stata winsor2 functionality exactly.
    
    Args:
        df: Input DataFrame (Polars or Pandas)
        varlist: List of column names to winsorize/trim
        replace: If True, modify original columns. If False, create new columns with suffix
        trim: If True, set extreme values to NaN. If False, clamp to percentiles (winsorize)
        cuts: [low, high] percentiles (0-100 scale). Default [1, 99]
        by: Column name(s) for grouping. If None, compute percentiles over entire dataset
        suffix: Suffix for new columns when replace=False. Default "_w" for winsorize, "_tr" for trim
        
    Returns:
        DataFrame with processed variables
        
    Examples:
        # Stata: winsor2 FErr, replace cuts(1 99) trim by(time_avail_m)
        df = winsor2(df, ['FErr'], replace=True, trim=True, cuts=[1, 99], by=['time_avail_m'])
        
        # Stata: winsor2 temp*, replace cuts(0.1 99.9) trim by(fyear)  
        df = winsor2(df, ['tempVar1', 'tempVar2'], replace=True, trim=True, cuts=[0.1, 99.9], by=['fyear'])
        
        # Stata: winsor2 tempRet60, replace cut(1 99) trim
        df = winsor2(df, ['tempRet60'], replace=True, trim=True, cuts=[1, 99])
    """
    
    # Validate inputs
    if len(cuts) != 2:
        raise ValueError("cuts must contain exactly 2 values [low, high]")
    
    low_cut, high_cut = cuts
    if low_cut >= high_cut:
        raise ValueError("Low cut must be less than high cut")
    
    if low_cut < 0 or high_cut > 100:
        raise ValueError("Cuts must be between 0 and 100")
    
    # Convert cuts to decimal (Stata uses 0-100 scale, quantile functions use 0-1 scale)
    low_pct = low_cut / 100.0
    high_pct = high_cut / 100.0
    
    # Set default suffix based on operation
    if suffix == "_w" and trim:
        suffix = "_tr"
    
    # Handle both Polars and Pandas DataFrames
    is_polars = isinstance(df, pl.DataFrame)
    
    if is_polars:
        return _winsor2_polars(df, varlist, replace, trim, low_pct, high_pct, by, suffix, low_cut, high_cut)
    else:
        return _winsor2_pandas(df, varlist, replace, trim, low_pct, high_pct, by, suffix, low_cut, high_cut)


def _winsor2_polars(
    df: pl.DataFrame, 
    varlist: List[str], 
    replace: bool, 
    trim: bool, 
    low_pct: float, 
    high_pct: float, 
    by: Optional[Union[str, List[str]]], 
    suffix: str,
    low_cut: float,
    high_cut: float
) -> pl.DataFrame:
    """Polars implementation of winsor2."""
    
    # Process each variable
    for var in varlist:
        if var not in df.columns:
            raise ValueError(f"Variable '{var}' not found in DataFrame")
        
        # Determine target column name
        target_col = var if replace else f"{var}{suffix}"
        
        # Check if target column already exists (when not replacing)
        if not replace and target_col in df.columns:
            raise ValueError(f"Variable '{target_col}' already exists. Use replace=True or different suffix.")
        
        # Compute percentiles
        if by is None:
            # No grouping - compute percentiles over entire dataset
            if low_cut == 0:
                # Use minimum when low cut is 0
                low_val_expr = pl.col(var).min()
            else:
                low_val_expr = pl.col(var).quantile(low_pct)
                
            if high_cut == 100:
                # Use maximum when high cut is 100  
                high_val_expr = pl.col(var).max()
            else:
                high_val_expr = pl.col(var).quantile(high_pct)
                
            df = df.with_columns([
                low_val_expr.alias(f"__{var}_low"),
                high_val_expr.alias(f"__{var}_high")
            ])
        else:
            # With grouping - compute percentiles within groups
            by_cols = [by] if isinstance(by, str) else by
            
            if low_cut == 0:
                low_val_expr = pl.col(var).min().over(by_cols)
            else:
                low_val_expr = pl.col(var).quantile(low_pct).over(by_cols)
                
            if high_cut == 100:
                high_val_expr = pl.col(var).max().over(by_cols)
            else:
                high_val_expr = pl.col(var).quantile(high_pct).over(by_cols)
                
            df = df.with_columns([
                low_val_expr.alias(f"__{var}_low"),
                high_val_expr.alias(f"__{var}_high")
            ])
        
        # Apply winsorization or trimming
        if trim:
            # Trim: set extreme values to null (matches Stata's trim behavior)
            df = df.with_columns(
                pl.when(
                    (pl.col(var) < pl.col(f"__{var}_low")) | 
                    (pl.col(var) > pl.col(f"__{var}_high"))
                )
                .then(None)  # Set to null/NaN
                .otherwise(pl.col(var))
                .alias(target_col)
            )
        else:
            # Winsorize: clamp to percentile values
            df = df.with_columns(
                pl.when(pl.col(var) < pl.col(f"__{var}_low"))
                .then(pl.col(f"__{var}_low"))
                .when(pl.col(var) > pl.col(f"__{var}_high"))
                .then(pl.col(f"__{var}_high"))
                .otherwise(pl.col(var))
                .alias(target_col)
            )
        
        # Clean up temporary columns
        df = df.drop([f"__{var}_low", f"__{var}_high"])
    
    return df


def _winsor2_pandas(
    df: pd.DataFrame, 
    varlist: List[str], 
    replace: bool, 
    trim: bool, 
    low_pct: float, 
    high_pct: float, 
    by: Optional[Union[str, List[str]]], 
    suffix: str,
    low_cut: float,
    high_cut: float
) -> pd.DataFrame:
    """Pandas implementation of winsor2."""
    
    # Make a copy to avoid modifying original
    df = df.copy()
    
    # Process each variable
    for var in varlist:
        if var not in df.columns:
            raise ValueError(f"Variable '{var}' not found in DataFrame")
            
        # Determine target column name
        target_col = var if replace else f"{var}{suffix}"
        
        # Check if target column already exists (when not replacing)
        if not replace and target_col in df.columns:
            raise ValueError(f"Variable '{target_col}' already exists. Use replace=True or different suffix.")
        
        if by is None:
            # No grouping - compute percentiles over entire dataset
            if low_cut == 0:
                low_val = df[var].min()
            else:
                low_val = df[var].quantile(low_pct)
                
            if high_cut == 100:
                high_val = df[var].max()
            else:
                high_val = df[var].quantile(high_pct)
            
            if trim:
                # Trim: set extreme values to NaN
                df[target_col] = df[var].where(
                    (df[var] >= low_val) & (df[var] <= high_val), 
                    other=pd.NA
                )
            else:
                # Winsorize: clamp to percentiles
                df[target_col] = df[var].clip(lower=low_val, upper=high_val)
        else:
            # With grouping - compute percentiles within groups
            by_cols = [by] if isinstance(by, str) else by
            
            def winsor_group(group):
                if low_cut == 0:
                    low_val = group[var].min()
                else:
                    low_val = group[var].quantile(low_pct)
                    
                if high_cut == 100:
                    high_val = group[var].max()
                else:
                    high_val = group[var].quantile(high_pct)
                
                if trim:
                    # Trim: set extreme values to NaN
                    return group[var].where(
                        (group[var] >= low_val) & (group[var] <= high_val), 
                        other=pd.NA
                    )
                else:
                    # Winsorize: clamp to percentiles
                    return group[var].clip(lower=low_val, upper=high_val)
            
            df[target_col] = df.groupby(by_cols, group_keys=False).apply(winsor_group).values
    
    return df


# Convenience function for common usage patterns
def winsor2_trim_by_group(df: Union[pl.DataFrame, pd.DataFrame], 
                          varlist: List[str], 
                          by: Union[str, List[str]], 
                          cuts: List[float] = [1, 99]) -> Union[pl.DataFrame, pd.DataFrame]:
    """
    Convenience function for the most common winsor2 usage: trim by group.
    
    Equivalent to Stata: winsor2 varlist, replace cuts(low high) trim by(groupvar)
    """
    return winsor2(df, varlist, replace=True, trim=True, cuts=cuts, by=by)


def winsor2_trim(df: Union[pl.DataFrame, pd.DataFrame], 
                 varlist: List[str], 
                 cuts: List[float] = [1, 99]) -> Union[pl.DataFrame, pd.DataFrame]:
    """
    Convenience function for trimming without grouping.
    
    Equivalent to Stata: winsor2 varlist, replace cuts(low high) trim  
    """
    return winsor2(df, varlist, replace=True, trim=True, cuts=cuts, by=None)