# -*- coding: utf-8 -*-
# @Time    : 2024/10/29 14:04
# @Author  : tangjie.zheng
# @File    : sql_generator.py
# @Software: PyCharm2024

import random
from typing import Tuple, Union, Any

import data_generator





# 连接到Oracle数据库并读取表结构
#NUMBER字段使用 "DATA_PRECISION", "DATA_SCALE"
def get_table_columns(connection, schema_name: str, table_name: str):
    query = f"""
    SELECT column_name, data_type, data_length ,DATA_PRECISION, DATA_SCALE
    FROM all_tab_columns
    WHERE table_name = :table_name and owner= :schema_name
    """
    with connection.cursor() as cursor:
        cursor.execute(query,schema_name=schema_name.upper(), table_name=table_name.upper())
        return cursor.fetchall()


# 生成插入语句
def generate_insert_statement(config: dict, columns: list,pk_counter: int) -> Tuple[str, Union[int, Any]]:
    schema_name = config["schema"]
    table_name = config["table"]
    varchar_range = config["varchar_range"]
    date_range = config["date_range"]
    clob_range = config["clob_range"]
    blob_size = config["blob_size"]
    pk_name = config["pk_name"]


    column_names = ", ".join([f'"{col[0]}"' for col in columns])


    values = []

    for col in columns:
        col_name, col_type, col_length ,number_precision , number_scale = col
        if varchar_range[0] >= col_length-1:
            varchar_range[0] = 0

        if varchar_range[1] > col_length:
            varchar_range[1] = col_length

        if col_name == pk_name:
            value = str(pk_counter)
            pk_counter += 1
        elif col_type == "VARCHAR2":
            value = f"'{data_generator.generate_random_string(varchar_range[0], varchar_range[1])}'"
        elif col_type == "NUMBER":
            # 计算获取整数位数
            digits = number_precision - number_scale
            value = f"'{round(random.uniform(0,10 ** digits), number_scale)}'"
            if digits <= 0:
                value = 'NULL'
                print("不支持改NUMBER 取值范围"+ number_precision + number_scale)

        elif col_type == "DATE":
            value = f"TO_DATE('{data_generator.generate_random_date(date_range[0], date_range[1]).strftime('%Y-%m-%d')}', 'YYYY-MM-DD')"
        elif col_type.startswith("TIMESTAMP"):
            timestamp = data_generator.generate_random_timestamp(date_range[0], date_range[1])
            value = f"TO_TIMESTAMP('{timestamp.strftime('%Y-%m-%d %H:%M:%S')}', 'YYYY-MM-DD HH24:MI:SS')"
        elif col_type == "CHAR":
            value = f"'{data_generator.generate_random_string(col_length, col_length)}'"  # 固定长度字符串
        elif col_type == "FLOAT":
            value = str(data_generator.generate_random_float())
        elif col_type == "BLOB":
            blob = data_generator.generate_random_blob(blob_size)
            value = f"HEXTORAW('{data_generator.blob_to_hex_string(blob)}')"  # 用.HEXTORAW()将字符串转为BLOB
        elif col_type == "CLOB":
            value = f"'{data_generator.generate_random_clob(clob_range[0], clob_range[1])}'"
        else:
            value = "NULL"
            print("待支持的数据类型："+col_type)

        values.append(value)

    values_str = ", ".join(values)
    return f"INSERT INTO \"{schema_name}\".\"{table_name}\" ({column_names}) VALUES ({values_str})", pk_counter