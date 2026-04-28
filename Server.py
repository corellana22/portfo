from flask import Flask, render_template, url_for, redirect, request
import csv
import smtplib
from email.message import EmailMessage
import os

app = Flask(__name__)


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='assets/soccer.ico'))


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


def write_to_csv(data):
    with open('database.csv', mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            data.get('email', ''),
            data.get('subject', ''),
            data.get('message', '')
        ])


def send_email(data):
    sender_email = os.environ.get("PORTFOLIO_EMAIL")
    app_password = os.environ.get("PORTFOLIO_APP_PASSWORD")

    email = EmailMessage()
    email["From"] = sender_email
    email["To"] = sender_email
    email["Subject"] = f"Portfolio Contact: {data.get('subject', 'New Message')}"

    email.set_content(f"""
New portfolio message:

From: {data.get('email', '')}

Subject:
{data.get('subject', '')}

Message:
{data.get('message', '')}
""")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(email)


@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.form.to_dict()
        write_to_csv(data)

        try:
            send_email(data)
        except Exception as email_error:
            print("Email send error:", email_error)

        return redirect(url_for('thankyou'))

    except Exception as e:
        print('Form save error:', e)
        return 'Did not save to database', 500


if __name__ == "__main__":
    app.run(debug=True)
