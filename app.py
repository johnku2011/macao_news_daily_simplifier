# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 17:36:52 2023

@author: John.Ku
"""

from flask import Flask, render_template, request
import glob

import pandas as pd
import datetime
import re
from urllib.parse import unquote

def get_csv_files():
    return glob.glob('./data/*.csv')

def read_csv(file_path):
    return pd.read_csv(file_path)

def filter_by_today(data):
    current_date = datetime.date.today()   
    formatted_date = current_date.strftime("%Y-%m/%d/")
    export_date = current_date.strftime("%Y%m%d")
    filtered_files = []
    for file in files:
        file_date = re.search(r'(\d{8})', file).group(1)
        if file_date == export_date:
            filtered_files.append(file)
    return filtered_files

def get_selected_file(files):
    today_files = filter_by_today(files)
    if len(today_files) > 0:
        return today_files[0]
    else:
        return files[0]

files = get_csv_files()

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    
    files = get_csv_files()
    
    selected_file = get_selected_file(files)
    
    df = read_csv(selected_file)
    
    data = df.to_dict('records')
    
    # Render the template with the data
    return render_template('index.html', files=files, selected_file=selected_file, data=data)

@app.route('/<path:filename>')
def select_file(filename):
    files = get_csv_files()
    df = read_csv(filename)
    data = df.to_dict('records')
    return render_template('index.html', files=files, selected_file=filename, data=data)

@app.route('/copy', methods=['POST'])
def copy():
    summary = request.form['summary']
    content = request.form['content']

    # Perform copy action here (e.g., using the clipboard library)

    flash('News copied successfully!')
    return render_template('index.html')


# Custom filter for regex_replace
@app.template_filter('regex_replace')
def regex_replace(s, pattern, repl):
    return re.sub(pattern, repl, s)


if __name__ == '__main__':
    app.debug = True
    app.run()

