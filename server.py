from flask import Flask
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
def restaurantMenu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
  output = ''
  for item in items:
    output += item.name
    output += '</br>'
    output += item.price
    output += '</br>'
    output += item.description
    output +='</br>'
    output +='</br>'
  return output
  
#Task 1: Create route for new_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/new/')
def new_menu_item(restaurant_id):
  return "page to create a new menu item. Task 1 complete!"
  
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