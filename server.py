from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# @app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
  return render_template('menu.html', restaurant=restaurant, items=items)
  
#Task 1: Create route for new_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
  if request.method == 'POST':
    new_item = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
    session.add(new_item)
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    return render_template('new_menu.html', restaurant_id=restaurant_id)
  
#Task 2: Create route for edit_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def edit_menu_item(restaurant_id, menu_id):
  return "page to edit a menu item. Task 2 complete!"
  
#Task 3: Create a route for delete_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
  return "page to delete a menu item. Task 3 complete!"
  
  
if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)