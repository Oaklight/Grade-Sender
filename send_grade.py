import csv
import smtplib
from email.mime.text import MIMEText
import time

DEBUG = True
user_account = ""
user_password = ""
user_smtp_server = ""
user_smtp_port = 587
file_to_open = ''

# text = "Hi {},\nWe are emailing you the score of your midterm\nStudent ID: {}\nScore: {}\nAverage: 63.0255\nStandard deviation: 15.3874\nYou can come to the office to check for the scoring.\nYou can ask for regrading, and you understand it may lead to a lower score.\nBest regards,\nSI140 Instructors"
content = """
        <html>
          <head></head>
          <body>
            <p>Hi {},<br><br>
               Here is your midterm score.<br>
               Student ID: {}, Your score: {},<br>
               You can come to the office to check for the score according to the time table:<br>
               13:00-14:00 Thr(13th); 19:00-20:00 Thr(13th); 13:00-14:00 Fri(14th);<br>
               Grade appeal will lead to regrading on your answersheet, which may result in a lower score.<br><br>
               Best regards,<br>
               Instructors
            </p>
          </body>
        </html>
        """


def send(mail, name, id, score):
    msg = MIMEText(content.format(name, id, score), 'html')
    msg['From'] = user_account
    msg['Subject'] = "Midterm Score for SI140 Probability and Statistics"
    if DEBUG:
        msg['To'] = user_account
    else:
        msg['To'] = mail
    server.send_message(msg)

try:
    server = smtplib.SMTP()
    server.connect(user_smtp_server, user_smtp_port)
    print('Conneted!', flush = True)
except:
    print('Failed to connect!', flush = True)
    exit(1)

try:
    server.starttls()
    server.login(user_account, user_password)
    print('Logged in!', flush = True)
except:
    server.quit()
    print('Failed to login!', flush = True)
    exit(1)

with open(file_to_open, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    i = 0
    for row in reader:
        entries = row[0].split(',')
        id = entries[1]
        name = entries[2]
        email = entries[5]
        score = entries[-1]
        # print(name, email, score)
        # print(content.format(name, id, score))
        while True:
            try:
                send(email, name, id, score)
                print('{} Sent!'.format(name), flush = True)
            except smtplib.SMTPSenderRefused:
                print('Failed to send to {}, because too fast!'.format(name), flush = True)
                print('Waiting for timeout ... ', end = '', flush = True)
                time.sleep(65)
                print('Done.', flush = True)
                round = 1;
                while True:
                    try:
                        send(email, name, id, score)
                        print('{} Sent!'.format(name), flush = True)
                    except smtplib.SMTPSenderRefused:
                        print('Failed to send to {}, because too fast!'.format(name), flush = True)
                        print('Waiting for timeout ... ', end = '', flush = True)
                        time.sleep(65*round)
                        print('Done.', flush = True)
                        round = round + 1
                    except smtplib.SMTPServerDisconnected:
                        server.connect(user_smtp_server, user_smtp_port)
                        server.starttls()
                        server.login(user_account, user_password)
                        print('reconnected!', flush = True)
                    else:
                        break
            except smtplib.SMTPServerDisconnected:
                server.connect(user_smtp_server, user_smtp_port)
                server.starttls()
                server.login(user_account, user_password)
                print('reconnected!', flush = True)
                round = 1;
                while True:
                    try:
                        send(email, name, id, score)
                        print('{} Sent!'.format(name), flush = True)
                    except smtplib.SMTPSenderRefused:
                        print('Failed to send to {}, because too fast!'.format(name), flush = True)
                        print('Waiting for timeout ... ', end = '', flush = True)
                        time.sleep(65*round)
                        print('Done.', flush = True)
                        round = round + 1
                    except smtplib.SMTPServerDisconnected:
                        server.connect(user_smtp_server, user_smtp_port)
                        server.starttls()
                        server.login(user_account, user_password)
                        print('reconnected!', flush = True)
                    else:
                        break
            else:
                break

        if i % 5 == 4:
            server.quit()
            print('Waiting for timeout ... ', end = '', flush = True)
            time.sleep(65)
            print('Done.', flush = True)
            try:
                server.connect(user_smtp_server, user_smtp_port)
                server.starttls()
                server.login(user_account, user_password)
            except:
                server.connect(user_smtp_server, user_smtp_port)
                server.starttls()
                server.login(user_account, user_password)
        if i % 15 == 14:
            server.quit()
            print('Waiting for timeout ... ', end = '', flush = True)
            time.sleep(65)
            print('Done.', flush = True)
            try:
                server.connect(user_smtp_server, user_smtp_port)
                server.starttls()
                server.login(user_account, user_password)
            except:
                server.connect(user_smtp_server, user_smtp_port)
                server.starttls()
                server.login(user_account, user_password)
        i = i + 1
server.quit()