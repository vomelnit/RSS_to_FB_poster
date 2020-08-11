## @package log_func
#  This module responsible for logging
import datetime

logfile = "log.log"

## Write 'exception_msg' into file 'logfile_name'
#   param logfile_name a string
#   param exception_msg a string
#   No return
def logging(logfile_name,exception_msg):
    with open(logfile_name, 'a') as log:
        now  = datetime.datetime.now()
        log.write(now.strftime("\n%d/%m/%y %H:%M") +' ' + str(exception_msg) + '\n')
        print("\nCheck logfile...\n")