from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship, backref

Base = declarative_base()


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    login = Column(String(50))
    password = Column(String(255))
    website = Column(String(50))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', backref=backref('categories', uselist=False))
