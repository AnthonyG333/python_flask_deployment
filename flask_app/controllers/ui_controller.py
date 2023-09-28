from flask_app import app, mail
from flask_mail import Message
from flask import render_template, request, redirect, session, flash
from flask_app.models.option_model import Option

# DISPLAY : Dashboard
@app.route("/lincolnstcafe")
def home():
    if "cart" not in session:
        session["cart_length"] = 0
    return render_template("Home.html")

# DISPLAY : Options By Category
@app.route("/lincolnstcafe/<string:category>")
def option_category(category):
    if "cart" not in session:
        session["cart_length"] = 0
    category_dict = {
        "category" : category
    }
    all_options = Option.read_all_by_category(category_dict)
    return render_template("OptionsByCategory.html", all_options = all_options)

# DISPLAY : CART VIEW
@app.route("/lincolnstcafe/cart/view")
def cart_view():
    return render_template("Cart.html")

# ACTION : ADD TO CART
@app.route("/lincolnstcafe/cart/add", methods = ['POST'])
def cart_add():
    if not request.form["quantity"] or int(request.form["quantity"]) == 0:
        id = {
            "id" : request.form["id"]
        } 
        option = Option.read_one(id)
        category_dict = {
            "category" : option.category
        }
        all_options = Option.read_all_by_category(category_dict)
        flash("Unable to add to cart. Quantity must be at least 1.", "err_quantity")
        return render_template("OptionsByCategory.html", all_options = all_options)
    id = {
        "id" : request.form["id"]
    }
    option = Option.read_one(id)
    category = option.category
    option_dict = {
        "id" : option.id,
        "image" : option.image,
        "name" : option.name,
        "price_per_unit" : int(option.price),
        "quantity" : int(request.form["quantity"])
    }
    session["cart_length"] += option_dict["quantity"]
    if option_dict["quantity"] >= 2:
        total_price = option_dict["quantity"] * option_dict["price_per_unit"]
        option_dict["total_price"] = total_price
    else: 
        option_dict["total_price"] = option_dict["price_per_unit"]
    
    if "cart" in session:
        option_exists = False
        for dict in session["cart"]:
            if dict["id"] == option_dict["id"]:
                dict["quantity"] += option_dict["quantity"]
                dict["total_price"] += option_dict["total_price"]
                option_exists = True
        if option_exists == False:
            cart_list = session["cart"]
            cart_list.append(option_dict)
            session["cart"] = cart_list
    if "cart" not in session:
        option_list = []
        option_list.append(option_dict)
        session["cart"] = option_list
        session["cart_length"] = option_dict["quantity"]

    session["subtotal"] = 0
    for dict in session["cart"]:
        session["subtotal"] += dict["total_price"]
    
    return redirect(f"/lincolnstcafe/{category}")

# ACTION : CART INCREMENT
@app.route("/lincolnstcafe/cart/increment/<int:id>")
def cart_increment(id):
    for dict in session["cart"]:
        if dict["id"] == id:
            # QUANTITY 
            new_quantity = dict["quantity"] + 1
            dict["quantity"] = new_quantity
            # TOTAL PRICE
            new_total_price = dict["total_price"] + dict["price_per_unit"]
            dict["total_price"] = new_total_price
            # SUBTOTAL
            session["subtotal"] += dict["price_per_unit"]
            # CART LENGTH
            session["cart_length"] += 1
            session.modified = True
    return redirect("/lincolnstcafe/cart/view")

# ACTION : CART DECREMENT
@app.route("/lincolnstcafe/cart/decrement/<int:id>")
def cart_decrement(id):
    for dict in session["cart"]:
        if dict["id"] == id:
            # QUANTITY 
            new_quantity = dict["quantity"] - 1
            if new_quantity == 0:
                return redirect(f"/lincolnstcafe/cart/remove/{id}")
            dict["quantity"] = new_quantity
            # TOTAL PRICE
            new_total_price = dict["total_price"] - dict["price_per_unit"]
            dict["total_price"] = new_total_price
            # SUBTOTAL
            session["subtotal"] -= dict["price_per_unit"]
            # CART LENGTH
            session["cart_length"] -= 1
            session.modified = True
    return redirect("/lincolnstcafe/cart/view")

# ACTION : CART REMOVE
@app.route("/lincolnstcafe/cart/remove/<int:id>")
def cart_remove(id):
    for dict in session["cart"]:
        if dict["id"] == id:
            # SUBTOTAL
            new_subtotal = session["subtotal"]- dict["total_price"]
            session["subtotal"] = new_subtotal
            # CART LENGTH
            session["cart_length"] -= dict["quantity"]
            # REMOVING OPTION
            index = session["cart"].index(dict)
            session["cart"].pop(index)
            session.modified = True
    return redirect("/lincolnstcafe/cart/view")

# ACTION : CART CLEAR
@app.route("/lincolnstcafe/cart/clear")
def cart_clear():
    session.clear()
    return redirect("/lincolnstcafe/pizza")

# DISPLAY : CART CHECKOUT GET
@app.route("/lincolnstcafe/cart/checkout/get")
def cart_checkout_get():
    return render_template("Checkout.html")

# ACTION : CART CHECKOUT POST
@app.route("/lincolnstcafe/cart/checkout/post", methods = ["POST"])
def cart_checkout_post():
    if not Option.validate_checkout(request.form):
        return render_template("Checkout.html")
    first_name = request.form["first_name"]
    session["first_name"] = first_name
    email = request.form["email"]

    Subject = "Lincoln St. Cafe - Thank You for Your Order!"
    msg = Message( subject = Subject, sender = "lincolnstcafe@outlook.com", recipients = [email])
    msg.html = render_template("Email.html")
    mail.send(msg)

    session.clear()

    return redirect("/lincolnstcafe/cart/success")

# DISPLAY : SUCCESS
@app.route("/lincolnstcafe/cart/success")
def cart_success():
    return render_template("Success.html")
