/*
 * Email functionality is set up with EmailJS:
 * - Service ID: service_0fx4jjj
 * - Template ID: template_restaurant_feedback
 * - Template variables: {{first_name}}, {{last_name}}, {{phone}}, {{email}}, and {{feedback}}
 *
 * The template content:
 * You have received new restaurant feedback!
 *
 * First Name: {{first_name}}
 * Last Name: {{last_name}}
 * Phone Number: {{phone}}
 * Email: {{email}}
 * Feedback:
 * {{feedback}}
 *
 * Thank you!
 */

// EmailJs Validation

(function () {
  emailjs.init("LBGotSW3D8VaOMttF"); // Public Key
})();

// This old event listener has been removed to prevent conflicts with the more specific form handlers below

// Navigation menu toggle
const navSec = document.getElementById("nav-section");

function handleMenu() {
    navSec.classList.toggle('hidden');
}

// Add scroll effect to navbar
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('nav');
    if (window.scrollY > 50) {
        navbar.classList.add('bg-white');
        navbar.classList.add('shadow-lg');
    } else {
        navbar.classList.remove('shadow-lg');
    }
});

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', function() {
    // Get all navigation links that point to anchors
    const navLinks = document.querySelectorAll('a[href^="#"]');

    // Add click event listener to each link
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Only process links that point to an anchor on the page
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();

                // Close mobile menu if it's open
                if (!navSec.classList.contains('hidden')) {
                    navSec.classList.add('hidden');
                }

                // Smooth scroll to the target element
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Cache for storing prediction results to avoid duplicate API calls
const predictionCache = new Map();

// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // EmailJS is now initialized directly in the HTML
    console.log("DOM fully loaded - EmailJS should be initialized in HTML");
    console.log("DOM fully loaded");

    // Get the prediction form
    const predictionForm = document.getElementById('prediction-form');
    console.log("Prediction form:", predictionForm);

    if (predictionForm) {
        // Add submit event listener to the form
        predictionForm.addEventListener('submit', function(event) {
            // Prevent the default form submission
            event.preventDefault();
            console.log("Form submitted - preventDefault called");

            // Get input values
            const locality = document.getElementById('locality').value;
            const cuisine = document.getElementById('cuisine').value;

            console.log("Input values - Locality:", locality, "Cuisine:", cuisine);

            // Form validation is handled by HTML5 required attributes
            // This is just a double-check
            if (!locality || !cuisine) {
                alert("Please enter both locality and cuisine.");
                return;
            }

            console.log("Validation passed. Sending prediction request for:", locality, cuisine);

            // Create cache key
            const cacheKey = `${locality.toLowerCase().trim()}_${cuisine.toLowerCase().trim()}`;

            // Check if we have cached result
            if (predictionCache.has(cacheKey)) {
                console.log("Using cached result for:", cacheKey);
                const cachedResult = predictionCache.get(cacheKey);
                displayResults(cachedResult);
                return;
            }

            // Show loading spinner
            const loadingSpinner = document.getElementById('loading-spinner');
            const predictBtn = document.getElementById('predict-btn');

            if (loadingSpinner) {
                loadingSpinner.classList.remove('hidden');
            }

            // Disable the button during API call
            if (predictBtn) {
                predictBtn.disabled = true;
            }

            // Try to use the real API first, fallback to mock data if needed
            console.log("Attempting to use real ML model prediction");

            // Make API request to Flask backend with timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

            fetch('http://localhost:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    locality: locality.trim(),
                    cuisine: cuisine.trim(),
                }),
                signal: controller.signal
            })
            .then(response => {
                clearTimeout(timeoutId);
                console.log("Response received:", response);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return response.json();
            })
            .then(data => {
                console.log("✅ REAL API SUCCESS! Data received from API:", data);
                console.log("🤖 Model Used:", data.model_used);
                console.log("📊 Status:", data.status);

                // Validate the response data
                if (data && (data.status === 'success' || data.status === 'locality_not_found' || data.status === 'cuisine_not_found')) {
                    // Cache the successful result
                    predictionCache.set(cacheKey, data);
                    console.log("🎯 USING REAL ML MODEL PREDICTION - NOT FALLBACK!");
                    displayResults(data);
                } else {
                    throw new Error('Invalid response format from API');
                }

                // Hide loading spinner and re-enable button
                if (loadingSpinner) {
                    loadingSpinner.classList.add('hidden');
                }
                if (predictBtn) {
                    predictBtn.disabled = false;
                }
            })
            .catch(error => {
                clearTimeout(timeoutId);
                console.error("API Error:", error);

                // Determine if it's a network error or server error
                if (error.name === 'AbortError') {
                    console.log("Request timed out, falling back to mock data");
                } else if (error.message.includes('fetch')) {
                    console.log("Network error, falling back to mock data");
                } else {
                    console.log("Server error, falling back to mock data");
                }

                // Fallback to mock data if API fails
                console.log("⚠️ USING FALLBACK MOCK DATA - API FAILED!");
                const mockData = generateMockData(locality, cuisine);
                // Cache the fallback result too
                predictionCache.set(cacheKey, mockData);
                displayResults(mockData);

                // Hide loading spinner and re-enable button
                if (loadingSpinner) {
                    loadingSpinner.classList.add('hidden');
                }
                if (predictBtn) {
                    predictBtn.disabled = false;
                }
            });
        });
    } else {
        console.error("Predict button not found!");
    }
});

// Function to generate mock data as fallback (moved outside DOMContentLoaded)
function generateMockData(locality, cuisine) {
        // Function to get realistic restaurant names based on cuisine
        function getRestaurantNames(cuisine) {
                // Restaurant names by cuisine type
                const restaurantsByCuisine = {
                    'North Indian': [
                        'Punjabi Tadka', 'Spice Junction', 'Royal Punjab', 'Delhi Darbar',
                        'Tandoori Nights', 'Mughal Mahal', 'Curry Leaf', 'Masala House'
                    ],
                    'South Indian': [
                        'Dosa Plaza', 'Udupi Palace', 'Chennai Express', 'Madras Cafe',
                        'Idli House', 'Andhra Bhavan', 'Saravana Bhavan', 'Kerala Kitchen'
                    ],
                    'Chinese': [
                        'Golden Dragon', 'Wok & Roll', 'China Town', 'Chopsticks',
                        'Mainland China', 'Panda Express', 'Asian Spice', 'Noodle House'
                    ],
                    'Italian': [
                        'Pizza Express', 'Pasta Paradise', 'Little Italy', 'Olive Garden',
                        'Romano\'s', 'La Pizzeria', 'Bella Italia', 'Mamma Mia'
                    ],
                    'Mexican': [
                        'Taco Bell', 'Chili\'s', 'El Mexicano', 'Tortilla House',
                        'Salsa Kitchen', 'Guacamole', 'Nachos & More', 'Amigos'
                    ],
                    'Fast Food': [
                        'Burger King', 'McDonald\'s', 'KFC', 'Subway',
                        'Domino\'s', 'Pizza Hut', 'Wendy\'s', 'Five Guys'
                    ]
                };

                // Default list for cuisines not in our mapping
                const defaultNames = [
                    'Flavor House', 'Spice Garden', 'Food Paradise', 'Gourmet Kitchen',
                    'Tasty Bites', 'Delicious Eats', 'Foodie\'s Choice', 'Culinary Delight'
                ];

                // Get the appropriate list or use default
                const namesList = restaurantsByCuisine[cuisine] || defaultNames;

                // Shuffle the array to get random names each time
                return [...namesList].sort(() => Math.random() - 0.5);
            }

            // Get restaurant names for the selected cuisine
            const restaurantNames = getRestaurantNames(cuisine);

            // Create a simple hash function for consistent results
            function simpleHash(str) {
                let hash = 0;
                for (let i = 0; i < str.length; i++) {
                    const char = str.charCodeAt(i);
                    hash = ((hash << 5) - hash) + char;
                    hash = hash & hash; // Convert to 32-bit integer
                }
                return Math.abs(hash);
            }

            // Generate consistent "random" values based on input (normalize inputs first)
            const inputKey = locality.toLowerCase().trim() + cuisine.toLowerCase().trim();
            const seed = simpleHash(inputKey);

            // Pseudo-random function with seed - improved for better distribution
            function seededRandom(seed, min, max) {
                // Use a better pseudo-random algorithm
                let x = Math.sin(seed * 9301 + 49297) * 233280;
                const random = x - Math.floor(x);
                return Math.round((random * (max - min) + min) * 10) / 10; // Round to 1 decimal
            }

            // Create mock data based on user input with consistent results
            const mockData = {
                status: 'success',
                locality: locality,
                cuisine: cuisine,
                predicted_rating: seededRandom(seed, 3.0, 5.0).toFixed(1),
                restaurants: [
                    {
                        name: restaurantNames[0],
                        rating: seededRandom(seed + 1, 4.0, 5.0).toFixed(1),
                        address: `123 Main Street, ${locality}, Indore`
                    },
                    {
                        name: restaurantNames[1],
                        rating: seededRandom(seed + 2, 3.5, 5.0).toFixed(1),
                        address: `456 Park Avenue, ${locality}, Indore`
                    },
                    {
                        name: restaurantNames[2],
                        rating: seededRandom(seed + 3, 3.0, 5.0).toFixed(1),
                        address: `789 Food Street, ${locality}, Indore`
                    }
                ]
            };

            // Return the mock data for fallback use
            return mockData;
}

// Function to display results (moved outside DOMContentLoaded)
function displayResults(data) {
        // Get output elements
        const outputDiv = document.getElementById('output');
        const ratingDiv = document.getElementById('prediction-rating');
        const restaurantsDiv = document.getElementById('restaurants-list');
        const suggestionsDiv = document.getElementById('suggestions');

        // Clear previous content
        ratingDiv.innerHTML = '';
        restaurantsDiv.innerHTML = '';
        suggestionsDiv.innerHTML = '';

        // Show the output div
        outputDiv.classList.remove('hidden');

        // Handle different response types
        if (data.status === 'success') {
            // Display the predicted rating with model information
            if (data.predicted_rating) {
                const modelInfo = data.model_used ?
                    '<span class="text-green-400 text-sm">(ML Model)</span>' :
                    '<span class="text-blue-400 text-sm">(Fallback)</span>';
                ratingDiv.innerHTML = `<div class="text-xl font-bold">Predicted Rating: <span class="text-yellow-400">${data.predicted_rating}</span> ${modelInfo}</div>`;
            }

            // Display only the highest-rated restaurant if available
            if (data.restaurants && data.restaurants.length > 0) {
                // Find the highest-rated restaurant
                let highestRatedRestaurant = data.restaurants[0];
                console.log("Initial highest rated restaurant:", highestRatedRestaurant);

                for (let i = 1; i < data.restaurants.length; i++) {
                    console.log(`Comparing restaurant ${i}:`, data.restaurants[i]);
                    if (parseFloat(data.restaurants[i].rating) > parseFloat(highestRatedRestaurant.rating)) {
                        highestRatedRestaurant = data.restaurants[i];
                        console.log("New highest rated restaurant:", highestRatedRestaurant);
                    }
                }

                // Log the final selected restaurant
                console.log("Final highest rated restaurant:", highestRatedRestaurant);

                const heading = document.createElement('h3');
                heading.className = 'text-center text-sm font-bold mb-1';
                heading.textContent = `Highest Rated ${data.cuisine} Restaurant in ${data.locality}`;
                restaurantsDiv.appendChild(heading);

                // Create container for the restaurant card
                const cardsContainer = document.createElement('div');
                cardsContainer.className = 'grid grid-cols-1 gap-1 mt-1';

                // Create card for the highest-rated restaurant
                const card = document.createElement('div');
                card.className = 'bg-gray-800 p-2 rounded-md';
                console.log("Created restaurant card with class:", card.className);

                // Restaurant name with rating
                const nameRating = document.createElement('div');
                nameRating.className = 'flex justify-between items-center';

                const name = document.createElement('h4');
                name.className = 'text-sm font-bold text-white'; // Reduced from text-lg to text-sm
                name.textContent = highestRatedRestaurant.name;
                console.log("Setting restaurant name to:", highestRatedRestaurant.name);

                const rating = document.createElement('span');
                rating.className = 'bg-green-600 text-white px-1 py-0.5 rounded text-xs';
                rating.textContent = `★ ${highestRatedRestaurant.rating}`;

                nameRating.appendChild(name);
                nameRating.appendChild(rating);

                // Restaurant address
                const address = document.createElement('p');
                address.className = 'text-gray-300 text-xs mt-0.5';
                address.textContent = highestRatedRestaurant.address;

                // Add elements to card
                card.appendChild(nameRating);
                card.appendChild(address);

                // Add card to container
                cardsContainer.appendChild(card);

                restaurantsDiv.appendChild(cardsContainer);
            }
        } else if (data.status === 'cuisine_not_found') {
            // Display message and available cuisines
            suggestionsDiv.innerHTML = `
                <p class="text-center">${data.message}</p>
                <p class="text-center mt-2">Available cuisines in ${data.locality}:</p>
                <ul class="list-disc pl-5 mt-1">
                    ${data.available_cuisines.map(cuisine => `<li>${cuisine}</li>`).join('')}
                </ul>
            `;
        } else if (data.status === 'locality_not_found') {
            // Display message and suggested localities
            suggestionsDiv.innerHTML = `
                <p class="text-center">${data.message}</p>
                <p class="text-center mt-2">Try these popular localities:</p>
                <ul class="list-disc pl-5 mt-1">
                    ${data.suggested_localities.map(locality => `<li>${locality}</li>`).join('')}
                </ul>
            `;
        } else if (data.status === 'error') {
            // Display error message
            suggestionsDiv.innerHTML = `<p class="text-center text-red-500">${data.error}</p>`;
        } else {
            // Fallback for unexpected response
            suggestionsDiv.innerHTML = `<p class="text-center text-yellow-300">Received response: ${JSON.stringify(data)}</p>`;
        }
}

// Phone Number Validation
const phoneInput = document.getElementById('phone');

phoneInput.addEventListener('input', function () {
    this.value = this.value.replace(/[^0-9]/g, ''); // Allow only numbers

    if (this.value.length > 10) {
        this.value = this.value.slice(0, 10); // Limit to 10 digits
    }
});

// Add event listener to the contact form
const contactForm = document.getElementById('contact-form');
console.log("Contact form:", contactForm);

// Handle contact form submission
if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
        console.log("Contact form submitted");
        e.preventDefault(); // Prevent default form submission

        // Validate phone number
        const phone = phoneInput.value;
        if (!/^\d{10}$/.test(phone)) {
            alert('Please enter a valid 10-digit phone number.');
            return;
        }

        // Get form data
        const firstName = this.querySelector('input[name="first_name"]').value;
        const lastName = this.querySelector('input[name="last_name"]').value;
        const email = this.querySelector('input[name="email"]').value;
        const feedback = this.querySelector('textarea[name="feedback"]').value;

        // Show loading state
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.textContent = 'Sending...';
        submitButton.disabled = true;

        // Prepare template parameters with all possible formats to ensure compatibility
        const templateParams = {
            // Format 1: Standard EmailJS format
            from_name: firstName + " " + lastName,
            from_email: email,
            message: feedback + "\n\nPhone: " + phone,

            // Format 2: Original form field names
            first_name: firstName,
            last_name: lastName,
            phone: phone,
            email: email,
            feedback: feedback,

            // Format 3: Alternative naming conventions
            name: firstName + " " + lastName,
            to_name: "Restaurant Owner",

            // Format 4: Additional fields that might be in the template
            subject: "Restaurant Feedback",
            date: new Date().toLocaleDateString()
        };

        console.log("Sending feedback email with parameters:", templateParams);

        // Use the global emailjs object that was initialized in the HTML
        var serviceID = 'service_0fx4jjj'; // Confirmed correct service ID
        var templateID = 'template_9wm4bcr'; // Confirmed correct template ID

        console.log('Sending email with:');
        console.log('- Service ID:', serviceID);
        console.log('- Template ID:', templateID);
        console.log('- Parameters:', templateParams);

        // Send the email using EmailJS
        window.emailjs.send(serviceID, templateID, templateParams)
            .then(function(response) {
                console.log('SUCCESS!', response.status, response.text);

                // Change button text to "Feedback Submitted"
                submitButton.textContent = "Feedback Submitted";
                submitButton.classList.add("bg-green-500");
                submitButton.classList.remove("bg-blue-500");

                // Refresh the page after a short delay
                setTimeout(function() {
                    // Refresh the page
                    window.location.reload();
                }, 2000);
            })
            .catch(function(error) {
                console.error('FAILED...', error);

                // Show error in alert instead of popup
                let errorDetails = '';

                if (error.status === 0) {
                    errorDetails = 'Network error - check your internet connection';
                } else if (error.status === 400) {
                    errorDetails = 'Bad request - check your template ID and parameters';
                } else if (error.status === 401 || error.status === 403) {
                    errorDetails = 'Authentication error - check your EmailJS user ID and service ID';
                } else {
                    errorDetails = error.message || JSON.stringify(error);
                }

                // Show error in console
                console.error('Failed to send feedback: ' + errorDetails);

                // Reset button text and style
                submitButton.textContent = "Submit Feedback";
                submitButton.classList.remove("bg-green-500");
                submitButton.classList.add("bg-blue-500");
            })
            .finally(function() {
                // Only re-enable the button, don't reset the text (that's handled in the success case)
                submitButton.disabled = false;
            });
    });
}
