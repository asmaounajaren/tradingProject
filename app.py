from flask import Flask, render_template, request, jsonify
from register import reg
import os
import pickle
from model import cluster_stocks,visualize_clusters,analyze_cluster_pairs

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
        plot_img=visualize_clusters(selected_sector)
        pair_options = analyze_cluster_pairs(selected_sector, 1, 0.1, 0.1)
        print("ALl pairs")
        print(pair_options)

        response = {
            'clusters': clusters,
            'plot_img': plot_img,
            'options': pair_options
        }
        return jsonify(response)
    else:
        selected_sector = 'Energy'
        clusters = cluster_stocks(selected_sector)
        plot_img=visualize_clusters(selected_sector)
        print(plot_img)
        return render_template('index.html', sectors=sectors, clusters=clusters,plot_img=plot_img)

# print(cluster_stocks('Real_Estate'))
@app.route("/optimisation")
def about_page():
    return render_template("optimisation.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
