from sqlalchemy import Table,Column,Integer,String
from database.database import meta


Weekly = Table(
    'weekly',meta,
    Column("id",Integer,primary_key=True),
    Column("min",String(32)),
    Column("max",String(32)),
    Column("avarage_price",String(32)),
    Column("total_volume",String(32)),
    Column("last_price",String(32)),
    Column("datetime",String(32)),

)
