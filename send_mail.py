import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email(subject, body, sender_email, receiver_email, smtp_password, attachment=None):
    # Email configuration
    print(f"Subject: {subject}")
    print(f"Sender Email: {sender_email}")
    print(f"Receiver Email: {receiver_email}")

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    if attachment:
        print(f"Attachment: {attachment}")
        # Open and read the attachment file
        with open(attachment, 'rb') as attachment_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_file.read())

        # Encode the attachment and set the filename
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment)}')

        # Attach the attachment to the email message
        message.attach(part)

    try:
        # Connect to the SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
