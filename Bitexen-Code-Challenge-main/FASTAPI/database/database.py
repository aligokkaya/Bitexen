from sqlalchemy import create_engine,MetaData

meta = MetaData()
db_engine = create_engine("mysql+pymysql://hypegena:aZ5xjXf133@hypegenai.com/hypegena_b_challenge")
conn = db_engine.connect()
