# Stata `label var` Command Translation to Python

## Overview

The `label var` command in Stata adds descriptive labels to variables for documentation and display purposes. While pandas doesn't have an exact equivalent, there are several ways to preserve variable metadata in Python.

## Stata Syntax and Usage

### Basic Syntax
```stata
label variable varname "Variable description"
label var varname "Variable description"    [abbreviated form]
```

### Common Patterns from Our Codebase

**Example 1: Simple label (Size.do)**
```stata
label var Size "Size"
```

**Example 2: Descriptive label (BM.do)**
```stata
label var BM "Book-to-market, Original, Stattman (1980)"
```

**Example 3: Technical description (Accruals.do)**
```stata
label var Accruals "Accruals"
```

**Example 4: Complex predictor label (Beta.do)**
```stata
label var Beta "CAPM Beta"
```

**Example 5: Units and methodology (CFP.do)**
```stata
label var cfp "Cash flow to price"
```

## Python Translation Patterns

### Method 1: Comments in Code (Most Common)
```python
# Stata: label var Size "Size"
df['Size'] = np.log(df['mve_c'])  # Size: Market capitalization (log)
```

### Method 2: Dictionary Documentation
```python
# Create variable labels dictionary
variable_labels = {
    'Size': 'Size: Market capitalization (log)',
    'BM': 'Book-to-market, Original, Stattman (1980)',
    'Beta': 'CAPM Beta',
    'Accruals': 'Accruals based on Sloan (1996)',
    'cfp': 'Cash flow to price'
}

# Apply during variable creation
df['Size'] = np.log(df['mve_c'])  # variable_labels['Size']
```

### Method 3: DataFrame Attributes (Advanced)
```python
# Store labels as DataFrame attribute
df.attrs['variable_labels'] = {
    'Size': 'Size: Market capitalization (log)',
    'BM': 'Book-to-market, Original, Stattman (1980)',
    'Beta': 'CAPM Beta'
}
```

### Method 4: Custom Metadata Class
```python
class LabeledDataFrame(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._variable_labels = {}
    
    def label_var(self, varname, label):
        """Add variable label (similar to Stata)"""
        self._variable_labels[varname] = label
    
    def get_label(self, varname):
        """Get variable label"""
        return self._variable_labels.get(varname, varname)
    
    def describe_labels(self):
        """Show all variable labels"""
        for var, label in self._variable_labels.items():
            print(f"{var}: {label}")

# Usage
df = LabeledDataFrame(data)
df.label_var('Size', 'Size: Market capitalization (log)')
```

## Complete Translation Examples

### Example 1: Size Predictor
**Stata:**
```stata
gen Size = log(mve_c)
label var Size "Size"
```

**Python:**
```python
# Method 1: Inline comment
df['Size'] = np.log(df['mve_c'])  # Size: Market capitalization (log)

# Method 2: Documentation dictionary
variable_labels = {'Size': 'Size: Market capitalization (log)'}
df['Size'] = np.log(df['mve_c'])
```

### Example 2: Complex Label
**Stata:**
```stata
gen BM = log(ceqt / me_datadate)
label var BM "Book-to-market, Original, Stattman (1980)"
```

**Python:**
```python
# Create variable with comprehensive documentation
df['BM'] = np.log(df['ceqt'] / df['me_datadate'])
# BM: Book-to-market ratio based on Stattman (1980)
# Formula: log(book equity / market equity at datadate)

# Or using documentation dictionary
variable_labels = {
    'BM': 'Book-to-market, Original, Stattman (1980)'
}
```

### Example 3: Multiple Variables with Labels
**Stata:**
```stata
gen Accruals = calculation
label var Accruals "Accruals"
gen Beta = calculation  
label var Beta "CAPM Beta"
gen Size = calculation
label var Size "Size"
```

**Python:**
```python
# Method 1: Inline documentation
df['Accruals'] = accruals_calculation  # Accruals based on Sloan (1996)
df['Beta'] = beta_calculation          # CAPM Beta from rolling regression
df['Size'] = size_calculation          # Size: Market capitalization (log)

# Method 2: Centralized documentation
VARIABLE_LABELS = {
    'Accruals': 'Accruals based on Sloan (1996)',
    'Beta': 'CAPM Beta from rolling regression', 
    'Size': 'Size: Market capitalization (log)'
}

def add_variable_with_label(df, varname, calculation, labels_dict):
    """Add variable with automatic labeling"""
    df[varname] = calculation
    print(f"Created {varname}: {labels_dict.get(varname, 'No label')}")

# Usage
add_variable_with_label(df, 'Size', np.log(df['mve_c']), VARIABLE_LABELS)
```

## Documentation Strategies

### Strategy 1: Header Comments
```python
"""
Predictor Variable Definitions:
- Size: Market capitalization (log) based on CRSP market value
- BM: Book-to-market ratio, Original methodology from Stattman (1980)  
- Beta: CAPM Beta estimated from 60-month rolling regression
- Accruals: Total accruals based on Sloan (1996) equation 1
"""
```

### Strategy 2: Variable Creation Functions
```python
def create_size_predictor(df):
    """
    Create Size predictor variable.
    
    Definition: Market capitalization (log)
    Source: CRSP market value of equity
    Reference: Standard size factor in asset pricing
    """
    df['Size'] = np.log(df['mve_c'])
    return df

def create_bm_predictor(df):
    """
    Create Book-to-Market predictor variable.
    
    Definition: Book-to-market ratio (log)
    Formula: log(book equity / market equity)
    Reference: Stattman (1980), original specification
    """
    df['BM'] = np.log(df['ceqt'] / df['me_datadate'])
    return df
```

### Strategy 3: Metadata Export
```python
def export_variable_documentation(df, labels_dict, filename):
    """Export variable documentation to CSV"""
    doc_df = pd.DataFrame([
        {'Variable': var, 'Label': label, 'Type': str(df[var].dtype)}
        for var, label in labels_dict.items()
        if var in df.columns
    ])
    doc_df.to_csv(filename, index=False)

# Usage
export_variable_documentation(df, VARIABLE_LABELS, 'variable_documentation.csv')
```

## Advanced Documentation Patterns

### Jupyter Notebook Documentation
```python
# Use markdown cells for variable documentation
"""
## Variable Definitions

| Variable | Description | Source | Reference |
|----------|-------------|--------|-----------|
| Size | Market cap (log) | CRSP | Standard factor |
| BM | Book-to-market | Compustat + CRSP | Stattman (1980) |
| Beta | CAPM Beta | Returns regression | CAPM model |
"""
```

### Schema Documentation
```python
import json

# Create schema with variable descriptions
predictor_schema = {
    "variables": {
        "Size": {
            "description": "Size: Market capitalization (log)",
            "formula": "log(market_value_equity)",
            "source": "CRSP",
            "reference": "Standard size factor"
        },
        "BM": {
            "description": "Book-to-market, Original, Stattman (1980)",
            "formula": "log(book_equity / market_equity)",
            "source": "Compustat + CRSP",
            "reference": "Stattman (1980)"
        }
    }
}

# Save schema
with open('predictor_schema.json', 'w') as f:
    json.dump(predictor_schema, f, indent=2)
```

## Integration with Our Project

### ABOUTME Documentation Pattern
```python
# ABOUTME: Creates Size predictor - market capitalization (log)
# ABOUTME: Based on standard size factor in asset pricing literature

import pandas as pd
import numpy as np

def create_size_predictor():
    """
    Size Predictor Creation
    
    Input: SignalMasterTable.parquet (mve_c column)
    Output: Size predictor (log market capitalization)
    Reference: Standard size factor in finance literature
    """
    # Load data with market value
    df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')[['permno', 'time_avail_m', 'mve_c']]
    
    # Create Size predictor: Market capitalization (log)
    df['Size'] = np.log(df['mve_c'])
    
    return df[['permno', 'time_avail_m', 'Size']]
```

### Validation Documentation
```python
def validate_predictor_creation(df, predictor_name, description):
    """
    Validate and document predictor creation
    
    Parameters:
    df: DataFrame with predictor
    predictor_name: Name of predictor variable
    description: Variable description (equivalent to Stata label)
    """
    print(f"\n=== {predictor_name} Predictor Validation ===")
    print(f"Description: {description}")
    print(f"Observations: {len(df)}")
    print(f"Non-missing: {df[predictor_name].notna().sum()}")
    print(f"Summary statistics:")
    print(df[predictor_name].describe())

# Usage
validate_predictor_creation(df, 'Size', 'Size: Market capitalization (log)')
```

## Validation Checklist

When documenting variables in Python:
1. ✅ Include variable description in comments or documentation
2. ✅ Document formula/calculation method
3. ✅ Reference source data and literature
4. ✅ Maintain consistent documentation format
5. ✅ Export documentation for external use if needed

## Common Documentation Approaches

### ❌ LIMITED: No documentation
```python
df['Size'] = np.log(df['mve_c'])  # No description
```

### ✅ GOOD: Inline comments
```python
df['Size'] = np.log(df['mve_c'])  # Size: Market capitalization (log)
```

### ✅ BETTER: Function documentation
```python
def create_size_predictor(df):
    """Create Size predictor: Market capitalization (log)"""
    return np.log(df['mve_c'])
```

### ✅ BEST: Comprehensive documentation
```python
def create_size_predictor(df):
    """
    Create Size predictor variable.
    
    Definition: Market capitalization (log)
    Formula: log(market_value_equity)
    Source: CRSP market value of equity (mve_c)
    Reference: Standard size factor in asset pricing literature
    
    Returns: Series with Size predictor values
    """
    return np.log(df['mve_c'])
```

## Project Integration

For our specific project, the most practical approach is:

1. **Inline comments** for simple variables
2. **Function docstrings** for complex calculations  
3. **Header documentation** in each predictor file
4. **ABOUTME comments** following project standards

This maintains clarity while being compatible with our existing codebase structure.