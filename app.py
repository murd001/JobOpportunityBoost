from flask import Flask, render_template, request
from send_mail import send_email  # Import send_email function
import csv
import os
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'mysite/uploads'

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
    product_key = request.form.get('productKey')

    # Ensure that the upload folder exists
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"Created upload folder: {upload_folder}")
    else:
        print(f"Upload folder already exists: {upload_folder}")

    # Process attachment
    attachment = request.files.get('attachment')
    if attachment:
        attachment_filename = attachment.filename
        attachment_path = os.path.join(upload_folder, attachment_filename)
        print(f"Attachment path: {attachment_path}")

        # Check if file exists and is writable
        if os.path.exists(attachment_path) and not os.access(attachment_path, os.W_OK):
            print(f"Error: File '{attachment_filename}' already exists and is not writable.")
        else:
            try:
                attachment.save(attachment_path)
                print(f"Attachment '{attachment_filename}' saved successfully.")
            except Exception as e:
                print(f"Error saving attachment '{attachment_filename}': {e}")

    # Select uploaded file or use sample_list.csv if no file is uploaded
    uploaded_file = request.files.get('uploadedFile')
    uploaded_file_path = "uploaded_list.csv" if uploaded_file else "mysite/Unique_Email_List.csv"

    if referral_code:
        with open('referral_codes.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([referral_code])

    if sender_email:
        with open('customer_emails.csv','a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([sender_email])

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
        if product_key == 'a7781':
            send_email(subject, body, sender_email, receiver_email, smtp_password, attachment_path)

    # Delete temporary uploaded file if one was uploaded
    if uploaded_file:
        os.remove(uploaded_file_path)

    # Delete contents of the uploads folder
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error deleting file/directory: {e}")

    return "Emails sent successfully!"

if __name__ == '__main__':
    app.run(debug=True)
