from sqlalchemy import Table,Column,Integer,String
from database.database import meta

Users = Table(
    'users',meta,
    Column("id",Integer,primary_key=True),
    Column("name_surname",String(32)),
    Column("mail",String(32)),
    Column("password",String(32))
)
