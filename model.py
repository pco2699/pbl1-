import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base

class TT_Location(object):
    pass

class TT_Report(object):
    pass


url = "sqlite:///data.sqlite3"
engine = create_engine(url, echo=False)
Base = declarative_base(engine)

tables = {name: sqlalchemy.Table(name, Base.metadata, autoload=True,
                                 autoload_with=engine)
          for name in engine.table_names()}
mapper(TT_Location, tables["location"])
mapper(TT_Report, tables["report"])