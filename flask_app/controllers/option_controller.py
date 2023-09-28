from flask_app import app
from flask import render_template, session, request, redirect, flash
from flask_app.models.option_model import Option
from flask_app.models.admin_model import Admin
from werkzeug.utils import secure_filename
import uuid as uuid
import os

UPLOAD_FOLDER = "flask_app/static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.split(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# DISPLAY : Option Create GET
@app.route("/lincolnstcafe/admin/option/create/get")
def admin_option_create_get():
    id = {
        "id" : session["admin_id"]
    }
    curr_admin = Admin.read_one(id)
    return render_template("AdminOptionCreate.html", curr_admin = curr_admin)

# ACTION : Option Create POST
@app.route("/lincolnstcafe/admin/option/create/post", methods = ["POST"])
def admin_option_create_post():
    file = request.files["image"]

    if "admin_id" not in session:
        flash("Please log in to create a new menu option.", "session_expired")
        return redirect("/lincolnstcafe/admin/login/registration")
    elif not Option.validate_create(request.form):
        id = {
            "id" : session["admin_id"]
        }
        curr_admin = Admin.read_one(id)
        return render_template("AdminOptionCreate.html", curr_admin = curr_admin)
    elif not file:
        flash("File cannot be empty.", "err_image")
        id = {
            "id" : session["admin_id"]
        }
        curr_admin = Admin.read_one(id)
        return render_template("AdminOptionCreate.html", curr_admin = curr_admin)
    elif not allowed_file(file.filename):
        flash("Invalid file type.", "err_file_type")
        id = {
            "id" : session["admin_id"]
        }
        curr_admin = Admin.read_one(id)
        return render_template("AdminOptionCreate.html", curr_admin = curr_admin)
    else:
        file_filename = secure_filename(file.filename)
        file_name = str(uuid.uuid1()) + "-" + file_filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))

        price = request.form["price"]
        final_price = float(price)

        data = {
            **request.form,
            "image" : file_name,
            "price" : final_price
        }
        Option.create(data)
        category = data["category"]
        flash("Option creation successful!", "upload_success")
        return redirect(f"/lincolnstcafe/admin/{category}")

# DISPLAY : Option Update GET
@app.route("/lincolnstcafe/admin/option/update/get/<int:id>")
def admin_option_update_get(id):
    option_id = {
        "id" : id
    }
    curr_option = Option.read_one(option_id)
    id = {
        "id" : session["admin_id"]
    }
    curr_admin = Admin.read_one(id)
    return render_template("AdminOptionUpdate.html", curr_option = curr_option, curr_admin = curr_admin)

# DISPLAY : Option Update POST
@app.route("/lincolnstcafe/admin/option/update/post/<int:id>", methods=["POST"])
def admin_option_update_post(id):
    if not Option.validate_create(request.form):
        option_id = {
        "id" : id
        }
        curr_option = Option.read_one(option_id)
        id = {
        "id" : session["admin_id"]
        }
        curr_admin = Admin.read_one(id)
        return render_template("AdminOptionUpdate.html", curr_option = curr_option, curr_admin = curr_admin)
    
    file = request.files["image"]
    if not file:
        flash("File cannot be empty.", "err_image")
        option_id = {
        "id" : id
        }
        curr_option = Option.read_one(option_id)
        id = {
        "id" : session["admin_id"]
        }
        curr_admin = Admin.read_one(id)
        return render_template("AdminOptionUpdate.html", curr_option = curr_option, curr_admin = curr_admin)
    if file and allowed_file(file.filename):
        file_filename = secure_filename(file.filename)
        file_name = str(uuid.uuid1()) + "-" + file_filename
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))

    price = request.form["price"]
    final_price = float(price)

    data = {
        **request.form,
        "image" : file_name,
        "price" : final_price
    }
    Option.update(data)
    category = data["category"]
    return redirect(f"/lincolnstcafe/admin/{category}")

# ACTION : Option Delete
@app.route("/lincolnstcafe/admin/option/delete/<int:id>")
def admin_option_delete(id):
    if "admin_id" not in session:
        return redirect("/lincolnstcafe/admin/login/registration")
    id_dict = {
        "id" : id
    }
    Option.delete(id_dict)
    return redirect("/lincolnstcafe/admin/pizza")