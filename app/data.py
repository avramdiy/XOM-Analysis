import pandas as pd
from flask import Flask, jsonify, Response

app = Flask(__name__)

def load_html_to_df(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_html = f.read()
    df = pd.DataFrame({'raw_html': [raw_html]})
    return df

@app.route('/load_html')
def load_html():
    file_path = r'C:\Users\avram\OneDrive\Desktop\TRG Week 36\xom.us.txt'
    df = load_html_to_df(file_path)
    return df.to_json(orient='records')