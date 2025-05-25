import pickle
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import KNeighborsRegressor
from functools import lru_cache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RestaurantRecommender:
    def __init__(self):
        """Initialize the Restaurant Recommender with optimized loading."""
        # Initialize variables
        self.model = None
        self.encoder = None
        self.df = None
        self.model_loaded = False
        self.localities = []
        self.cuisines = []

        # Cache for frequent operations
        self._locality_cache = {}
        self._cuisine_cache = {}

        # Load dataset first
        self._load_dataset()

        # Load or train the model
        self._load_or_train_model()

    def _load_dataset(self):
        """Load the Zomato Indore dataset with optimized error handling."""
        try:
            # Define file paths
            base_path = os.path.dirname(__file__)
            excel_path = os.path.join(base_path, 'zomato_indore.xlsx')
            csv_path = os.path.join(base_path, 'zomato_indore.csv')

            # Try loading Excel first (faster if available)
            if os.path.exists(excel_path):
                self.df = pd.read_excel(excel_path)
                logger.info(f"Excel dataset loaded: {len(self.df)} restaurants")
            elif os.path.exists(csv_path):
                # Optimized CSV loading with most common encoding first
                self.df = self._load_csv_with_encoding(csv_path)
            else:
                logger.warning("Dataset file not found. Using fallback data.")
                self._use_fallback_data()
                return

            # Validate and clean data
            self._validate_and_clean_data()

        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            self._use_fallback_data()

    def _load_csv_with_encoding(self, csv_path):
        """Load CSV with optimized encoding detection."""
        encodings = ['latin-1', 'utf-8', 'iso-8859-1', 'cp1252']  # Most common first

        for encoding in encodings:
            try:
                df = pd.read_csv(csv_path, encoding=encoding)
                logger.info(f"CSV dataset loaded with {encoding} encoding: {len(df)} restaurants")
                return df
            except UnicodeDecodeError:
                continue

        raise Exception("Could not read CSV with any supported encoding")

    def _validate_and_clean_data(self):
        """Validate and clean the loaded dataset."""
        if self.df is None:
            raise Exception("No dataset loaded")

        logger.info(f"Dataset columns: {self.df.columns.tolist()}")

        # Check required columns
        required_columns = ['Locality', 'Cuisines', 'aggregate_rating', 'avg_cost_for_two']
        missing_columns = [col for col in required_columns if col not in self.df.columns]

        if missing_columns:
            logger.warning(f"Missing columns: {missing_columns}. Using fallback data.")
            self._use_fallback_data()
            return

        # Clean data
        self.df = self.df.dropna(subset=['Locality', 'Cuisines', 'aggregate_rating'])

        # Extract unique values with caching
        self.localities = sorted(self.df['Locality'].unique().tolist())
        self.cuisines = sorted(self.df['Cuisines'].unique().tolist())

        logger.info(f"Found {len(self.localities)} localities and {len(self.cuisines)} cuisines")

    def _load_or_train_model(self):
        """Load existing model or train a new one."""
        model_path = os.path.join(os.path.dirname(__file__), 'restaurant_recommender.pkl')

        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)

            self.model = model_data.get('model')
            self.encoder = model_data.get('encoder')

            if self.model and self.encoder:
                logger.info(f"Model loaded successfully from {model_path}")
                self.model_loaded = True
            else:
                raise Exception("Invalid model data")

        except Exception as e:
            logger.warning(f"Error loading model: {e}")
            logger.info("Training new model...")
            self._train_model()

    def _use_fallback_data(self):
        """Use optimized fallback data if dataset is not available."""
        self.df = None

        # Optimized fallback data - most common localities and cuisines in Indore
        self.localities = [
            "Vijay Nagar", "Old Palasia", "New Palasia", "Sapna Sangeeta",
            "Bhawar Kuan", "Rajendra Nagar", "Sudama Nagar", "Geeta Bhawan",
            "Annapurna", "LIG Colony", "MG Road", "AB Road", "Scheme 54",
            "Scheme 78", "Rau", "Khandwa Road", "Saket", "Bombay Hospital"
        ]

        self.cuisines = [
            "North Indian", "South Indian", "Chinese", "Italian",
            "Fast Food", "Street Food", "Mughlai", "Continental",
            "Desserts", "Beverages", "Bakery", "Mithai", "Cafe",
            "Pizza", "Burger", "Biryani", "Thali", "Veg", "Non-Veg"
        ]

    def _train_model(self):
        """Train the machine learning model with optimized parameters."""
        if self.df is None:
            logger.warning("No dataset available for training")
            self.model_loaded = False
            return

        try:
            # Prepare features and target with validation
            required_columns = ['Locality', 'Cuisines', 'avg_cost_for_two', 'aggregate_rating']
            if not all(col in self.df.columns for col in required_columns):
                raise Exception(f"Missing required columns: {required_columns}")

            # Clean data more efficiently
            clean_df = self.df[required_columns].dropna()

            if len(clean_df) < 10:  # Minimum data requirement
                raise Exception("Insufficient data for training")

            features = clean_df[['Locality', 'Cuisines', 'avg_cost_for_two']].copy()
            target = clean_df['aggregate_rating']

            # Optimized one-hot encoding
            self.encoder = OneHotEncoder(
                sparse_output=False,
                handle_unknown='ignore',
                drop='if_binary'  # Optimize for binary features
            )
            categorical_features = self.encoder.fit_transform(features[['Locality', 'Cuisines']])

            # Combine features efficiently
            X = np.column_stack([categorical_features, features['avg_cost_for_two'].values])
            y = target.values

            # Optimized model with better parameters
            self.model = KNeighborsRegressor(
                n_neighbors=min(7, len(clean_df) // 10),  # Adaptive neighbors
                weights='distance',  # Distance-based weighting
                algorithm='auto'  # Let sklearn choose best algorithm
            )
            self.model.fit(X, y)

            # Save model efficiently
            self._save_model()
            self.model_loaded = True
            logger.info("Model trained and saved successfully!")

        except Exception as e:
            logger.error(f"Error training model: {e}")
            self.model_loaded = False

    def _save_model(self):
        """Save the trained model efficiently."""
        model_data = {
            'model': self.model,
            'encoder': self.encoder,
            'feature_names': self.encoder.get_feature_names_out(['Locality', 'Cuisines']).tolist() + ['avg_cost_for_two']
        }

        model_path = os.path.join(os.path.dirname(__file__), 'restaurant_recommender.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f, protocol=pickle.HIGHEST_PROTOCOL)

    @lru_cache(maxsize=128)
    def _get_cached_restaurants(self, locality, cuisine):
        """Get restaurants with caching for better performance."""
        return self._get_restaurants_by_criteria_internal(locality, cuisine)

    def get_restaurants_by_criteria(self, locality, cuisine, predicted_rating):
        """Get actual restaurants matching the criteria from dataset"""
        if self.df is None:
            return self.get_fallback_restaurants(locality, cuisine, predicted_rating)

        try:
            # Filter restaurants by locality and cuisine
            filtered_df = self.df[
                (self.df['Locality'].str.contains(locality, case=False, na=False)) &
                (self.df['Cuisines'].str.contains(cuisine, case=False, na=False))
            ].copy()

            if filtered_df.empty:
                # If no exact matches, get restaurants from the same locality
                filtered_df = self.df[self.df['Locality'].str.contains(locality, case=False, na=False)].copy()

            if filtered_df.empty:
                # If still no matches, get restaurants with similar cuisine
                filtered_df = self.df[self.df['Cuisines'].str.contains(cuisine, case=False, na=False)].copy()

            if not filtered_df.empty:
                # Sort by rating and get top restaurants
                top_restaurants = filtered_df.nlargest(3, 'aggregate_rating')

                restaurants = []
                for _, row in top_restaurants.iterrows():
                    restaurants.append({
                        'name': row['Name'],
                        'rating': float(row['aggregate_rating']),
                        'address': f"{row['Locality']}, Indore",
                        'cuisine': row['Cuisines'],
                        'cost_for_two': int(row['avg_cost_for_two'])
                    })

                return restaurants
            else:
                return self.get_fallback_restaurants(locality, cuisine, predicted_rating)

        except Exception as e:
            logger.error(f"Error getting restaurants: {e}")
            return self.get_fallback_restaurants(locality, cuisine, predicted_rating)

    def get_fallback_restaurants(self, locality, cuisine, predicted_rating):
        """Fallback restaurant data when dataset is not available"""
        return [
            {
                'name': f'Top {cuisine} Restaurant',
                'rating': round(predicted_rating + 0.3, 1),
                'address': f'{locality}, Indore',
                'cuisine': cuisine,
                'cost_for_two': 500
            },
            {
                'name': f'Popular {cuisine} Place',
                'rating': round(predicted_rating + 0.1, 1),
                'address': f'{locality}, Indore',
                'cuisine': cuisine,
                'cost_for_two': 400
            },
            {
                'name': f'{cuisine} Corner',
                'rating': round(predicted_rating - 0.1, 1),
                'address': f'{locality}, Indore',
                'cuisine': cuisine,
                'cost_for_two': 350
            }
        ]

    @lru_cache(maxsize=256)
    def predict(self, locality, cuisine):
        """
        Predict restaurant recommendations using optimized ML model.

        Args:
            locality (str): The locality/area name
            cuisine (str): The cuisine type

        Returns:
            dict: Prediction results including restaurants, rating, and other details
        """
        try:
            # Normalize inputs for consistency
            locality = locality.strip().title()
            cuisine = cuisine.strip().title()

            # Check if model is loaded and dataset is available
            if not self.model_loaded or self.model is None or self.encoder is None:
                return self._fallback_predict(locality, cuisine)

            # Optimized existence check with caching
            locality_exists = self._check_locality_exists(locality)
            cuisine_exists = self._check_cuisine_exists(cuisine)

            if not locality_exists:
                return {
                    'status': 'locality_not_found',
                    'message': f'Locality "{locality}" not found in our database.',
                    'suggested_localities': self.localities[:10],
                    'model_used': True
                }

            if not cuisine_exists:
                return {
                    'status': 'cuisine_not_found',
                    'message': f'Cuisine "{cuisine}" not found in our database.',
                    'available_cuisines': self.cuisines[:15],
                    'model_used': True
                }

            # Optimized prediction with cached median cost
            predicted_rating = self._get_prediction_score(locality, cuisine)

            # Get actual restaurants
            restaurants = self.get_restaurants_by_criteria(locality, cuisine, predicted_rating)

            return {
                'status': 'success',
                'locality': locality,
                'cuisine': cuisine,
                'predicted_rating': predicted_rating,
                'restaurants': restaurants,
                'model_used': True
            }

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return self._fallback_predict(locality, cuisine)

    @lru_cache(maxsize=64)
    def _check_locality_exists(self, locality):
        """Check if locality exists with caching."""
        return any(locality.lower() in loc.lower() for loc in self.localities)

    @lru_cache(maxsize=64)
    def _check_cuisine_exists(self, cuisine):
        """Check if cuisine exists with caching."""
        return any(cuisine.lower() in cuis.lower() for cuis in self.cuisines)

    @lru_cache(maxsize=128)
    def _get_prediction_score(self, locality, cuisine):
        """Get prediction score with caching."""
        # Use cached median cost
        avg_cost = getattr(self, '_cached_median_cost', None)
        if avg_cost is None:
            avg_cost = self.df['avg_cost_for_two'].median() if self.df is not None else 500
            self._cached_median_cost = avg_cost

        # Create input efficiently
        input_data = pd.DataFrame({
            'Locality': [locality],
            'Cuisines': [cuisine],
            'avg_cost_for_two': [avg_cost]
        })

        # Encode and predict
        categorical_encoded = self.encoder.transform(input_data[['Locality', 'Cuisines']])
        X_pred = np.column_stack([categorical_encoded, input_data['avg_cost_for_two'].values])

        predicted_rating = self.model.predict(X_pred)[0]
        return round(max(1.0, min(5.0, predicted_rating)), 1)

    def _fallback_predict(self, locality, cuisine):
        """Optimized fallback prediction when ML model is not available."""
        # Normalize inputs
        locality = locality.strip().title()
        cuisine = cuisine.strip().title()

        # Optimized rule-based prediction with better logic
        cuisine_ratings = {
            'north indian': 4.2,
            'south indian': 4.2,
            'chinese': 4.1,
            'italian': 4.1,
            'fast food': 3.8,
            'street food': 4.3,
            'desserts': 4.0,
            'cafe': 3.9
        }

        predicted_rating = cuisine_ratings.get(cuisine.lower(), 4.0)

        # Get fallback restaurants
        restaurants = self.get_fallback_restaurants(locality, cuisine, predicted_rating)

        return {
            'status': 'success',
            'locality': locality,
            'cuisine': cuisine,
            'predicted_rating': predicted_rating,
            'restaurants': restaurants,
            'model_used': False
        }

    def get_localities(self):
        """Return the list of available localities"""
        return self.localities

    def get_cuisines(self):
        """Return the list of available cuisines"""
        return self.cuisines

    def get_cuisines_for_locality(self, locality):
        """Return available cuisines for a specific locality with optimization."""
        if self.df is None:
            return self.cuisines[:10]  # Return top cuisines as fallback

        try:
            # Get cuisines available in the specific locality
            locality_restaurants = self.df[
                self.df['Locality'].str.contains(locality, case=False, na=False)
            ]

            if not locality_restaurants.empty:
                available_cuisines = locality_restaurants['Cuisines'].unique().tolist()
                return sorted(available_cuisines)
            else:
                return self.cuisines[:10]

        except Exception as e:
            logger.error(f"Error getting cuisines for locality: {e}")
            return self.cuisines[:10]

# Optimized singleton pattern with lazy loading
_recommender_instance = None

def get_recommender():
    """Get singleton recommender instance with lazy loading."""
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = RestaurantRecommender()
    return _recommender_instance

# Optimized API functions
def get_prediction(locality, cuisine):
    """Get restaurant prediction."""
    return get_recommender().predict(locality, cuisine)

def get_localities():
    """Get available localities."""
    return get_recommender().get_localities()

def get_cuisines():
    """Get available cuisines."""
    return get_recommender().get_cuisines()

def get_cuisines_for_locality(locality):
    """Get cuisines for specific locality."""
    return get_recommender().get_cuisines_for_locality(locality)
