"""Map CRSP CIZ distribution flags to legacy four-digit distribution codes.

How to run: import ``restore_distcd`` from a CRSP download script.
Inputs: CIZ distribution rows and the bundled official code crosswalk CSV.
Outputs: a copy of the rows with an integer ``distcd`` column; no file writes.

The CSV is the code-only projection of CRSP's
``CRSP_DistributionCode_SIZ_to_CIZ_Mapping.html`` (3,473 rows). The seven CIZ
fields in that crosswalk uniquely determine DISTCD. ``DisOrdinaryFlg`` is not
part of the published crosswalk. Keep literal ``N/A`` values as codes.
"""

from pathlib import Path

import pandas as pd


CODE_FIELDS = [
    'distype', 'disfreqtype', 'dispaymenttype', 'disdetailtype',
    'distaxtype', 'disorigcurtype', 'disamountsourcetype',
]
MAP_PATH = Path(__file__).with_name('crsp_distribution_code_map.csv')


def restore_distcd(events):
    """Attach exact legacy codes, raising on unknown or ambiguous flag tuples."""
    mapping = pd.read_csv(MAP_PATH, dtype={field: 'string' for field in CODE_FIELDS},
                          keep_default_na=False)
    if mapping.duplicated(CODE_FIELDS).any():
        raise ValueError('CRSP distribution crosswalk has ambiguous CIZ flag tuples.')
    if events[CODE_FIELDS].isna().any().any():
        raise ValueError('CIZ distribution rows have null code fields.')
    result = events.merge(mapping, on=CODE_FIELDS, how='left', validate='many_to_one',
                          indicator=True, sort=False)
    unknown = result['_merge'].ne('both')
    if unknown.any():
        examples = result.loc[unknown, CODE_FIELDS].drop_duplicates().head(10)
        raise ValueError(f'{unknown.sum()} CIZ distribution rows have unmapped flags:\n'
                         f'{examples.to_string(index=False)}')
    return result.drop(columns='_merge')
