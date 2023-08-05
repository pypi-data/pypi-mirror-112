import datetime

# 本月时间：假设此刻时间是 2021-07-07 17:04:15.889853
now = datetime.datetime.now()                       # 2021-07-07 17:04:15.889853 <class datetime>
timeformat_year = now.strftime("%Y")                # 2021 <str>
timeformat_month = now.strftime("%Y%m")             # 202107 <str>
timeformat_day = now.strftime("%Y%m%d")             # 20210707 <str>
timeformat_hour = now.strftime("%Y%m%d%H")          # 2021070717 <str>
timeformat_min = now.strftime("%Y%m%d%H%M")         # 202107071704 <str>
timeformat_second = now.strftime("%Y%m%d%H%M%S")    # 20210707170415 <str>


def difTime(dif_day, timeformat_type='day'):
    """间隔时间

    Args:
        dif_day (int): 间隔时间差天数. Defaults to int.
        timeformat_type (str, optional): 要返回的时间戳格式. Defaults to 'day'.

    Returns:
        [str]: 返回字符串类型的时间戳
    """
    now = datetime.datetime.now()
    if timeformat_type == 'year':
        timeformat_x = (now + datetime.timedelta(days=dif_day)).strftime("%Y")
    elif timeformat_type == 'month':
        timeformat_x = (now + datetime.timedelta(days=dif_day)).strftime("%Y%m")
    elif timeformat_type == 'month_num':
        timeformat_x = int((now + datetime.timedelta(days=dif_day)).strftime("%m"))
    elif timeformat_type == 'day':
        timeformat_x = (now + datetime.timedelta(days=dif_day)).strftime("%Y%m%d")
    elif timeformat_type == 'hour':
        timeformat_x = (now + datetime.timedelta(days=dif_day)).strftime("%Y%m%d%H")
    elif timeformat_type == 'min':
        timeformat_x = (now + datetime.timedelta(days=dif_day)).strftime("%Y%m%d%H%M")
    elif timeformat_type == 'second':
        timeformat_x = (now + datetime.timedelta(days=dif_day)).strftime("%Y%m%d%H%M%S")

    return timeformat_x
    
