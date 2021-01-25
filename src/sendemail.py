import smtplib
from passwords import details


def sendEmail(message):
    email = details['email']
    password = details['password']
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()
