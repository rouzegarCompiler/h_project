from flask import render_template, request, jsonify
from app import app

from mod_admin.models import Product,DiscountCode

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/list_products")
def list_products():
    products = Product.query.all()
    return render_template("list_products.html", products = products)

@app.route("/rules")
def rules():
    return render_template("rules.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


"""
    To check discount code in front side
"""
@app.route("/check_discount_code")
def check_discount_code():
    discount_code = request.args.get("discount_code")
    product_id = request.args.get("product_id",0)

    found_discount_code = DiscountCode.query.filter_by(code = discount_code).first()
    found_product = Product.query.filter_by(id = product_id).first()

    if found_discount_code and found_product:
        context = {
            "status": "valid",
            "price" : found_product.cost,
            "discount_value" : found_discount_code.value
        }
        return jsonify(context)

    context = {
        "status": "invalid",
        "price" : 0,
        "discount_value" : 0
    }
    return jsonify(context)