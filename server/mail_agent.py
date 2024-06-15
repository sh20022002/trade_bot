import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(recipient_email, subject, body):
    """
    Send an email using SMTP.

    :param recipient_email: str, The email address of the recipient.
    :param subject: str, The subject of the email.
    :param body: str, The body of the email.
    :return: None
    :raises: Exception if there is an error sending the email.
    """
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = os.getenv('SENDER_EMAIL')
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the body with the msg instance
        msg.attach(MIMEText(body, 'plain'))

        # Create an SMTP session
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enable security

        # Login with the sender's email and password
        server.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Quit the SMTP session
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")
