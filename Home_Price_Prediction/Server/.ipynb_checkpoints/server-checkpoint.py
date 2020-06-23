from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
import util

app = Flask(__name__)
app.config['SERVER_NAME'] = "localhost:5000" # attempting to set explicitly, as it defaults to None 

@app.route('/')
def home():
    return "home..."

@app.route('/api', methods=['GET'])
def index():
    return "Hello, World!"

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    print('server name ', app.config["SERVER_NAME"])
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    
#     app.run(debug=True)