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

@app.route('/')
def show_dataframe():
    file_path = r'C:\Users\avram\OneDrive\Desktop\TRG Week 36\xom.us.txt'
    df = load_html_to_df(file_path)
    if "OpenInt" in df.columns:
        df = df.drop(columns=["OpenInt"])
    if df.empty:
        html_table = "<p>No table or tabular data found in the file.</p>"
    else:
        html_table = df.to_html(index=False)
    return render_template_string("""
        <html>
        <head><title>HTML DataFrame</title></head>
        <body>
            <h2>HTML DataFrame</h2>
            {{ table|safe }}
        </body>
        </html>
    """, table=html_table)

if __name__ == '__main__':
    app.run(debug=True)