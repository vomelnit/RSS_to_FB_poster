## @package mail_remind
#  This module responsible for sending emails to inform that Facebook token will expire in few days
import smtplib
import os
import datetime
import log_func

logfile = log_func.logfile
gmail_user = 'vomelnytskyi@gmail.com'
gmail_password = 'password'

sent_from = gmail_user
sent_to = ['womelnitsky@gmail.com', 'digest-ua@ukr.net','info@autoconsulting.ua']
subject = u'Facebook token is going to expire'

body_text = "Facebook token is going to expire. Change it in file 'conf.py'."
message = "\r\n".join((
        "From: %s" % gmail_user,
        "To: %s" % sent_to,
        "Subject: %s" % subject ,
        "",
        body_text
    ))

## Connect to gmail via SMTP  and send email with text
#   No params
#   No return
def remind_to_refresh_token():
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, sent_to, message.encode('utf-8'))
        server.close()
    except Exception as exp_cause:
        print(exp_cause)
        log_func.logging(logfile, exp_cause)

## Check last modification date of file 'conf.py' and call remind_to_refresh_token() if modification was enough long ago
#   No params
#   No return
def compare_last_mod_date():
    last_mod_datetime = datetime.datetime.fromtimestamp(os.path.getmtime('conf.py'))
    today = datetime.datetime.today()
    diff = today - last_mod_datetime
    if (diff.days>54): remind_to_refresh_token()

    ###Uncomment this part to find out if program can send emails via SMTP and please check logfile. If there is no exceptions: everything is okay
    #remind_to_refresh_token()

