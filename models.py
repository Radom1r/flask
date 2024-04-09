import os
import datetime
import atexit
from sqlalchemy import create_engine, Integer, ForeignKey, String, func, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship, mapped_column, Mapped

POSTRGES_PASSWORD = os.getenv('POSTRGES_PASSWORD', 'secret')
POSTRGES_USER = os.getenv('POSTRGES_USER', 'app')
POSTRGES_DB = os.getenv('POSTRGES_DB', 'app')
POSTRGES_HOST = os.getenv('POSTRGES_HOST', '127.0.0.1')
POSTRGES_PORT = os.getenv('POSTRGES_PORT', '5432')

# PG_DSN = f'postrgesql://{POSTRGES_USER}:{POSTRGES_PASSWORD}@{POSTRGES_HOST}:{POSTRGES_PORT}/{POSTRGES_DB}'
PG_DSN = 'postgresql://appadmin:jdfh8jhtghnjkfrvhyu@localhost:5432/SQL_5'


engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    Adv = relationship('Adv', backref='User')

class Adv(Base):
    __tablename__ = 'Adv'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    user: Mapped[int] = mapped_column(Integer, ForeignKey('User.id'))

Base.metadata.create_all(bind=engine)
atexit.register(engine.dispose)