import smtplib, ssl
from email.message import EmailMessage

def sendmail(receiver_email, subject, content):
    smtp_server = "localhost"
    port = 1025  # For starttls
    sender_email = "gs15@mail.com"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        message = EmailMessage()
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = receiver_email
        message.set_content(content)
        server.send_message(message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
