"""
ABOUTME: Generate interactive HTML browser for SignalDoc.csv with Open Asset Pricing website styling
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

    # Count statistics for display
    total_signals = len(signals)
    predictor_count = sum(1 for s in signals if s['Category'] == 'Predictor')
    placebo_count = sum(1 for s in signals if s['Category'] == 'Placebo')

    # Generate HTML with Open Asset Pricing website styling
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Open Source Asset Pricing - Signal Documentation Browser</title>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: Georgia, serif;
            background-color: #ffffff;
            color: #333;
            line-height: 1.6;
        }}

        /* Header styling to match Open Asset Pricing */
        .site-header {{
            text-align: center;
            padding: 2rem 0 1rem;
            background: white;
        }}

        .site-title {{
            font-size: 2rem;
            font-weight: normal;
            margin-bottom: 1rem;
            font-family: Georgia, serif;
        }}

        /* Navigation bar */
        .nav-bar {{
            text-align: center;
            padding: 0.5rem 0;
            border-top: 2px solid #666;
            border-bottom: 2px solid #666;
            margin: 0 auto;
            max-width: 1000px;
        }}

        .nav-bar a {{
            color: #333;
            text-decoration: none;
            padding: 0 2rem;
            font-family: Arial, sans-serif;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .nav-bar a:hover {{
            text-decoration: underline;
        }}

        .nav-bar a.active {{
            font-weight: bold;
        }}

        /* Main container - flipped layout with content area as main focus */
        .main-container {{
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 1rem;
            display: flex;
            gap: 2rem;
        }}

        /* Main content area (left side, larger) */
        .content-area {{
            flex: 1;
            min-width: 0;
        }}

        .content-box {{
            border: 1px solid #999;
            padding: 1.5rem;
            background: white;
        }}

        .content-box h2 {{
            font-size: 1.5rem;
            font-weight: normal;
            margin-bottom: 1rem;
            text-align: center;
        }}

        /* Signal details styling */
        .signal-title {{
            font-size: 1.75rem;
            color: #2c3e50;
            margin-bottom: 0.5rem;
            border-bottom: 3px solid #3498db;
            padding-bottom: 0.5rem;
        }}

        .signal-meta {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
            font-family: Arial, sans-serif;
            font-size: 0.9rem;
        }}

        .category-badge {{
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            font-size: 0.8rem;
            font-weight: normal;
            background: #f0f0f0;
        }}

        .category-predictor {{
            background: #d4edda;
            color: #155724;
        }}

        .category-placebo {{
            background: #fff3cd;
            color: #856404;
        }}

        .category-dropped {{
            background: #f8d7da;
            color: #721c24;
        }}

        /* Detail fields */
        .detail-row {{
            display: flex;
            padding: 0.75rem 0;
            border-bottom: 1px solid #e9ecef;
            font-family: Arial, sans-serif;
            font-size: 0.9rem;
        }}

        .detail-label {{
            width: 200px;
            font-weight: 600;
            color: #6c757d;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            flex-shrink: 0;
        }}

        .detail-value {{
            flex: 1;
            color: #333;
            line-height: 1.6;
        }}

        .detail-long {{
            background: #f9f9f9;
            padding: 1rem;
            border-left: 3px solid #999;
            margin: 1rem 0;
            border-radius: 3px;
            font-family: Arial, sans-serif;
            font-size: 0.9rem;
        }}

        /* Sidebar (right side, smaller) */
        .sidebar {{
            width: 400px;
        }}

        .sidebar-box {{
            border: 1px solid #999;
            padding: 1rem;
            background: white;
        }}

        .sidebar-box h3 {{
            font-size: 1rem;
            text-transform: uppercase;
            font-family: Arial, sans-serif;
            font-weight: normal;
            margin-bottom: 1rem;
            text-align: center;
        }}

        /* Search controls */
        .controls {{
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}

        .controls input, .controls select {{
            padding: 0.5rem;
            border: 1px solid #999;
            font-family: Arial, sans-serif;
            font-size: 0.9rem;
            width: 100%;
        }}

        /* Signal list */
        .signal-count {{
            font-family: Arial, sans-serif;
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 1rem;
            padding: 0.5rem 0;
            border-bottom: 1px solid #ddd;
        }}

        .signal-list {{
            max-height: 600px;
            overflow-y: auto;
        }}

        .signal-item {{
            padding: 0.75rem;
            border-bottom: 1px solid #e0e0e0;
            cursor: pointer;
            transition: background 0.2s;
            font-family: Arial, sans-serif;
        }}

        .signal-item:hover {{
            background: #f0f0f0;
        }}

        .signal-item.active {{
            background: #3498db;
            color: white;
        }}

        .signal-item-name {{
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.25rem;
        }}

        .signal-item-acronym {{
            font-size: 0.8rem;
            color: #666;
            font-style: italic;
        }}

        .signal-item.active .signal-item-acronym {{
            color: #e0e0e0;
        }}

        .signal-item-meta {{
            font-size: 0.75rem;
            color: #999;
            margin-top: 0.25rem;
        }}

        .signal-item.active .signal-item-meta {{
            color: #d0d0d0;
        }}

        /* Summary stats */
        .summary-stats {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            font-family: Arial, sans-serif;
            font-size: 0.9rem;
        }}

        .stat-item {{
            flex: 1;
            text-align: center;
            padding: 0.5rem;
            background: #f9f9f9;
            border: 1px solid #ddd;
        }}

        .stat-value {{
            font-size: 1.25rem;
            font-weight: bold;
            color: #333;
        }}

        .stat-label {{
            color: #666;
            font-size: 0.75rem;
            margin-top: 0.25rem;
        }}

        /* Footer */
        .site-footer {{
            background: #000;
            color: white;
            padding: 2rem;
            margin-top: 3rem;
            text-align: center;
            font-family: Arial, sans-serif;
            font-size: 0.85rem;
        }}

        .site-footer a {{
            color: white;
            text-decoration: underline;
        }}

        /* Links */
        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        /* No results message */
        .no-results {{
            padding: 2rem;
            text-align: center;
            color: #999;
            font-family: Arial, sans-serif;
        }}

        /* Empty state */
        .detail-empty {{
            padding: 3rem;
            text-align: center;
            color: #999;
            font-family: Arial, sans-serif;
            font-size: 1.1rem;
        }}

        /* Info text */
        .info-text {{
            font-family: Arial, sans-serif;
            font-size: 0.9rem;
            color: #666;
            margin: 1rem 0;
        }}
    </style>
</head>
<body>
    <div class="site-header">
        <h1 class="site-title">Open Source Asset Pricing</h1>
    </div>

    <nav class="nav-bar">
        <a href="#" class="active">SIGNAL BROWSER</a>
        <a href="https://www.openassetpricing.com/data/">DATA</a>
        <a href="https://www.openassetpricing.com/code/">CODE</a>
        <a href="https://www.openassetpricing.com/featured-in/">FEATURED IN</a>
        <a href="https://www.openassetpricing.com/faq/">FAQ</a>
    </nav>

    <div class="main-container">
        <!-- Main content area (left, larger) -->
        <div class="content-area">
            <div class="content-box">
                <h2>Chen-Zimmermann Signal Documentation Browser</h2>
                
                <p class="info-text">
                    This browser provides interactive access to signal documentation from the academic asset pricing literature. 
                    If you use this data, please cite our paper:
                    <br><br>
                    <em>@article{{ChenZimmermann2021, title={{Open Source Cross-Sectional Asset Pricing}}, author={{Chen, Andrew Y. and Tom Zimmermann}}, journal={{Critical Finance Review}}, year={{2022}}, volume={{11}}, number={{2}}, pages={{207-264}}}}</em>
                </p>

                <div id="detailPanel">
                    <div class="detail-empty">Select a signal from the list to view its details</div>
                </div>
            </div>
        </div>

        <!-- Sidebar (right, smaller) -->
        <div class="sidebar">
            <div class="sidebar-box">
                <h3>Signal List</h3>
                
                <div class="summary-stats">
                    <div class="stat-item">
                        <div class="stat-value">{total_signals}</div>
                        <div class="stat-label">Total</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{predictor_count}</div>
                        <div class="stat-label">Predictors</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{placebo_count}</div>
                        <div class="stat-label">Placebos</div>
                    </div>
                </div>

                <div class="controls">
                    <select id="categoryFilter">
                        <option value="">All Categories</option>
                        <option value="Predictor">Predictor</option>
                        <option value="Placebo">Placebo</option>
                        <option value="Dropped">Dropped</option>
                    </select>
                    <input type="text" id="searchInput" placeholder="Search signals...">
                </div>

                <div class="signal-count">
                    <span id="signalCount">Showing {total_signals} signals</span>
                </div>

                <div class="signal-list" id="signalList"></div>
            </div>
        </div>
    </div>

    <footer class="site-footer">
        <p>© 2025 Open Source Asset Pricing | Powered by Minimalist Blog WordPress Theme</p>
        <p style="margin-top: 1rem;">
            The views expressed here are those of the authors and do not necessarily reflect the position of the Board of Governors of the Federal Reserve or the Federal Reserve System.
        </p>
    </footer>

    <script>
        const signalsData = {signals_json};

        let filteredSignals = signalsData;
        let selectedSignal = null;

        // Initialize
        function init() {{
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

        function getDetailTitle(signal) {{
            const baseDescription = (signal.Description || '').toString();
            const evidenceSummaryValue = (signal['EvidenceSummary'] || '').toString().trim().toLowerCase();
            const suffix = evidenceSummaryValue === 'hxz variant' ? ' (HXZ variation)' : '';
            return `${{baseDescription}}${{suffix}}`;
        }}

        function getCategoryClass(category) {{
            if (category === 'Predictor') return 'category-predictor';
            if (category === 'Placebo') return 'category-placebo';
            if (category === 'Dropped') return 'category-dropped';
            return '';
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

            countEl.textContent = `Showing ${{filteredSignals.length}} signal${{filteredSignals.length !== 1 ? 's' : ''}}`;

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
                panel.innerHTML = '<div class="detail-empty">Select a signal from the list to view its details</div>';
                return;
            }}

            const detailTitle = getDetailTitle(selectedSignal);
            const categoryClass = getCategoryClass(selectedSignal.Category);

            // Build detail rows
            const fields = [
                {{ key: 'signalname', label: 'Acronym' }},             
                {{ key: 'AuthorYear', label: 'Paper' }},                       
                {{ key: 'Predictability', label: 'Predictability Evidence' }},
                {{ key: 'Definition', label: 'Definition', longText: true }},
                {{ key: 'CodeLink', label: 'Code', link: true }},                
                {{ key: 'KeyTable', label: 'Table Replicated' }},
                {{ key: 'TestInOP', label: 'Predictability Test' }},
                {{ key: 'Sample', label: 'Sample', computed: true }},
                {{ key: 'Sign', label: 'Sign of Predictability', transform: 'sign' }},
                {{ key: 'Return', label: 'Return (% Monthly)' }},
                {{ key: 'TStat', label: 'T-Stat' }},
                {{ key: 'StockWeight', label: 'Stock Weight', transform: 'weight' }},
                {{ key: 'LSQuantile', label: 'Long-Short Quantile' }},
                {{ key: 'QuantileFilter', label: 'Quantile Filter' }},
                {{ key: 'PortfolioPeriod', label: 'Portfolio Period' }},
                {{ key: 'StartMonth', label: 'Start Month' }},
                {{ key: 'Filter', label: 'Filter' }},
                {{ key: 'EvidenceSummary', label: 'Evidence Summary', transform: 'evidence' }},
                {{ key: 'GScholarCites202509', label: 'GScholar Cites (2025)' }},
                {{ key: 'Notes', label: 'Notes', longText: true }},
                {{ key: 'Quality', label: 'Replication Quality' }},
                {{ key: 'FormCategory', label: 'Form Category' }},
                {{ key: 'DataCategory', label: 'Data Category' }},
                {{ key: 'EconomicCategory', label: 'Economic Category' }}
            ];

            const detailRows = fields
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
                    
                    if (field.computed && field.key === 'Sample') {{
                        const start = selectedSignal['SampleStart'] || '';
                        const end = selectedSignal['SampleEnd'] || '';
                        if (start && end) {{
                            value = `${{start}}-${{end}}`;
                        }} else if (start) {{
                            value = `${{start}}-`;
                        }} else if (end) {{
                            value = `-${{end}}`;
                        }}
                    }} else if (field.transform === 'sign') {{
                        const signValue = selectedSignal[field.key];
                        if (signValue === '1.0' || signValue === '1') {{
                            value = 'High signal implies high return';
                        }} else {{
                            value = 'High signal implies low return';
                        }}
                    }} else if (field.transform === 'weight') {{
                        const weightValue = selectedSignal[field.key];
                        if (weightValue === 'EW') {{
                            value = 'equal-weighted';
                        }} else {{
                            value = 'value-weighted';
                        }}
                    }} else if (field.transform === 'evidence') {{
                        value = selectedSignal[field.key].replace(/HXZ variant/g, 'Hou, Xue, Zhang (2020, RFS) created this variation from the original paper');
                    }} else if (field.link && field.key === 'CodeLink') {{
                        const linkUrl = selectedSignal[field.key];
                        value = linkUrl ? `<a href="${{linkUrl}}" target="_blank" rel="noopener">GitHub Link</a>` : '';
                    }} else {{
                        value = selectedSignal[field.key] || '';
                    }}

                    if (field.longText && value) {{
                        return `
                            <div class="detail-long">
                                <div style="font-weight: 600; color: #6c757d; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
                                    ${{field.label}}
                                </div>
                                <div>${{value}}</div>
                            </div>
                        `;
                    }} else {{
                        return `
                            <div class="detail-row">
                                <div class="detail-label">${{field.label}}</div>
                                <div class="detail-value">${{value}}</div>
                            </div>
                        `;
                    }}
                }})
                .join('');

            panel.innerHTML = `
                <div class="signal-title">${{detailTitle}}</div>
                <div class="signal-meta">
                    <strong>${{selectedSignal.signalname}}</strong>
                    <span class="category-badge ${{categoryClass}}">${{selectedSignal.Category}}</span>
                </div>
                <div>
                    ${{detailRows}}
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
    print(f"    - {predictor_count} Predictors")
    print(f"    - {placebo_count} Placebos")
    print(f"\nTo view: open {output_path.absolute()}")

if __name__ == '__main__':
    main()