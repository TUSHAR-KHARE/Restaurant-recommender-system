from model import get_prediction, get_localities, get_cuisines

# Test the model functions
print("Available localities:")
print(get_localities())

print("\nAvailable cuisines:")
print(get_cuisines())

# Test prediction with valid locality and cuisine
print("\nPrediction for Vijay Nagar and North Indian:")
result = get_prediction("Vijay Nagar", "North Indian")
print(result)

# Test prediction with valid locality but invalid cuisine
print("\nPrediction for Vijay Nagar and Italian (which might not be available):")
result = get_prediction("Vijay Nagar", "Italian")
print(result)

# Test prediction with invalid locality
print("\nPrediction for Invalid Locality and North Indian:")
result = get_prediction("Invalid Locality", "North Indian")
print(result)
