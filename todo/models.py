from sqlalchemy import Column, Integer, String, Boolean

from todo.database import Base


class Todos(Base):
    __table_name__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
