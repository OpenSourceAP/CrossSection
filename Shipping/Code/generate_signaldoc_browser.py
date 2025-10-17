# ABOUTME: Generate interactive master-detail HTML browser for SignalDoc.csv
# ABOUTME: Run with: python generate_signal_browser.py [output_path]

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

def main():
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Determine output path
    if len(sys.argv) > 1:
        output_path = Path(sys.argv[1])
    else:
        output_path = Path('../SignalDoc-Browser.html')

    print(f"Reading SignalDoc.csv...")
    doc = pd.read_csv('../../SignalDoc.csv')

    # Create AuthorYear column
    doc['AuthorYear'] = doc['Authors'].fillna('') + ' ' + doc['Year'].fillna('').astype(str)
    doc['AuthorYear'] = doc['AuthorYear'].str.strip()

    # Prepare data for JSON
    signals = []
    for idx, row in doc.iterrows():
        # Rename "Drop" to "Dropped"
        category = format_value(row.get('Cat.Signal', ''))
        if category == 'Drop':
            category = 'Dropped'

        signal = {
            'signalname': format_value(row.get('Acronym', '')),
            'Category': category,
            'AuthorYear': format_value(row['AuthorYear']),
            'Predictability': format_value(row.get('Predictability in OP', '')),
            'Quality': format_value(row.get('Signal Rep Quality', '')),
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
            'Notes': format_value(row.get('Notes', ''))
        }
        signals.append(signal)

    signals_json = json.dumps(signals, indent=2)

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Chen-Zimmermann (2020) Signal Library</title>
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
            width: 350px;
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
            overflow-y: auto;
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

        .signal-item-meta {{
            font-size: 0.85rem;
            color: #666;
        }}

        .signal-item.active .signal-item-meta {{
            color: #ecf0f1;
        }}

        .detail-panel {{
            flex: 1;
            overflow-y: auto;
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
            font-size: 2rem;
            color: #2c3e50;
            margin-bottom: 1.5rem;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.5rem;
        }}

        .detail-field {{
            margin-bottom: 1.25rem;
        }}

        .detail-label {{
            font-weight: 600;
            color: #555;
            margin-bottom: 0.25rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .detail-value {{
            color: #333;
            line-height: 1.6;
            font-size: 1rem;
        }}

        .detail-value.long-text {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 4px;
            border-left: 3px solid #3498db;
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
            <h1>The Chen-Zimmermann (2020) Signal Library</h1>
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

        function filterSignals() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const category = document.getElementById('categoryFilter').value;

            filteredSignals = signalsData.filter(signal => {{
                const matchesSearch = !searchTerm ||
                    signal.signalname.toLowerCase().includes(searchTerm) ||
                    signal.Description.toLowerCase().includes(searchTerm) ||
                    signal.AuthorYear.toLowerCase().includes(searchTerm);

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
                    <div class="signal-item-name">${{signal.signalname}}</div>
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
                {{ key: 'signalname', label: 'Signal' }},
                {{ key: 'Category', label: 'Category' }},
                {{ key: 'Predictability', label: 'Predictability' }},
                {{ key: 'Quality', label: 'Quality' }},
                {{ key: 'AuthorYear', label: 'Authors' }},
                {{ key: 'Description', label: 'Description' }},
                {{ key: 'Journal', label: 'Journal' }},
                {{ key: 'FormCategory', label: 'Form Category' }},
                {{ key: 'DataCategory', label: 'Data Category' }},
                {{ key: 'EconomicCategory', label: 'Economic Category' }},
                {{ key: 'SampleStart', label: 'Sample Start' }},
                {{ key: 'SampleEnd', label: 'Sample End' }},
                {{ key: 'Acronym2', label: 'Acronym2' }},
                {{ key: 'EvidenceSummary', label: 'Evidence Summary' }},
                {{ key: 'KeyTable', label: 'Key Table' }},
                {{ key: 'TestInOP', label: 'Test in OP' }},
                {{ key: 'Sign', label: 'Sign' }},
                {{ key: 'Return', label: 'Return' }},
                {{ key: 'TStat', label: 'T-Stat' }},
                {{ key: 'StockWeight', label: 'Stock Weight' }},
                {{ key: 'LSQuantile', label: 'LS Quantile' }},
                {{ key: 'QuantileFilter', label: 'Quantile Filter' }},
                {{ key: 'PortfolioPeriod', label: 'Portfolio Period' }},
                {{ key: 'StartMonth', label: 'Start Month' }},
                {{ key: 'Filter', label: 'Filter' }},
                {{ key: 'Definition', label: 'Detailed Definition' }},
                {{ key: 'Notes', label: 'Notes' }}
            ];

            const fieldsHtml = fields
                .filter(field => selectedSignal[field.key])
                .map(field => {{
                    const value = selectedSignal[field.key];
                    const isLongText = value.length > 100;
                    return `
                        <div class="detail-field">
                            <div class="detail-label">${{field.label}}</div>
                            <div class="detail-value ${{isLongText ? 'long-text' : ''}}">${{value}}</div>
                        </div>
                    `;
                }})
                .join('');

            panel.innerHTML = `
                <div class="detail-content">
                    <div class="detail-title">${{selectedSignal.signalname}}</div>
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
