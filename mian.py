# -*- coding: utf-8 -*-
# @Time    : 2024/10/28 16:03
# @Author  : tangjie.zheng
# @File    : mian.py
# @Software: PyCharm2024

import cx_Oracle
from cx_Oracle import Cursor

import sql_generator
import datetime
import json



# 读取配置文件
def load_config(config_file: str) -> dict:
    with open(config_file, 'r') as file:
        config = json.load(file)

    # 解析日期范围
    config["date_range"] = (
        datetime.datetime.strptime(config["date_range"][0], "%Y-%m-%d").date(),
        datetime.datetime.strptime(config["date_range"][1], "%Y-%m-%d").date()
    )
    return config

# 主函数
# dsn: str, user: str, password: str, schema_name : str , table_name: str, num_rows: int, varchar_range: Tuple[int, int],
#          date_range: Tuple[datetime.date, datetime.date], clob_range: tuple
def main(config_file: str):

    # 读取配置文件
    config = load_config(config_file)
    db_config = config["database"]

    # 建立数据库连接
    connection = cx_Oracle.connect(user=db_config["user"], password=db_config["password"], dsn=db_config["dsn"])
    cursor = connection.cursor()

    # 获取表结构
    # [('col1', 'NUMBER', 22), ('col2', 'VARCHAR2', 100) ,('col3', 'VARCHAR2', 32)]
    columns = sql_generator.get_table_columns(connection, config["schema"], config["table"])
    print("表结构:" )
    print( columns)
    # 表结构参考
    # [('COLUMN_NAME111', 'NUMBER', 22), ('A', 'VARCHAR2', 100), ('column=name', 'NUMBER', 22), ('C', 'TIMESTAMP(6)', 11), ('ID', 'NUMBER', 22), ('NAME', 'VARCHAR2', 32)]


    pk_counter = config["pk_start"]
    # 生成执行插入语句
    for _ in range(config["num_rows"]):
        stmt, pk_counter = sql_generator.generate_insert_statement(config, columns, pk_counter)
        #insert_statements.append(stmt)
        print(stmt)
        cursor.execute(stmt)
        connection.commit()

    cursor.close()
    connection.close()

# 使用示例
if __name__ == "__main__":

    main("config.json")
