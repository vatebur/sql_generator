# -*- coding: utf-8 -*-
# @Time    : 2024/10/29 14:41
# @Author  : tangjie.zheng
# @File    : oracle_conn_test.py
# @Software: PyCharm2024

import platform
import cx_Oracle
print(platform.architecture())
print("Oracle Client Version:", cx_Oracle.clientversion())


