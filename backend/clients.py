import os
from sqlalchemy import create_engine, engine

db_user = os.getenv('DB_USER')
db_pswd = os.getenv('DB_PSWD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
address = f"mysql+pymysql://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}"

create_table_sql = '''
    CREATE TABLE post (
        url VARVHAR(50) PRIMARY KEY,
        author VARVHAR(50),
        pushes LONGTEXT,
        status INT
    )
'''

def get_mysql_connect() -> engine.base.Connection:
    engine = create_engine(address)
    connect = engine.connect()
    return connect

    
