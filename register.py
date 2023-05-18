from flask import Blueprint, render_template
reg = Blueprint('register', __name__)

@reg.route("/register")
def register_page():
    return render_template("register.html")
