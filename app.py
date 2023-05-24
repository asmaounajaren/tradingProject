from flask import Flask, render_template, request, jsonify
from register import reg
import os
import pickle
from model import cluster_stocks,visualize_clusters

app = Flask(__name__)
app.secret_key = os.urandom(32)

app.register_blueprint(reg)
# model = pickle.load(open('model.pkl', 'rb'))

sectors = [
    'Energy',
    'Communication_Services',
    'Financials',
    'Health_Care',
    'Industrials',
    'Information_Technology',
    'Real_Estate'

]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_sector = request.form.get('sector')
        clusters = cluster_stocks(selected_sector)
        image = visualize_clusters(selected_sector)
        image.save(os.path.join('static', 'img', 'image.png'))
        # Get the absolute path of the "static" directory
        static_dir = os.path.abspath(os.path.join(os.getcwd(), 'static'))

        # Specify the file path using the absolute path
        image_path = os.path.join(static_dir, 'img', image)

        # Save the image
        image.save(image_path)
        return jsonify(clusters,image)
    else:
        selected_sector = 'Financials'
        clusters = cluster_stocks(selected_sector)
        return render_template('index.html', sectors=sectors, clusters=clusters)

# print(cluster_stocks('Real_Estate'))
@app.route("/optimisation")
def about_page():
    return render_template("optimisation.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
