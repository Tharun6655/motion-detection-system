import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, body):
    sender_email = "ogtc420@gmail.com"
    receiver_email = "1da22cs427.cs@drait.edu.in"
    password = "ofzz smux bons oirn"  # Replace this with the generated App Password

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
