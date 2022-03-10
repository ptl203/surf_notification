import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
password = input("Type your password and press enter: ")
sender_email = "californiaburritowsc@gmail.com"
receiver_email = "californiaburritowsc@gmail.com"
message = """\
Subject: Hi there

This message is sent from Python."""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
