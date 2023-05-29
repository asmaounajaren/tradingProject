from flask import Flask, render_template, request, jsonify, session
from register import reg
import os
import pickle
from model import cluster_stocks,visualize_clusters,analyze_cluster_pairs,plot_and_simulate_trading,calculate_performance,z_score_spread,plot_performance

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
        selectedSector = request.form.get('selectedSector')
        clusterNum = request.form.get('cluster')
        print("cluster")
        print("cluser numero: ",clusterNum )
        print("secteur: ",selectedSector)
        trade,zscore_image = plot_and_simulate_trading(pairs, selectedSector, clusterNum,1,-1,10000)
        print("before")
        trade_history = trade.to_html()
        print(trade_history)
        # zscore_image='/Z-score_Spread_and_Trading_Signals_for_'+pairs[0]+'_and_'+pairs[1]+'_in_'+selectedSector+'_Sector,_Cluster_'+clusterNum+'.png';
        response ={
            'trade_history': trade_history,
            'zscore_image': zscore_image
        }
        return jsonify(response)

    else:
        return render_template('index.html')

@app.route("/statistics", methods=['GET','POST'])
def statistics():
    if request.method == 'POST':
        selected_pairs = request.form.get('selectedPair')
        selectedSector = request.form.get('selectedSector')
        print('pair statistics', selected_pairs)
        tuple_pairs = tuple(selected_pairs.split(','))
        pairs = tuple(item.strip() for item in tuple_pairs)
        dataa, final_cash, total_return, annualized_return, volatility, sharpe_ratio, max_drawdown, num_trades, win_rate=calculate_performance(z_score_spread,pairs[0],pairs[1],selectedSector,-1,1,10000,0.3)
        print(dataa, 'finalcash',final_cash,'total_return', total_return,'annualized_return', annualized_return, 'volatility',volatility, 'sharpe_ratio',sharpe_ratio,'max_drawdown', max_drawdown,'num_trades', num_trades,'win_rate', win_rate)
        statisticimage=plot_performance(dataa,total_return,annualized_return,volatility,sharpe_ratio,max_drawdown,num_trades,win_rate,selectedSector,pairs[0],pairs[1])
        print("statistic image")
        print(statisticimage)
        response = {
            "dataa": dataa.to_html(),
            "final_cash": round(final_cash, 2),
            "total_return": round(total_return,2),
            "annualized_return": round(annualized_return,2),
            "volatility": round(volatility,2),
            "sharpe_ratio": round(sharpe_ratio,2),
            "max_drawdown": round(max_drawdown,2),
            "num_trades": round(num_trades,2),
            "win_rate": round(win_rate,2),
            "statisticimage": statisticimage
        }
        return jsonify(response)
@app.route("/optimisation")
def about_page():
    return render_template("optimisation.html")
@app.route("/historique")
def historique():
    if request.method == 'POST':
        return render_template("historique.html")
    else:
        return render_template("historique.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)
