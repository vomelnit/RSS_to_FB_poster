import datetime

logfile = "log.log"

def logging(logfile_name,exception_msg):
    with open(logfile_name, 'a') as log:
        now  = datetime.datetime.now()
        log.write(now.strftime("%d/%m/%y %H:%M") +' ' + str(exception_msg) + '\n')