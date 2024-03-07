from flask import Flask, render_template, request
from send_mail import send_email  # Import send_email function
import csv
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads' 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_email', methods=['POST'])
def send_email_route():
    # Get form data from the request
    subject = request.form.get('emailSubject')
    body = request.form.get('emailBody')
    sender_email = request.form.get('senderEmail')
    smtp_password = request.form.get('smtpPassword')
    referral_code = request.form.get('referralCode')
    attachments = []
    if 'attachment' in request.files:
        # Loop through each uploaded file
        for attachment_file in request.files.getlist('attachment'):
            attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], attachment_file.filename)
            attachment_file.save(attachment_path)
            attachments.append(attachment_path)
    
    # Select uploaded file or use sample_list.csv if no file is uploaded
    uploaded_file = request.files.get('uploadedFile')
    uploaded_file_path = "uploaded_list.csv" if uploaded_file else "sample_list.csv"

    if referral_code:
        with open('referral_codes.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([referral_code])

    if uploaded_file:
        # Save uploaded file temporarily
        uploaded_file.save(uploaded_file_path)

    # Read email addresses from the CSV file
    receiver_emails = []
    with open(uploaded_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            receiver_emails.append(row[0])

    # Call send_email function for each receiver email
    for receiver_email in receiver_emails:
        send_email(subject, body, sender_email, receiver_email, smtp_password, attachments)

    # Delete attachment files after sending all emails
    for attachment in attachments:
        os.remove(attachment)
        
    # Delete temporary uploaded file if one was uploaded
    if uploaded_file:
        os.remove(uploaded_file_path)

    return "Emails sent successfully!"

if __name__ == '__main__':
    app.run(debug=True)
