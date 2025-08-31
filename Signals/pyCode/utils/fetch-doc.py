# ABOUTME: Fetch and display signal documentation from SignalDoc.csv
# ABOUTME: Takes signal name as command line arg, displays readable info

import pandas as pd
import polars as pl
from polars import col as cc
import os
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Fetch signal documentation')
    parser.add_argument('signalname', help='Name of the signal to look up')
    args = parser.parse_args()
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # read signaldoc
    doc0 = pd.read_csv('../../../SignalDoc.csv')
    doc = pl.from_pandas(doc0)
    
    doc = doc.rename(
        {'Acronym': 'signalname'}
    ).with_columns(
        pl.concat_str([pl.col('Authors'), pl.lit(" "), pl.col('Year')]).alias('AuthorYear')
    )
    
    # select a signal
    docselect = doc.filter(
        cc('signalname') == args.signalname
    )
    
    if len(docselect) == 0:
        print(f"Signal '{args.signalname}' not found in SignalDoc.csv")
        sys.exit(1)
    
    # Format output for readability - show all columns in order
    row = docselect.row(0, named=True)
    
    # Define column order and display names
    columns = [
        ('signalname', 'Signal'),
        ('Cat.Signal', 'Category'),
        ('Predictability in OP', 'Predictability'),
        ('Signal Rep Quality', 'Quality'),
        ('AuthorYear', 'Authors'),
        ('LongDescription', 'Description'), 
        ('Journal', 'Journal'),
        ('Cat.Form', 'Form Category'),
        ('Cat.Data', 'Data Category'),
        ('Cat.Economic', 'Economic Category'),
        ('SampleStartYear', 'Sample Start'),
        ('SampleEndYear', 'Sample End'),
        ('Acronym2', 'Acronym2'),
        ('Evidence Summary', 'Evidence Summary'),
        ('Key Table in OP', 'Key Table'),
        ('Test in OP', 'Test in OP'),
        ('Sign', 'Sign'),
        ('Return', 'Return'),
        ('T-Stat', 'T-Stat'),
        ('Stock Weight', 'Stock Weight'),
        ('LS Quantile', 'LS Quantile'),
        ('Quantile Filter', 'Quantile Filter'),
        ('Portfolio Period', 'Portfolio Period'),
        ('Start Month', 'Start Month'),
        ('Filter', 'Filter'),
        ('Detailed Definition', 'Definition'),
        ('Notes', 'Notes')
    ]
    
    # Find max width for alignment
    max_width = max(len(display_name) for _, display_name in columns)
    
    for col, display_name in columns:
        if col in row and row[col] is not None and str(row[col]).strip() != '':
            print(f"{display_name:<{max_width}}: {row[col]}")

if __name__ == '__main__':
    main()