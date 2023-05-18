from flask import Flask, render_template
from register import reg
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.register_blueprint(reg)
@app.route('/')
def index():  # put application's code here
    return render_template("index.html")

@app.route("/optimisation")
def about_page():
    return render_template("optimisation.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
