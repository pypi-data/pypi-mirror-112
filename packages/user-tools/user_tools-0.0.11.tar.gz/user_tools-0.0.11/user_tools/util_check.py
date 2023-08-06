#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Some checks on files or directories."""
import os
import re
from typing import Dict, List, Tuple, Union
from pathlib import Path


def is_exist(file_path: Union[str, Path], create: bool = False) -> bool:
    """Test whether file_path exists.

    :param file_path(str): The path that needs to be judged.\n
    :param create(bool): Whether to create. If create is True,\n
            create a directory named file_path if it does not exist.\n
    :return(bool): A boolean representing whether file_path exists."""

    if create and not os.path.exists(file_path):
        os.makedirs(file_path)
    return os.path.exists(file_path)


def is_not_null(file_path: Union[str, Path]) -> bool:
    """Test whether file_path is not null.

    :param file_path(str): The path that needs to be judged.\n
    :return(bool): Returns whether file_path is not null.\n
        Return True if file_path exist and not null.\n
        Return False, it may be the following:\n
            file_path not file or dir; file_path not exist."""

    result = False
    if is_exist(file_path):
        if file_or_dir(file_path) == "file":
            result = os.path.getsize(file_path) != 0
        elif file_or_dir(file_path) == "dir":
            result = bool(os.listdir(file_path))
    return result


def file_or_dir(file_path: Union[str, Path]) -> str:
    """ Returns file type of the file_path.

    :param file_path(str): The path that needs to be judged.\n
    :return(str): Returns file type of the file_path.\n
        The return values are as follows.\n
            "dir": If file_path is a directory,\n
            "file": If file_path is a file,\n
            file_path + "Not exist!": If file_path is not exist\n
            "Not file or dir!": If file_path not a dir or file."""

    result = ""
    if not is_exist(file_path):
        result = str(file_path) + "Not exist!"
    elif os.path.isdir(file_path):
        result = "dir"
    elif os.path.isfile(file_path):
        result = "file"
    else:
        result = "Not file or dir!"
    return result


def check_ip(ip: str) -> bool:
    """Test whether the IP is valid.

    :param ip(str): The IP that needs to be judged.\n
    :return(bool): Returns whether url is valid.\n
        Return False, if the IP is not legal."""

    ip_rex = r'(?=(\b|\D))(((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{1,2})|(2[0-4]\d)|(25[0-5]))(?=(\b|\D))'

    is_legal = re.match(re.compile(ip_rex), ip)
    if is_legal:
        return True
    else:
        return False


def check_url(url: str, style: str = "http") -> bool:
    """Test whether url is valid.

    :params url(str): The url that needs to be judged.\n
    :return(bool): Returns whether url is valid.\n
        Return False, if the style is not web or git.
    """

    result = False
    if style == "http":
        result = True if re.match(r'^https?:/{2}\w.+$', url) else False
    elif style == "git":
        result = True if re.match(
            r'^(http(s)?:\/\/([^\/]+?\/){2}|git@[^:]+:[^\/]+?\/).*?.git$', url
        ) else False
    return result


def check_arg(info_dict: Dict, expr_list: List, empty_arg: List) -> Tuple:
    """Check whether the parameters are correct.

    :param expr_list(List): List of parameters to check.
    :param info_dict(Dict): Information about whether the parameter being checked is correct.
    :param Empty_arg(List): Optional parameter list.

    :return Tuple(bool, Any): If there is no error, return (True, ""), otherwise False and an error message is returned.
    """
    flag = False
    not_exist = []
    for i in info_dict.keys():
        if i not in info_dict and i not in empty_arg:
            not_exist.append(i)
            flag = True
    if flag:
        return (False, "Please confirm whether the following parameters are correct: " + ",".join(not_exist))

    for _ in expr_list:
        if _ not in info_dict:
            return (False, f"{' '.join(expr_list)} are all required parameter")
    for k, v in info_dict.items():
        if v.strip() == "":
            if k not in empty_arg:
                return (False, f"The parameter {k}'value cannot be empty")
    return (True, "")
