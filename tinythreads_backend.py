# TinyThreads Store - Flask REST API with SQLite
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tinythreads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------------- Models --------------------------- #
class Product(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(250))
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200))

class CartItem(db.Model):
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    product_id = db.Column(db.String, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product')

class Order(db.Model):
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    total = db.Column(db.Float, nullable=False)

class OrderItem(db.Model):
    id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.String, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.String, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product')

# --------------------------- Routes --------------------------- #
@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'desc': p.desc,
        'price': p.price,
        'image': p.image
    } for p in products]), 200

@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    new_product = Product(
        id=str(uuid4()),
        name=data.get("name"),
        desc=data.get("desc"),
        price=data.get("price"),
        image=data.get("image")
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added."}), 201

@app.route("/products/<product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        abort(404)
    data = request.get_json()
    product.name = data.get("name", product.name)
    product.desc = data.get("desc", product.desc)
    product.price = data.get("price", product.price)
    product.image = data.get("image", product.image)
    db.session.commit()
    return jsonify({"message": "Product updated."}), 200

@app.route("/products/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    return '', 204

@app.route("/cart/<user_id>", methods=["GET"])
def view_cart(user_id):
    items = CartItem.query.filter_by(user_id=user_id).all()
    cart = [{
        'id': item.id,
        'product': {
            'id': item.product.id,
            'name': item.product.name,
            'price': item.product.price
        }
    } for item in items]
    return jsonify(cart), 200

@app.route("/cart/<user_id>", methods=["POST"])
def add_to_cart(user_id):
    data = request.get_json()
    product = Product.query.get(data.get("product_id"))
    if not product:
        abort(404)
    cart_item = CartItem(id=str(uuid4()), user_id=user_id, product_id=product.id)
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({"message": "Product added to cart."}), 200

@app.route("/cart/<user_id>/<product_id>", methods=["DELETE"])
def remove_from_cart(user_id, product_id):
    item = CartItem.query.filter_by(user_id=user_id, product_id=product_id).first()
    if not item:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Product removed from cart."}), 200

@app.route("/order/<user_id>", methods=["POST"])
def place_order(user_id):
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty."}), 400
    total = sum(item.product.price for item in cart_items)
    order = Order(id=str(uuid4()), user_id=user_id, total=total)
    db.session.add(order)
    for item in cart_items:
        order_item = OrderItem(id=str(uuid4()), order_id=order.id, product_id=item.product.id)
        db.session.add(order_item)
        db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Order placed."}), 201

@app.route("/orders", methods=["GET"])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': o.id,
        'user_id': o.user_id,
        'total': o.total
    } for o in orders]), 200

# --------------------------- Run App --------------------------- #
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, threaded=False, use_reloader=True)
