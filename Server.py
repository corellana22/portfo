from flask import Flask, render_template, url_for, redirect, request
import csv
app = Flask(__name__)
print(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_file(data):
    with open('database.txt', mode = 'a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email}, {subject}, {message}')

def write_to_csv(data):
     with open('database.csv', mode = 'a', newline='') as database2:
         email = data['email']
         subject = data['subject']
         message = data['message']
         csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
         csv_writer.writerow([email,subject, message])

# import os

# def write_to_csv(data, filename='database.csv'):
#     # open with newline='' so csv handles line endings correctly
#     with open(filename, mode='a', newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=['email', 'subject', 'message'])
#         if f.tell() == 0:           # file is empty -> write header
#             writer.writeheader()
#         writer.writerow({
#             'email': data['email'],
#             'subject': data['subject'],
#             'message': data['message'],
#         })


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_to_csv(data)
            return redirect('/thankyou.html')
        except:
            return 'Did not save to database'
    else:
        return 'something went wrong. Try again!'