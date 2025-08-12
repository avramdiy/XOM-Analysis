import pandas as pd
from flask import Flask, render_template_string
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

def load_html_to_df(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = f.read()
    soup = BeautifulSoup(raw_data, 'html.parser')
    table = soup.find('table')
    if table:
        try:
            df = pd.read_html(str(table))[0]
        except Exception:
            df = pd.DataFrame()
    else:
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

def plot_decade(df, column='Close'):
    plt.figure(figsize=(8, 3))
    plt.plot(df['Date'], df[column], label=column)
    plt.title(f"{column} Price Over Time")
    plt.xlabel("Date")
    plt.ylabel(column)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f'<img src="data:image/png;base64,{img_base64}"/>'

def plot_moving_average(df, column='Close', window=20):
    plt.figure(figsize=(8, 3))
    plt.plot(df['Date'], df[column], label='Close')
    plt.plot(df['Date'], df[column].rolling(window=window).mean(), label=f'{window}-Day MA')
    plt.title(f"{column} & {window}-Day Moving Average")
    plt.xlabel("Date")
    plt.ylabel(column)
    plt.legend()
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f'<img src="data:image/png;base64,{img_base64}"/>'

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
                decade_tables += ddf.head(5).to_html(index=False)  # Show only first 5 rows
                decade_tables += "<h4>Summary Statistics</h4>"
                decade_tables += get_summary_stats(ddf)
                # Visualization for each decade
                if 'Close' in ddf.columns:
                    decade_tables += "<h4>Close Price Trend</h4>"
                    decade_tables += plot_decade(ddf, column='Close')
                    decade_tables += "<h4>20-Day Moving Average</h4>"
                    decade_tables += plot_moving_average(ddf, column='Close', window=20)
        html_table = df.head(10).to_html(index=False)  # Only show first 10 rows
    return render_template_string("""
        <html>
        <head><title>HTML DataFrame by Decade</title></head>
        <body>
            <h2>Full DataFrame (First 10 Rows)</h2>
            {{ table|safe }}
            <hr>
            <h2>DataFrame Split by Decade (First 5 Rows)</h2>
            {{ decade_tables|safe }}
        </body>
        </html>
    """, table=html_table, decade_tables=decade_tables)

if __name__ == '__main__':
    app.run(debug=True)