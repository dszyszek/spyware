import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_mail(email, password, message_body, subject, file=None):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = email

    msg.attach(MIMEText(message_body, 'plain'))

    if file:
        with open(file, "rb") as fil:
            part = MIMEApplication(
                    fil.read(),
                    Name=os.path.basename(file)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file)
            msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, email, text)
    server.quit()
