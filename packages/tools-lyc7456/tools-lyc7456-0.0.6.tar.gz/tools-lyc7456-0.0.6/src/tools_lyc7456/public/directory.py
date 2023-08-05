import os


def scanDir(targetDir):
    """[扫描目标目录] Write by lyc 2021-5-19

    Args:
        targetDir ([str]): [目标目录]

    Yields:
        [dic]: [返回文件的相对路径和绝对路径] 
                file_info = {
                'abs_file_path': ,      # 文件的绝对路径
                'rel_file_path': ,      # 文件的相对路径
                }
    """
    relativePath = targetDir.rsplit(os.sep, 1)[0] + os.sep  # 目标的相对路径
    relativeDir = targetDir.rsplit(os.sep, 1)[-1]  # 目标的相对路径下的第一级目录

    for (dirpath, dirnames, filenames) in os.walk(targetDir):
        for fn in filenames:
            # 把 dirpath 和 每个文件名拼接起来 就是全路径
            abs_file_path = os.path.join(dirpath, fn)  # 文件的绝对路径
            rel_file_path = abs_file_path.replace(relativePath, '')  # 文件的相对路径
            file_info = {
                'abs_file_path': abs_file_path,
                'rel_file_path': rel_file_path,
            }
            yield file_info
