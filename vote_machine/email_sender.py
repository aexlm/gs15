import smtplib, ssl, textwrap
from email.message import EmailMessage


"""def sendmail(receiver_email, subject, content):
    smtp_server = "localhost"
    port = 1025  # For starttls
    sender_email = "gs15botmail@gmail.com"

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
"""


def sendmail(receiver_email, subject, content):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "gs15botmail@gmail.com"  # Enter your address
    #receiver_email = "pisevo5480@xxyxi.com"  # Enter receiver address
    password = "hx7G5i9Sn"
    #message = EmailMessage()
    message = """\
        
    objet : %s\n

    
    content : %s """ % (subject, content)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        print("Successful sent!!")
if __name__ == "__main__":
    sendmail("pisevo5480@xxyxi.com", "vote", "your code is")
