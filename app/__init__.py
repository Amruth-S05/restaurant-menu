from flask import Flask, redirect, render_template, request, url_for

import logging

from .db import Restaurant, Base, Menu

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker


app = Flask(__name__)

url_object = URL.create(
	"postgresql+pg8000",
	username="amruth",
	password="amruth",
	host="localhost",
	database="restaurant_app",
	)
engine = create_engine(url_object)
session = sessionmaker(bind=engine)()


@app.route("/")
def index():
	restaurant_list = session.query(Restaurant).all()
	home_link = url_for("index")
	
	return render_template("index.html", restaurant_list=restaurant_list, home_link=home_link)


@app.route("/restaurant/<int:restaurant_id_from_user>")
def restaurant(restaurant_id_from_user):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id_from_user).one()
	menu_list = session.query(Menu).filter_by(restaurant_id=restaurant_id_from_user).all()

	return render_template("restaurant.html", restaurant=restaurant, menu_list=menu_list)


@app.route("/delete/<int:menu_id>")
def delete(menu_id):
	menu_item = session.query(Menu).filter_by(id=menu_id).one()
	restaurant = session.query(Restaurant).filter_by(id=menu_item.restaurant_id).one()
	session.delete(menu_item)
	# session.commit()
	# this brings permanent changes in the database data

	return redirect(f"/restaurant/{restaurant.id}")


@app.route("/edit/<int:menu_id>", methods=["GET", "POST"])
def edit(menu_id):
	menu_item = session.query(Menu).filter_by(id=menu_id).one()
	if request.method == "POST":
		new_price = request.form['menu-price']
		new_description = request.form['menu-description']

		menu_item.price = new_price
		menu_item.description = new_description
		app.logger.info(new_price, new_description)

		# session.commit()
		return redirect(url_for("restaurant", restaurant_id_from_user=menu_item.restaurant_id))

	return render_template("edit.html", menu_name=menu_item.name)


@app.route("/favicon.ico", methods=["GET"])
def favicon():
	return ""


if __name__ == "__main__":
	app.run()