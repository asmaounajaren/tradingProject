from flask import Flask, render_template, request, jsonify, session
from register import reg
import os
import pickle
from model import cluster_stocks,visualize_clusters,analyze_cluster_pairs,plot_and_simulate_trading

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
        selected_sector = request.form.get('selectedSector')
        print("secteur: ")
        print(selected_sector)
        clusters = cluster_stocks(selected_sector)
        plot_img = visualize_clusters(selected_sector)

        # if selected_pair is None or selected_sector is None or selected_cluster is None:
        # trade_history= plot_and_simulate_trading(pair_options[0], 'Industrials',1)
        # else:
        #     trade_history=plot_and_simulate_trading(pair_options[0], selected_sector,selected_cluster,1,-1,10000)

        response = {
            'clusters': clusters,
            'plot_img': plot_img,
        }
        return jsonify(response)
    else:
        selected_sector = 'Energy'
        clusters = cluster_stocks(selected_sector)
        plot_img=visualize_clusters(selected_sector)
        return render_template('index.html', sectors=sectors, clusters=clusters,plot_img=plot_img)

@app.route("/click", methods=['GET','POST'])
def clickButton():
    if request.method == 'POST':
        selected_sector = request.form.get('sector')
        selected_cluster = request.form.get('cluster')
        level_coint = request.form.get('levelCoint')  # Retrieve level_coint value
        mean_revert = request.form.get('meanRevert')  # Retrieve mean_revert value
        # Convert the retrieved values to float if needed
        level_coint = float(level_coint) if level_coint else None
        mean_revert = float(mean_revert) if mean_revert else None
        # Use the retrieved values in your logic
        if level_coint is None and mean_revert is None and selected_cluster is None:
            pair_options = analyze_cluster_pairs(selected_sector, 1, 0.1, 0.1)
            print("All pairs")
            print(pair_options)
        else:
            pair_options = analyze_cluster_pairs(selected_sector, selected_cluster, level_coint, mean_revert)
        response = {
            'options': pair_options
        }
        return jsonify(response)

@app.route("/selectedPair", methods=['GET','POST'])
def selectedPair():
    if request.method=='POST':
        selected_pairs= request.form.get('selectedPair')
        print('aaaaaaaaaaaaaaaaaa',selected_pairs)
        tuple_pairs=tuple(selected_pairs.split(','))
        pairs=tuple(item.strip() for item in tuple_pairs)
        print("pairs without space")
        print(pairs)
        print("tuuple--------->",tuple_pairs )
        selectedSector=request.form.get('selectedSector')
        clusterNum=request.form.get('cluster')
        print("cluster")
        print("cluser numero: ",clusterNum )
        print("secteur: ",selectedSector)
        trade = plot_and_simulate_trading(pairs, selectedSector, clusterNum,1,-1,10000)
        print("before")
        trade_history = trade.to_html()
        print(trade_history)
        response ={
            'trade_history': trade_history
        }
        return jsonify(response)

    else:
        return render_template('index.html')
@app.route("/optimisation")
def about_page():
    return render_template("optimisation.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
