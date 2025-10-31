from flask import Flask, render_template, url_for, redirect, request
import csv

app = Flask(__name__)  # ok if app.py sits beside /templates and /static

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route('/thankyou', methods=['GET'])
def thankyou():
    return render_template('thankyou.html')

def write_to_csv(data):
    with open('database.csv', mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([data.get('email',''), data.get('subject',''), data.get('message','')])

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect(url_for('thankyou'))  # ← redirect to route, not '/thankyou.html'
    except Exception as e:
        print('Form save error:', e)
        return 'Did not save to database', 500
