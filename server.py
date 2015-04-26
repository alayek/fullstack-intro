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
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
  edit_item = session.query(MenuItem).filter_by(id=menu_id).one()
  if request.method == 'POST':
    if request.form['name']:
      edit_item.name = request.form['name']
      session.add(edit_item)
      session.commit()
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    return render_template('edit_menu.html', restaurant_id=restaurant_id, menu_id=menu_id, item=edit_item)

#Task 3: Create a route for delete_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
  delete_item = session.query(MenuItem).filter_by(id=menu_id).one()

  if request.method == 'POST':
    if delete_item:
      session.delete(delete_item)
      session.commit()
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    return render_template('delete_menu.html', restaurant_id=restaurant_id, menu_id=menu_id, item=delete_item)
  
  
if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)