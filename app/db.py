import sys

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, URL
from sqlalchemy.orm import DeclarativeBase, relationship



class Base(DeclarativeBase):
	pass


class Restaurant(Base):
	__tablename__ = "restaurant"

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)


class Menu(Base):
	__tablename__ = "menu"

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey("restaurant.id"))

	restaurant = relationship(Restaurant)


url_object = URL.create(
	"postgresql+pg8000",
	username="amruth",
	password="amruth",
	host="localhost",
	database="restaurant_app",
	)

engine = create_engine(url_object)

Base.metadata.create_all(engine)
