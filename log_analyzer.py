import pandas as pd
from datetime import datetime
import pytz


def parse_datetime(x):
    '''
    Parses datetime with timezone formatted as:
        `[day/month/year:hour:minute:second zone]`

    Example:
        `>>> parse_datetime('13/Nov/2015:11:45:42 +0000')`
        `datetime.datetime(2015, 11, 3, 11, 45, 4, tzinfo=<UTC>)`

    Due to problems parsing the timezone (`%z`) with `datetime.strptime`, the
    timezone will be obtained using the `pytz` library.
    '''
    dt = datetime.strptime(x[1:-7], '%d/%b/%Y:%H:%M:%S')
    dt_tz = int(x[-6:-3])*60+int(x[-3:-1])
    return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))


def set_user_agent(log):
    log['my_user_agent'] = "other"
    log.loc[log.user_agent.str.contains("android", case = False), 'my_user_agent']    = "android"
    log.loc[log.user_agent.str.contains("windows", case = False), 'my_user_agent']    = "windows"
    log.loc[log.user_agent.str.contains("iphone", case = False), 'my_user_agent']     = "iphone"
    log.loc[log.user_agent.str.contains("macintosh", case = False), 'my_user_agent']  = "mac"
    log.loc[log.user_agent.str.contains("x11", case = False), 'my_user_agent']        = "linux"
    log.user_agent = log.my_user_agent
    log = log.drop('my_user_agent', axis = 1)
    return log

def read_log(filename):
    log = pd.read_csv(
        filename,
        sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
        engine='python',
        usecols=[0, 3, 7, 8],
        names=['ip', 'time', 'page', 'user_agent'],
        na_values='-',
        header=None)
    return log


log_names = pd.read_csv("logs_names.csv", sep = ' ')
kk = {log_names.input.iloc[i] : log_names.output.iloc[i] for i in range(log_names.shape[0])}

for input, output in kk.items():
    log = read_log(input)
    log = set_user_agent(log)
    log.time = log.time.map(parse_datetime)
    output = f'{output}_{datetime.now().strftime("%Y%m%d")}.csv'
    log.to_csv(output, index = False)



