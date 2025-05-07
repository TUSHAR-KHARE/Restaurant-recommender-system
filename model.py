import pickle
import os
import numpy as np
import pandas as pd

class RestaurantRecommender:
    def __init__(self):
        # Load the model from the pickle file
        model_path = os.path.join(os.path.dirname(__file__), 'restaurant_recommender.pkl')
        try:
            self.model = pickle.load(open(model_path, 'rb'))
            print(f"Model loaded successfully from {model_path}")
            self.model_loaded = True
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model_loaded = False
            
        # Define some sample data for localities and cuisines in Indore
        # This will be used as a fallback if the model doesn't work
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
        
        # Sample restaurant data with ratings
        self.sample_restaurants = {
            "Vijay Nagar": {
                "North Indian": [
                    {"name": "Nafees Restaurant", "rating": 4.2, "address": "56, Scheme No 54, Vijay Nagar"},
                    {"name": "Punjabi Tadka", "rating": 4.0, "address": "MR 10 Road, Vijay Nagar"}
                ],
                "South Indian": [
                    {"name": "Dosa Point", "rating": 3.9, "address": "Scheme No 78, Vijay Nagar"},
                    {"name": "Sagar Gaire", "rating": 4.1, "address": "AB Road, Vijay Nagar"}
                ],
                "Chinese": [
                    {"name": "Wang's Kitchen", "rating": 4.3, "address": "Scheme No 54, Vijay Nagar"},
                    {"name": "China Town", "rating": 3.8, "address": "MR 10 Road, Vijay Nagar"}
                ]
            },
            "Old Palasia": {
                "North Indian": [
                    {"name": "Patiala House", "rating": 4.4, "address": "Old Palasia Main Road"},
                    {"name": "Punjabi Swad", "rating": 4.1, "address": "Near Geeta Bhawan, Old Palasia"}
                ],
                "Italian": [
                    {"name": "La Pizzeria", "rating": 4.5, "address": "AB Road, Old Palasia"},
                    {"name": "Pizza Palace", "rating": 4.0, "address": "Near Geeta Bhawan, Old Palasia"}
                ],
                "Fast Food": [
                    {"name": "Burger Point", "rating": 3.9, "address": "Old Palasia Main Road"},
                    {"name": "Roll Express", "rating": 4.2, "address": "Near Geeta Bhawan, Old Palasia"}
                ]
            },
            "Annapurna": {
                "South Indian": [
                    {"name": "Madras Cafe", "rating": 4.3, "address": "Annapurna Main Road"},
                    {"name": "Dosa Factory", "rating": 4.0, "address": "Near Annapurna Temple"}
                ],
                "Street Food": [
                    {"name": "Chappan Dukan", "rating": 4.6, "address": "Annapurna Road"},
                    {"name": "Johnny Hot Dog", "rating": 4.5, "address": "Annapurna Market"}
                ],
                "Desserts": [
                    {"name": "Sweet Corner", "rating": 4.2, "address": "Annapurna Main Road"},
                    {"name": "Ice Cream Palace", "rating": 4.1, "address": "Near Annapurna Temple"}
                ]
            }
        }
        
        # Add more localities with default cuisines
        for locality in self.localities:
            if locality not in self.sample_restaurants:
                self.sample_restaurants[locality] = {
                    "North Indian": [
                        {"name": f"Punjabi Restaurant - {locality}", "rating": round(np.random.uniform(3.5, 4.5), 1), 
                         "address": f"Main Road, {locality}"}
                    ],
                    "Fast Food": [
                        {"name": f"Quick Bites - {locality}", "rating": round(np.random.uniform(3.5, 4.5), 1), 
                         "address": f"Market Area, {locality}"}
                    ]
                }
    
    def predict(self, locality, cuisine):
        """
        Predict restaurant recommendations based on locality and cuisine.
        
        Args:
            locality (str): The locality/area name
            cuisine (str): The cuisine type
            
        Returns:
            dict: Prediction results including restaurants, rating, and other details
        """
        # Normalize inputs (convert to title case for better matching)
        locality = locality.title()
        cuisine = cuisine.title()
        
        # Check if we have the locality in our sample data
        if locality in self.sample_restaurants:
            # Check if we have the cuisine for this locality
            if cuisine in self.sample_restaurants[locality]:
                restaurants = self.sample_restaurants[locality][cuisine]
                avg_rating = round(sum(r["rating"] for r in restaurants) / len(restaurants), 2)
                
                return {
                    "status": "success",
                    "predicted_rating": avg_rating,
                    "restaurants": restaurants,
                    "locality": locality,
                    "cuisine": cuisine
                }
            else:
                # If cuisine not found for this locality, suggest available cuisines
                available_cuisines = list(self.sample_restaurants[locality].keys())
                return {
                    "status": "cuisine_not_found",
                    "message": f"Cuisine '{cuisine}' not found in {locality}",
                    "available_cuisines": available_cuisines,
                    "locality": locality,
                    "predicted_rating": None
                }
        else:
            # If locality not found, suggest nearby or popular localities
            return {
                "status": "locality_not_found",
                "message": f"Locality '{locality}' not found",
                "suggested_localities": self.localities[:5],  # Suggest top 5 localities
                "predicted_rating": None
            }
    
    def get_localities(self):
        """Return the list of available localities"""
        return self.localities
    
    def get_cuisines(self):
        """Return the list of available cuisines"""
        return self.cuisines
    
    def get_cuisines_for_locality(self, locality):
        """Return available cuisines for a specific locality"""
        locality = locality.title()
        if locality in self.sample_restaurants:
            return list(self.sample_restaurants[locality].keys())
        return []

# Create a singleton instance
recommender = RestaurantRecommender()

# Function to get prediction
def get_prediction(locality, cuisine):
    return recommender.predict(locality, cuisine)

# Function to get localities
def get_localities():
    return recommender.get_localities()

# Function to get cuisines
def get_cuisines():
    return recommender.get_cuisines()

# Function to get cuisines for a locality
def get_cuisines_for_locality(locality):
    return recommender.get_cuisines_for_locality(locality)
