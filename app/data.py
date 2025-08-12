import pandas as pd
from flask import Flask, render_template_string
from bs4 import BeautifulSoup

app = Flask(__name__)

def load_html_to_df(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = f.read()
    # Try to parse as HTML table first
    soup = BeautifulSoup(raw_data, 'html.parser')
    table = soup.find('table')
    if table:
        try:
            df = pd.read_html(str(table))[0]
        except Exception:
            df = pd.DataFrame()
    else:
        # If no HTML table, try to read as CSV or TSV
        try:
            df = pd.read_csv(file_path, sep=None, engine='python')
        except Exception:
            df = pd.DataFrame()
    return df

def split_by_decade(df):
    df['Date'] = pd.to_datetime(df['Date'])
    decades = {
        '1970s': df[(df['Date'] >= '1970-01-02') & (df['Date'] <= '1979-12-31')],
        '1980s': df[(df['Date'] >= '1980-01-01') & (df['Date'] <= '1989-12-31')],
        '1990s': df[(df['Date'] >= '1990-01-01') & (df['Date'] <= '1999-12-31')],
        '2000s': df[(df['Date'] >= '2000-01-01') & (df['Date'] <= '2009-12-31')],
        '2010s': df[(df['Date'] >= '2010-01-01') & (df['Date'] <= '2017-11-10')]
    }
    return decades

def get_summary_stats(df):
    return df.describe(include='all').to_html()

@app.route('/')
def show_dataframe():
    file_path = r'C:\Users\avram\OneDrive\Desktop\TRG Week 36\xom.us.txt'
    df = load_html_to_df(file_path)
    if "OpenInt" in df.columns:
        df = df.drop(columns=["OpenInt"])
    if df.empty:
        html_table = "<p>No table or tabular data found in the file.</p>"
        decade_tables = ""
    else:
        decades = split_by_decade(df)
        decade_tables = ""
        for name, ddf in decades.items():
            decade_tables += f"<h3>{name}</h3>"
            if ddf.empty:
                decade_tables += "<p>No data for this decade.</p>"
            else:
                decade_tables += ddf.to_html(index=False)
                decade_tables += "<h4>Summary Statistics</h4>"
                decade_tables += get_summary_stats(ddf)
        html_table = df.to_html(index=False)
    return render_template_string("""
        <html>
        <head><title>HTML DataFrame by Decade</title></head>
        <body>
            <h2>Full DataFrame</h2>
            {{ table|safe }}
            <hr>
            <h2>DataFrame Split by Decade</h2>
            {{ decade_tables|safe }}
        </body>
        </html>
    """, table=html_table, decade_tables=decade_tables)

if __name__ == '__main__':
    app.run(debug=True)