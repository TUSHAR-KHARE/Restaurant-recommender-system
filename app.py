from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app and tell it to find templates in current folder
app = Flask(__name__, template_folder='.')
CORS(app, resources={r"/*": {"origins": "*"}})

# ML model loading
try:
    from model import get_prediction, get_localities, get_cuisines, get_cuisines_for_locality
    MODEL_AVAILABLE = True
    logger.info("✅ ML Model loaded successfully")
except Exception as e:
    MODEL_AVAILABLE = False
    logger.error(f"❌ Failed to load ML model: {e}")
    logger.info("🔄 Server will use fallback predictions")

def get_fallback_prediction(locality, cuisine):
    """Fallback prediction when ML model is not available"""
    cuisine_ratings = {
        'north indian': 4.2, 'south indian': 4.2, 'chinese': 4.1,
        'italian': 4.1, 'fast food': 3.8, 'street food': 4.3,
        'desserts': 4.0, 'cafe': 3.9, 'pizza': 4.0, 'burger': 3.9
    }

    predicted_rating = cuisine_ratings.get(cuisine.lower(), 4.0)

    return {
        'status': 'success',
        'locality': locality.title(),
        'cuisine': cuisine.title(),
        'predicted_rating': predicted_rating,
        'restaurants': [
            {
                'name': f'Top {cuisine.title()} Restaurant',
                'rating': round(predicted_rating + 0.3, 1),
                'address': f'{locality.title()}, Indore',
                'cuisine': cuisine.title(),
                'cost_for_two': 500
            },
            {
                'name': f'Popular {cuisine.title()} Place',
                'rating': round(predicted_rating + 0.1, 1),
                'address': f'{locality.title()}, Indore',
                'cuisine': cuisine.title(),
                'cost_for_two': 400
            }
        ],
        'model_used': False
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided', 'status': 'error'}), 400

        locality = data.get('locality', '').strip()
        cuisine = data.get('cuisine', '').strip()

        if not locality or not cuisine:
            return jsonify({'error': 'Locality and cuisine are required', 'status': 'error'}), 400

        logger.info(f"🔍 Prediction request: {locality} + {cuisine}")

        if MODEL_AVAILABLE:
            try:
                prediction_result = get_prediction(locality, cuisine)
                logger.info("✅ ML Model prediction successful")
                return jsonify(prediction_result)
            except Exception as e:
                logger.error(f"❌ ML Model failed: {e}")
                logger.info("🔄 Using fallback prediction")

        prediction_result = get_fallback_prediction(locality, cuisine)
        logger.info("✅ Fallback prediction successful")
        return jsonify(prediction_result)

    except Exception as e:
        logger.error(f"❌ Prediction endpoint error: {e}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/localities', methods=['GET'])
def localities():
    try:
        if MODEL_AVAILABLE:
            localities_list = get_localities()
        else:
            localities_list = [
                "Vijay Nagar", "Old Palasia", "New Palasia", "Sapna Sangeeta",
                "Bhawar Kuan", "Rajendra Nagar", "Sudama Nagar", "Geeta Bhawan"
            ]

        return jsonify({'status': 'success', 'localities': localities_list})
    except Exception as e:
        logger.error(f"❌ Localities endpoint error: {e}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/cuisines', methods=['GET'])
def cuisines():
    try:
        if MODEL_AVAILABLE:
            cuisines_list = get_cuisines()
        else:
            cuisines_list = [
                "North Indian", "South Indian", "Chinese", "Italian",
                "Fast Food", "Street Food", "Desserts", "Cafe"
            ]

        return jsonify({'status': 'success', 'cuisines': cuisines_list})
    except Exception as e:
        logger.error(f"❌ Cuisines endpoint error: {e}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/cuisines/<locality>', methods=['GET'])
def cuisines_by_locality(locality):
    try:
        if MODEL_AVAILABLE:
            cuisines_list = get_cuisines_for_locality(locality)
        else:
            cuisines_list = [
                "North Indian", "South Indian", "Chinese", "Italian",
                "Fast Food", "Street Food"
            ]

        return jsonify({'status': 'success', 'locality': locality, 'cuisines': cuisines_list})
    except Exception as e:
        logger.error(f"❌ Cuisines by locality endpoint error: {e}")
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'model_available': MODEL_AVAILABLE, 'message': 'Server is running'})

if __name__ == '__main__':
    logger.info("🚀 Starting Flask server...")
    logger.info(f"📊 Model Status: {'✅ Available' if MODEL_AVAILABLE else '❌ Using Fallback'}")
    app.run(debug=False, host='127.0.0.1', port=5000)
