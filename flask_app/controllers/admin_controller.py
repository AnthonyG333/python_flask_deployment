from flask_app import app, bcrypt
from flask import render_template, session, request, redirect, flash
from flask_app.models.admin_model import Admin
from flask_app.models.option_model import Option

# DISPLAY : Admin Login & Registration
@app.route("/lincolnstcafe/admin/login/registration")
def admin_login_registration():
    return render_template("AdminLoginRegistration.html")

# ACTION : Admin Create POST
@app.route("/lincolnstcafe/admin/create", methods = ["POST"])
def admin_create():
    if not Admin.validate_registration(request.form):
        return render_template("AdminLoginRegistration.html")
    
    hash_password = bcrypt.generate_password_hash(request.form["password"])
    # ALWAYS pass a dict as the arg when calling a @classmethod in order to prevent SQL injection
    data = {
        **request.form,
        "password" : hash_password
    }
    # the following line calls the @classmethod and passes the dict (request.form) as an arg, while simulataneously 
    id = Admin.create(data)
    session["admin_id"] = id
    return redirect("/lincolnstcafe/admin/pizza")

# ACTION : Admin Login POST
@app.route("/lincolnstcafe/admin/login", methods = ["POST"])
def admin_login():
    if not Admin.validate_login(request.form):
        return render_template("AdminLoginRegistration.html")
    
    data = {
        "email" : request.form["email"]
    }
    admin = Admin.read_one_by_email(data)
    session["admin_id"] = admin.id
    return redirect("/lincolnstcafe/admin/pizza")

# DISPLAY : Admin Dashboard
@app.route("/lincolnstcafe/admin/<string:category>")
def admin_account(category):
    if "admin_id" not in session:
        return redirect("/lincolnstcafe/admin/login/registration")
    id = {
        "id" : session["admin_id"]
    }
    curr_admin = Admin.read_one(id)
    category_data = {
        "category" : category
    }
    all_options = Option.read_all_by_category(category_data)
    return render_template("AdminOptionsByCategory.html", curr_admin = curr_admin, all_options = all_options)

# DISPLAY : Admin Update GET
@app.route("/lincolnstcafe/admin/update/get")
def admin_account_update_get():
    id = {
        "id" : session["admin_id"]
    }
    curr_admin = Admin.read_one(id)
    return render_template("AdminUpdate.html", curr_admin = curr_admin)

# ACTION : Admin Update POST
@app.route("/lincolnstcafe/admin/update/post", methods = ["POST"])
def admin_account_update_post():
    if not Admin.validate_registration(request.form):
        return redirect("AdminUpdate.html")
    hash_password = bcrypt.generate_password_hash(request.form["password"])
    data = {
        **request.form,
        "id" : session["admin_id"],
        "password" : hash_password
    }
    Admin.update(data)
    return redirect("/lincolnstcafe/admin/pizza")

# ACTION : Admin Logout
@app.route("/lincolnstcafe/admin/logout")
def admin_account_logout():
    if "admin_id" not in session:
        return ("/lincolnstcafe/admin/login/registration")
    session.pop("admin_id")
    return redirect("/lincolnstcafe/admin/login/registration")

# ACTION : Admin Delete
@app.route("/lincolnstcafe/admin/delete")
def admin_account_delete():
    if "admin_id" not in session:
        return redirect("/lincolnstcafe/admin/login/registration")
    id = {
        "id" : session["admin_id"]
    }
    Admin.delete(id)
    return redirect("/lincolnstcafe/admin/login/registration")
