from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle CORS (Cross-Origin Resource Sharing)
# Import our restaurant recommender model
from model import get_prediction, get_localities, get_cuisines, get_cuisines_for_locality

app = Flask(__name__)

# Enabling CORS so the frontend can communicate with the backend on different ports
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Step 1: Get data from the frontend (JSON)
        data = request.get_json()  # This will grab the JSON data sent by the frontend
        locality = data['locality']
        cuisine = data['cuisine']

        # Step 2: Perform prediction based on locality and cuisine using our model
        prediction_result = get_prediction(locality, cuisine)

        # Step 3: Return the prediction results as JSON response
        return jsonify(prediction_result)

    except Exception as e:
        # If there's an error, send an error response
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/localities', methods=['GET'])
def localities():
    """Return a list of available localities"""
    try:
        return jsonify({
            'status': 'success',
            'localities': get_localities()
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/cuisines', methods=['GET'])
def cuisines():
    """Return a list of available cuisines"""
    try:
        return jsonify({
            'status': 'success',
            'cuisines': get_cuisines()
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

@app.route('/cuisines/<locality>', methods=['GET'])
def cuisines_by_locality(locality):
    """Return cuisines available for a specific locality"""
    try:
        return jsonify({
            'status': 'success',
            'locality': locality,
            'cuisines': get_cuisines_for_locality(locality)
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 400

if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask app on localhost:5000 by default
