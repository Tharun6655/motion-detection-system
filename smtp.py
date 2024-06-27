import smtplib

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("ogtc420@gmail.com", "iloveyouineveryuniverse")
    print("Successfully connected to the SMTP server.")
    server.quit()
except Exception as e:
    print(f"Failed to connect: {e}")
