from sqlalchemy import Table,Column,Integer,String
from database.database import meta


Daily = Table(
    'daily',meta,
    Column("id",Integer,primary_key=True),
    Column("min",String(32)),
    Column("max",String(32)),
    Column("avarage_price",String(32)),
    Column("total_volume",String(32)),
    Column("last_price",String(32)),
    Column("datetime",String(32)),

)

#val=(r.data.camera,r.data.device_ip,str(r.data.frame_uuid),"bugun",
#str(savePath),str(savePath),r2.events.coordinates,r2.events.payload)