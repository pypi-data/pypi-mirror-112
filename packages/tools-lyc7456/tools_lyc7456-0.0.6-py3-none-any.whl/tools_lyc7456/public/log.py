import os
import logging

# Write by lyc at 2019-3-29
# V2019-7-4：分离logger继承关系，多个logger对象写到不同的日志文件
# V2021-7-7：优化注释，上传成包


def writeLog(logfile, name='errorlog', flag=True):
    """[打印日志对象]

    Args:
        logfile ([str]): [日志文件绝对路径]
        name (str, optional): [自定义日志对象名称，用于区分不用的对象打印的日志到不同的文件]. Defaults to 'errorlog'.
        flag (bool, optional): [True-默认日志格式，同时输出日志到标准屏幕和日志文件；False-用于打印文件列表，每行只包含一个文件名]. Defaults to True.

    Returns:
        [object]: [logger]
    """
    os.makedirs(os.path.dirname(logfile), exist_ok=True)  # 创建文件目录
    if flag:
        logformater = logging.Formatter(
            '%(asctime)s [%(levelname)s]:%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logformater = logging.Formatter('%(message)s')

    # 绑定日志输出到文件
    fh = logging.FileHandler(logfile, encoding='utf-8')
    fh.setFormatter(logformater)

    # 绑定日志数据到屏幕
    sh = logging.StreamHandler()
    sh.setFormatter(logformater)

    logger = logging.getLogger(name)
    logger.setLevel('INFO')
    logger.addHandler(sh)
    logger.addHandler(fh)

    return logger
