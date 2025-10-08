#%%
import pandas as pd
import polars as pl

placebo_name = 'AssetGrowth_q'
compq_varlist = ['atq']

#%%
# find missing obs

# read in csvs
stata_file = f"../Data/Placebos/{placebo_name}.csv"
python_file = f"../pyData/Placebos/{placebo_name}.csv"

stata_df = pl.read_csv(stata_file).rename({placebo_name: 'stata'})
python_df = pl.read_csv(python_file).rename({placebo_name: 'python'})

both = python_df.join(stata_df, on=['permno', 'yyyymm'], how='full', coalesce=True)

missing_in_python = both.filter(
    ~both['stata'].is_null() & both['python'].is_null()
)

# add gvkeys from signalmastertable
mastertable = pl.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet',
    columns=['permno', 'time_avail_m', 'gvkey']).with_columns(
        yyyymm = pl.col('time_avail_m').dt.year() * 100 + pl.col('time_avail_m').dt.month()
    )

missing_in_python = missing_in_python.join(mastertable, on=['permno', 'yyyymm'], how='left')

print(f'num obs missing from python: {len(missing_in_python)}')

print("sample of missing from python:")
print(missing_in_python.head(10))

#%%
# check Intermediate/m_QCompustat

# read in data
stata_compq = pd.read_stata('../Data/Intermediate/m_QCompustat.dta')
stata_compq = pl.from_pandas(stata_compq).select(
    ['gvkey', 'time_avail_m'] + compq_varlist
)

python_compq = pl.read_parquet('../pyData/Intermediate/m_QCompustat.parquet')
python_compq = python_compq.select(
    ['gvkey', 'time_avail_m'] + compq_varlist
)

stata_compq = stata_compq.rename({col: f'{col}_stata' for col in compq_varlist})
python_compq = python_compq.rename({col: f'{col}_python' for col in compq_varlist})

#%%

both_compq = python_compq.join(stata_compq, on=['gvkey', 'time_avail_m'], how='full', coalesce=True)

pl.Config.set_tbl_cols(12)
pl.Config.set_tbl_rows(36)

# filter for gvkey-time_avail_m
print("comparing m_QCompustat for the missing in python obs")
print(
    missing_in_python.join(
        both_compq.with_columns(
            pl.col('gvkey').cast(pl.Float64)
        ),
        on=['gvkey', 'time_avail_m'],
        how='left'
    ).drop(['time_avail_m'])
)

