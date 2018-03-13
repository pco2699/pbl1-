from sqlalchemy.orm import sessionmaker
from model import TT_Report, TT_Location, engine
from sqlalchemy.sql import join

Session = sessionmaker(bind=engine)
session = Session()
q = session.query(TT_Location)
for loc in q:
    print("%s %s %s" % (loc.id, loc.location, loc.long))

columns = [TT_Report.img_file, TT_Report.comment, TT_Location.location, TT_Location.long, TT_Location.lat]

q = join(TT_Report, TT_Location, TT_Report.location_id == TT_Location.id).select()
q = q.with_only_columns(columns)

for row in q.execute():
    print(dict(row))
