from sqlalchemy import create_engine
import mysql.connector  # MySQL连接信息

db_config = {
    "user": "root",
    "password": "123456",
    "host": "47.103.135.146",  # 或者你的服务器IP地址
    "database": "trade",

}

# 创建MySQL连接引擎
engine = create_engine('mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(
    **db_config))

connection = mysql.connector.connect(
    user='root',
    password='123456',
    host='47.103.135.146',  # 或者你的服务器IP地址
    database='trade'
)

# 创建游标对象
cursor = connection.cursor()
