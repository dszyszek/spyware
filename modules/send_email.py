import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_mail(email, password, message_body, subject, files=[]):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = email

    msg.attach(MIMEText(message_body, 'plain'))

    if files:
        for f in files:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                        fil.read(),
                        Name=os.path.basename(f)
                    )
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
                msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, email, text)
    server.quit()
