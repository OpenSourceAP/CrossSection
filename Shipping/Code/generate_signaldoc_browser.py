"""
ABOUTME: Generate interactive master-detail HTML browser for SignalDoc.csv
ABOUTME: Run with: python generate_signaldoc_browser.py [output_path]
INPUTS: 00_settings.txt (for paths), SignalDoc.csv from pathProject
OUTPUTS: Default path is pathStorage/SignalDoc-Browser.html (can override with command line argument)
"""

import pandas as pd
import json
import os
import sys
from pathlib import Path

def escape_html(text):
    """Escape HTML special characters"""
    if pd.isna(text) or text == '':
        return ''
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def format_value(val):
    """Format a value for display"""
    if pd.isna(val) or val == '':
        return ''
    return str(val)

def format_integer_value(val):
    """Format a value as an integer string when possible"""
    if pd.isna(val) or val == '':
        return ''
    try:
        return f"{int(float(val)):,}"
    except (ValueError, TypeError):
        return format_value(val)

def build_code_link(signalname, category):
    """Return the GitHub URL for the signal's implementation when available"""
    if not signalname:
        return ''

    normalized_category = (category or '').strip().lower()
    base_url = "https://github.com/OpenSourceAP/CrossSection/blob/master/Signals/pyCode"
    filename = f"{signalname}.py"

    if normalized_category == 'predictor':
        return f"{base_url}/Predictors/{filename}"
    if 'placebo' in normalized_category:
        return f"{base_url}/Placebos/{filename}"

    return ''

def main():
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Read settings from 00_settings.txt
    settings = {}
    with open('00_settings.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = [x.strip() for x in line.split(' = ', 1)]
                settings[key] = value

    pathProject = Path(settings['pathProject']).expanduser()
    pathStorage = Path(settings['pathStorage']).expanduser()

    # Determine output path
    if len(sys.argv) > 1:
        output_path = Path(sys.argv[1])
    else:
        output_path = pathStorage / 'SignalDoc-Browser.html'

    print(f"Reading SignalDoc.csv...")
    doc = pd.read_csv(pathProject / 'SignalDoc.csv')

    # Create AuthorYear column with Journal
    doc['AuthorYear'] = doc['Authors'].fillna('')

    # Add year and journal in parentheses
    year_journal = []
    for idx, row in doc.iterrows():
        parts = []
        year = str(row['Year']) if pd.notna(row['Year']) else ''
        journal = row['Journal'] if pd.notna(row['Journal']) else ''

        if year:
            parts.append(year)
        if journal:
            parts.append(journal)

        if parts:
            year_journal.append(' (' + ', '.join(parts) + ')')
        else:
            year_journal.append('')

    doc['AuthorYear'] = doc['AuthorYear'] + pd.Series(year_journal)

    predictability_map = {
        '1_clear': 'Clearly Significant (Predictor)',
        '2_likely': 'Likely Significant (Predictor)',
        '4_not': 'Not Significant (Placebo)',
        'indirect': 'Only indirect predictability evidence (Placebo)',
        '9_drop': 'Signal dropped from dataset (Placebo, see notes)'
    }

    # Prepare data for JSON
    signals = []
    for idx, row in doc.iterrows():
        # Rename "Drop" to "Dropped"
        category = format_value(row.get('Cat.Signal', ''))
        if category == 'Drop':
            category = 'Dropped'

        predictability_raw = row.get('Predictability in OP', '')
        if pd.isna(predictability_raw) or predictability_raw == '':
            predictability_value = ''
        else:
            predictability_key = str(predictability_raw).strip().lower()
            predictability_value = predictability_map.get(predictability_key, format_value(predictability_raw))

        signal = {
            'signalname': format_value(row.get('Acronym', '')),
            'Category': category,
            'AuthorYear': format_value(row['AuthorYear']),
            'Predictability': predictability_value,
            'Quality': format_value(row.get('Signal Rep Quality', '')),
            'GScholarCites202509': format_integer_value(row.get('GScholarCites202509', '')),
            'Description': format_value(row.get('LongDescription', '')),
            'Journal': format_value(row.get('Journal', '')),
            'FormCategory': format_value(row.get('Cat.Form', '')),
            'DataCategory': format_value(row.get('Cat.Data', '')),
            'EconomicCategory': format_value(row.get('Cat.Economic', '')),
            'SampleStart': format_value(row.get('SampleStartYear', '')),
            'SampleEnd': format_value(row.get('SampleEndYear', '')),
            'Acronym2': format_value(row.get('Acronym2', '')),
            'EvidenceSummary': format_value(row.get('Evidence Summary', '')),
            'KeyTable': format_value(row.get('Key Table in OP', '')),
            'TestInOP': format_value(row.get('Test in OP', '')),
            'Sign': format_value(row.get('Sign', '')),
            'Return': format_value(row.get('Return', '')),
            'TStat': format_value(row.get('T-Stat', '')),
            'StockWeight': format_value(row.get('Stock Weight', '')),
            'LSQuantile': format_value(row.get('LS Quantile', '')),
            'QuantileFilter': format_value(row.get('Quantile Filter', '')),
            'PortfolioPeriod': format_value(row.get('Portfolio Period', '')),
            'StartMonth': format_value(row.get('Start Month', '')),
            'Filter': format_value(row.get('Filter', '')),
            'Definition': format_value(row.get('Detailed Definition', '')),
            'Notes': format_value(row.get('Notes', '')),
            'CodeLink': build_code_link(format_value(row.get('Acronym', '')), category)
        }
        signals.append(signal)

    signals_json = json.dumps(signals, indent=2)

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Chen-Zimmermann (2020, CFR) Signal Library</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            height: 100vh;
            overflow: hidden;
        }}

        .container {{
            display: flex;
            flex-direction: column;
            height: 100vh;
        }}

        .header {{
            background: #2c3e50;
            color: white;
            padding: 1rem 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .header h1 {{
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }}

        .search-bar {{
            display: flex;
            gap: 1rem;
            margin-top: 0.75rem;
        }}

        .search-bar input {{
            flex: 1;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 0.9rem;
        }}

        .search-bar select {{
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 0.9rem;
            min-width: 200px;
        }}

        .main-content {{
            display: flex;
            flex: 1;
            overflow: hidden;
        }}

        .list-panel {{
            width: 450px;
            border-right: 1px solid #ddd;
            display: flex;
            flex-direction: column;
            background: #f8f9fa;
        }}

        .list-header {{
            padding: 0.75rem 1rem;
            background: #ecf0f1;
            border-bottom: 1px solid #ddd;
            font-weight: 600;
            color: #2c3e50;
        }}

        .signal-list {{
            flex: 1;
            overflow-y: scroll;
        }}

        .signal-item {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #e0e0e0;
            cursor: pointer;
            transition: background 0.2s;
        }}

        .signal-item:hover {{
            background: #e8eef2;
        }}

        .signal-item.active {{
            background: #3498db;
            color: white;
        }}

        .signal-item-name {{
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}

        .signal-item-acronym {{
            font-size: 0.85rem;
            color: #555;
            margin-bottom: 0.25rem;
            font-style: italic;
        }}

        .signal-item.active .signal-item-acronym {{
            color: #e0e0e0;
        }}

        .signal-item-meta {{
            font-size: 0.85rem;
            color: #666;
        }}

        .signal-item.active .signal-item-meta {{
            color: #ecf0f1;
        }}

        .detail-panel {{
            flex: 1;
            overflow-y: scroll;
            padding: 2rem;
            background: white;
        }}

        .detail-empty {{
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: #999;
            font-size: 1.1rem;
        }}

        .detail-content {{
            max-width: 800px;
        }}

        .detail-title {{
            font-size: 1.75rem;
            color: #2c3e50;
            margin-bottom: 1rem;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.5rem;
        }}

        .detail-field {{
            margin-bottom: 0.5rem;
        }}

        .detail-field.inline {{
            display: flex;
            gap: 2.0rem;
            align-items: baseline;
        }}

        .detail-field.block {{
            margin-bottom: 1rem;
        }}

        .detail-label {{
            font-weight: 600;
            color: #555;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .detail-field.inline .detail-label {{
            width: 220px;
            flex-shrink: 0;
            white-space: nowrap;
        }}

        .detail-field.block .detail-label {{
            margin-bottom: 0.25rem;
        }}

        .detail-value {{
            color: #333;
            line-height: 1.6;
            font-size: 0.95rem;
        }}

        .detail-field.inline .detail-value {{
            flex: 1;
        }}

        .detail-value.long-text {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 4px;
            border-left: 3px solid #3498db;
            margin-top: 0.25rem;
        }}

        .no-results {{
            padding: 2rem;
            text-align: center;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>The Chen-Zimmermann (2020, CFR) Signal Library</h1>
            <div class="search-bar">
                <select id="categoryFilter">
                    <option value="">All Categories</option>
                </select>
                <input type="text" id="searchInput" placeholder="Search signals...">
            </div>
        </div>

        <div class="main-content">
            <div class="list-panel">
                <div class="list-header">
                    <span id="signalCount">0 signals</span>
                </div>
                <div class="signal-list" id="signalList"></div>
            </div>

            <div class="detail-panel" id="detailPanel">
                <div class="detail-empty">Select a signal to view details</div>
            </div>
        </div>
    </div>

    <script>
        const signalsData = {signals_json};

        let filteredSignals = signalsData;
        let selectedSignal = null;

        // Initialize
        function init() {{
            populateCategoryFilter();
            renderSignalList();

            // Select BM signal by default
            const bmSignal = signalsData.find(s => s.signalname === 'BM');
            if (bmSignal) {{
                selectSignal('BM');
            }} else if (signalsData.length > 0) {{
                selectSignal(signalsData[0].signalname);
            }}

            document.getElementById('searchInput').addEventListener('input', filterSignals);
            document.getElementById('categoryFilter').addEventListener('change', filterSignals);
        }}

        function populateCategoryFilter() {{
            // Define specific order for categories
            const categoryOrder = ['Predictor', 'Placebo', 'Dropped'];
            const select = document.getElementById('categoryFilter');

            categoryOrder.forEach(cat => {{
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                select.appendChild(option);
            }});
        }}

        function getDetailTitle(signal) {{
            const baseDescription = (signal.Description || '').toString();
            const evidenceSummaryValue = (signal['EvidenceSummary'] || '').toString().trim().toLowerCase();
            const suffix = evidenceSummaryValue === 'hxz variant' ? ' (HXZ variation)' : '';
            return `${{baseDescription}}${{suffix}}`;
        }}

        function filterSignals() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const category = document.getElementById('categoryFilter').value;

            filteredSignals = signalsData.filter(signal => {{
                const detailTitle = getDetailTitle(signal).toLowerCase();
                const matchesSearch = !searchTerm ||
                    signal.signalname.toLowerCase().includes(searchTerm) ||
                    signal.Description.toLowerCase().includes(searchTerm) ||
                    signal.AuthorYear.toLowerCase().includes(searchTerm) ||
                    detailTitle.includes(searchTerm);

                const matchesCategory = !category || signal.Category === category;

                return matchesSearch && matchesCategory;
            }});

            renderSignalList();
        }}

        function renderSignalList() {{
            const listEl = document.getElementById('signalList');
            const countEl = document.getElementById('signalCount');

            countEl.textContent = `${{filteredSignals.length}} signal${{filteredSignals.length !== 1 ? 's' : ''}}`;

            if (filteredSignals.length === 0) {{
                listEl.innerHTML = '<div class="no-results">No signals found</div>';
                return;
            }}

            listEl.innerHTML = filteredSignals.map(signal => `
                <div class="signal-item ${{selectedSignal?.signalname === signal.signalname ? 'active' : ''}}"
                     onclick="selectSignal('${{signal.signalname}}')">
                    <div class="signal-item-name">${{getDetailTitle(signal)}}</div>
                    <div class="signal-item-acronym">${{signal.signalname}}</div>
                    <div class="signal-item-meta">${{signal.AuthorYear}}</div>
                </div>
            `).join('');
        }}

        function selectSignal(signalname) {{
            selectedSignal = signalsData.find(s => s.signalname === signalname);
            renderSignalList();
            renderDetailPanel();
        }}

        function renderDetailPanel() {{
            const panel = document.getElementById('detailPanel');

            if (!selectedSignal) {{
                panel.innerHTML = '<div class="detail-empty">Select a signal to view details</div>';
                return;
            }}

            const fields = [
                {{ key: 'signalname', label: 'Acronym', inline: true }},             
                {{ key: 'AuthorYear', label: 'Paper', inline: true }},                       
                {{ key: 'Predictability', label: 'Predictability Evidence', inline: true }},                
                {{ key: 'Definition', label: 'Definition', inline: false }},
                {{ key: 'CodeLink', label: 'Code', inline: true }},                
                {{ key: 'KeyTable', label: 'Table Replicated', inline: true }},
                {{ key: 'TestInOP', label: 'Predictability Test', inline: true }},
                {{ key: 'Sample', label: 'Sample', inline: true, computed: true }},
                {{ key: 'Sign', label: 'Sign of Predictability', inline: true }},
                {{ key: 'Return', label: 'Return (% Monthly)', inline: true }},
                {{ key: 'TStat', label: 'T-Stat', inline: true }},
                {{ key: 'StockWeight', label: 'Stock Weight', inline: true }},
                {{ key: 'LSQuantile', label: 'Long-Short Quantile', inline: true }},
                {{ key: 'QuantileFilter', label: 'Quantile Filter', inline: true }},
                {{ key: 'PortfolioPeriod', label: 'Portfolio Period', inline: true }},
                {{ key: 'StartMonth', label: 'Start Month', inline: true }},
                {{ key: 'Filter', label: 'Filter', inline: true }},
                {{ key: 'EvidenceSummary', label: 'Evidence Summary', inline: true }},
                {{ key: 'GScholarCites202509', label: 'GScholar Cites (2025)', inline: true }},                
                {{ key: 'Notes', label: 'Notes', inline: false }},
                {{ key: 'Category', label: 'Predictor or Placebo?', inline: true }},                
                {{ key: 'Acronym2', label: 'Acronym2', inline: true }},
                {{ key: 'Quality', label: 'Replication Quality', inline: true }},
                {{ key: 'FormCategory', label: 'Form Category', inline: true }},
                {{ key: 'DataCategory', label: 'Data Category', inline: true }},
                {{ key: 'EconomicCategory', label: 'Economic Category', inline: true }}
            ];

            const fieldsHtml = fields
                .filter(field => {{
                    if (field.computed && field.key === 'Sample') {{
                        return selectedSignal['SampleStart'] || selectedSignal['SampleEnd'];
                    }}
                    if (field.key === 'CodeLink') {{
                        return Boolean(selectedSignal[field.key]);
                    }}
                    return selectedSignal[field.key];
                }})
                .map(field => {{
                    let value = '';
                    let displayValue = '';
                    if (field.computed && field.key === 'Sample') {{
                        const start = selectedSignal['SampleStart'] || '';
                        const end = selectedSignal['SampleEnd'] || '';
                        if (start && end) {{
                            value = `${{start}}-${{end}}`;
                        }} else if (start) {{
                            value = `${{start}}-`;
                        }} else if (end) {{
                            value = `-${{end}}`;
                        }} else {{
                            value = '';
                        }}
                        displayValue = value;
                    }} else if (field.key === 'Sign') {{
                        const signValue = selectedSignal[field.key];
                        if (signValue === '1.0' || signValue === '1') {{
                            value = 'High signal implies high return';
                        }} else {{
                            value = 'High signal implies low return';
                        }}
                        displayValue = value;
                    }} else if (field.key === 'StockWeight') {{
                        const weightValue = selectedSignal[field.key];
                        if (weightValue === 'EW') {{
                            value = 'equal-weighted';
                        }} else {{
                            value = 'value-weighted';
                        }}
                        displayValue = value;
                    }} else if (field.key === 'EvidenceSummary') {{
                        value = selectedSignal[field.key].replace(/HXZ variant/g, 'Hou, Xue, Zhang (2020, RFS) created this variation from the original paper');
                        displayValue = value;
                    }} else if (field.key === 'CodeLink') {{
                        const linkUrl = selectedSignal[field.key];
                        value = linkUrl ? 'GitHub Link' : '';
                        displayValue = linkUrl ? `<a href="${{linkUrl}}" target="_blank" rel="noopener">GitHub Link</a>` : '';
                    }} else {{
                        value = selectedSignal[field.key] || '';
                        displayValue = value;
                    }}

                    const isLongText = value.length > 100;
                    const layoutClass = field.inline && !isLongText ? 'inline' : 'block';
                    const valueClass = (!field.inline || isLongText) ? 'long-text' : '';
                    return `
                        <div class="detail-field ${{layoutClass}}">
                            <div class="detail-label">${{field.label}}</div>
                            <div class="detail-value ${{valueClass}}">${{displayValue}}</div>
                        </div>
                    `;
                }})
                .join('');

            const detailTitle = getDetailTitle(selectedSignal);

            panel.innerHTML = `
                <div class="detail-content">
                    <div class="detail-title">${{detailTitle}}</div>
                    ${{fieldsHtml}}
                </div>
            `;

            panel.scrollTop = 0;
        }}

        init();
    </script>
</body>
</html>"""

    # Write output file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✓ Generated {output_path}")
    print(f"  Contains {len(signals)} signals")
    print(f"\nTo view: open {output_path.absolute()}")

if __name__ == '__main__':
    main()
