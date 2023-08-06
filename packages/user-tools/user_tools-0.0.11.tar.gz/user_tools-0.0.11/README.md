# user_tools

Some personally used modules.

> Some modules may be other people's source code, because this tool is mainly convenient for personal use, so there is no processing.
> If you think it is infringing, please contact me by email or GitHub to delete.
> If I know the source of the code, I will explain it.

# install

`pip install user_tools`

# module description

- `util_check.py` : Some checks on files or directories.
- `util_cmd.py` : Some functions related to command execution.
- `util_file.py` : Some functions related to file operations.
- `util_hashlib.py` : Some functions related to hash operations.
- `util_img.py` : Some functions related to image operations.
- `util_json.py` : Some functions related to json file operations.
- `util_random.py` : Custom random function.
- `util_str.py` : Custom str function.
- `util_time.py` : Some functions related to json time operations.
- `util_ua.py` : Some functions related to useragent.

# changelog

- 2020/03/09 : Initial completion of script writing.
- 2020/04/15 ：Update the docstring to add a description of the parameters. util_check.is_not_null() method adds monitoring of the directory. The util_check.check_url() method was added, but the git address detection is not yet complete because it is not familiar with the regularity.
- 2020/04/18 : Fix some bug.
- 2020/07/18 : Added typing for each file, added util_mysql.py and pyzabbix.py.
- 2021/02/17 : Removed some file, added util_str.py and changed some file.
- 2021/02/25 : Fix the bug in util_str.format_str().
- 2021/07/12 : Fix the bug in util_check.check_arg().