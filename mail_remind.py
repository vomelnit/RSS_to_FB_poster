import smtplib
import os
import datetime
import log_func

logfile = log_func.logfile
gmail_user = 'vomelnytskyi@gmail.com'
gmail_password = 'pass'

sent_from = gmail_user
sent_to = ['womelnitsky@gmail.com', 'digest-ua@ukr.net','info@autoconsulting.ua']
subject = u'Истекает срок Facebook токена'

body_text = "Истекает срок Facebook токена. Замените его в файле 'conf.py'. \n\nПодробная инструкция: ..."
message = "\r\n".join((
        "From: %s" % gmail_user,
        "To: %s" % sent_to,
        "Subject: %s" % subject ,
        "",
        body_text
    ))

def remind_to_refresh_token():
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, sent_to, message.encode('utf-8'))
        server.close()
    except Exception as exp_cause:
        log_func.logging(logfile, exp_cause)

def compare_last_mod_date():
    last_mod_datetime = datetime.datetime.fromtimestamp(os.path.getmtime('conf.py'))
    today = datetime.datetime.today()
    diff = today - last_mod_datetime
    if (diff.days>55): remind_to_refresh_token()

#remind_to_refresh_token()
