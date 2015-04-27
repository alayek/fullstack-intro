from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
  menus = [];
  restaurants = session.query(Restaurant).all()
  for restaurant in restaurants:
    menus.append(session.query(MenuItem).filter_by(restaurant_id=restaurant.id).count())
  return render_template('restaurants.html', restaurants=restaurants, menus=menus)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
  count = session.query(Restaurant).count() # get no. of restaurants, for pagination
  items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
  return render_template('menu.html', restaurant=restaurant, items=items, count=count)


# Add route for restaurant editing
@app.route('/restaurants/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def restaurant_edit(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  if request.method == 'POST':
    # edit the restaurant here
    prev_restaurant_name = restaurant.name
    restaurant.name = request.form['name']
    restaurant.description = request.form['description']
    session.add(restaurant)
    session.commit()
    flash("Restaurant %s was successfully edited" % prev_restaurant_name)
    return redirect(url_for('show_restaurants'))
  else:
    return render_template('edit_restaurant.html', restaurant=restaurant)


# Add route for restaurant deleting
@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def restaurant_delete(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  if request.method == 'POST':
    name = restaurant.name
    # first delete the menus from the MenuItem
    menus = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    for menu in menus:
      session.delete(menu)
    # now the restaurant
    session.delete(restaurant)
    session.commit()
    flash("Restaurant %s and all its menus were deleted" % name)
    return redirect(url_for('show_restaurants'))
  else:
    return render_template('delete_restaurant.html', restaurant=restaurant)



#Task 1: Create route for new_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  count = session.query(Restaurant).count()
  if request.method == 'POST':
    new_item = MenuItem(name=request.form['name'], restaurant_id=restaurant_id, price='$' + request.form['price'], description=request.form['description'])
    session.add(new_item)
    session.commit()
    flash("New menu item %s created" % new_item.name)
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    return render_template('new_menu.html', restaurant=restaurant, count=count)
  
#Task 2: Create route for edit_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
  edit_item = session.query(MenuItem).filter_by(id=menu_id).one()
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  count = session.query(Restaurant).count() # get no. of restaurants, for pagination
  if request.method == 'POST':
    if request.form['name']:
      name = edit_item.name # store the previous name
      edit_item.name = request.form['name']
      edit_item.price = '$' + request.form['price']
      edit_item.description = request.form['description']
      session.add(edit_item)
      session.commit()
      flash("Item %s edited" % name)
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    return render_template('edit_menu.html', restaurant=restaurant, menu_id=menu_id, item=edit_item, count=count)

#Task 3: Create a route for delete_menu_item function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
  delete_item = session.query(MenuItem).filter_by(id=menu_id).one()

  if request.method == 'POST':
    if delete_item:
      name = delete_item.name
      session.delete(delete_item)
      session.commit()
      flash("%s deleted from menu" % name)
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    return render_template('delete_menu.html', restaurant_id=restaurant_id, menu_id=menu_id, item=delete_item)

# For JSON API
@app.route('/restaurants/<int:restaurant_id>/menu/json/')
def restaurant_menu_json(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
  return jsonify(MenuItems=[item.serialize for item in items])

# For JSON API specific to menu
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/json/')
def restaurant_menu_item_json(restaurant_id, menu_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  try:
    item = session.query(MenuItem).filter_by(restaurant_id=restaurant_id,id=menu_id).one()
    return jsonify(MenuItem=item.serialize)
  except:
    return "no data found"
  
  
if __name__ == '__main__':
  app.secret_key = 'super secret key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)