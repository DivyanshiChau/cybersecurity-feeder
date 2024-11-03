from flask import Flask, render_template, redirect, url_for, jsonify
import json
import os
import subprocess

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FETCHED_DATA_PATH = os.path.join(BASE_DIR, "fetched_data")

def load_json_data(file_name):
    file_path = os.path.join(FETCHED_DATA_PATH, file_name)
    try:
        with open(file_path) as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []


@app.route('/')
def index():
    # Load all news data 
    selup_data = load_json_data("selup_data.json")
    cyware_data = load_json_data("cyware_news.json")
    cybersecurity_news = load_json_data("cybersecurity_news.json")
    
    
    all_news = selup_data + cyware_data + cybersecurity_news

    return render_template('index.html', news_data=all_news)


@app.route('/refresh')
def refresh_news():
    subprocess.run(["python", "toiup.py"])  # Run the toiup.py script
    subprocess.run(["python", "selup.py"])  # Run the selup.py script
    subprocess.run(["python", "cywareup.py"])  # Run the cywareup.py script

    
    selup_data = load_json_data("selup_data.json")
    cyware_data = load_json_data("cyware_news.json")
    cybersecurity_news = load_json_data("cybersecurity_news.json")

   
    all_news = selup_data + cyware_data + cybersecurity_news
    return jsonify(all_news)


@app.route('/selup')
def selup_news():
    selup_data = load_json_data("selup_data.json")
    return render_template('index.html', news_data=selup_data)


@app.route('/cywareup')
def cyware_news():
    cyware_data = load_json_data("cyware_news.json")
    return render_template('index.html', news_data=cyware_data)


@app.route('/cybersecurity')
def cybersecurity_news():
    cybersecurity_data = load_json_data("cybersecurity_news.json")
    return render_template('index.html', news_data=cybersecurity_data)

if __name__ == '__main__':
    app.run(debug=True)
