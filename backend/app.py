from flask import Flask, Blueprint, send_from_directory, render_template, request, jsonify, session, make_response
from transformers import pipeline
from move_routes import move_routes
import pandas as pd
import smtplib
from dotenv import load_dotenv
from pymongo import MongoClient
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash
import re
import os 
from flask_cors import CORS
import requests
import spacy
from bson import ObjectId  # Make sure to import ObjectId
#from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from datetime import timedelta
from flask_session import Session

app = Flask(__name__, static_folder="static/build", template_folder='templates')
CORS(app, origins="http://localhost:5173", supports_credentials=True)
app.secret_key = "your_secret_key"  # Required for session management
app.config['SESSION_TYPE'] = 'filesystem'  # Configure session to use the filesystem
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False 
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Register Blueprints
app.register_blueprint(move_routes)

@app.route("/")
def home():
    return render_template("simple_chat.html")

@app.route("/yogabot")
def yogabot():
    return render_template("index.html")


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

Session(app)

load_dotenv() # Loads environment variables from .env file into the Python environment

 # Serve simple_chat.html


# Load the dataset with the 'TranslatedInstructions' column
data = pd.read_csv('new_data.csv')



# Spoonacular API key
spoonacular_api_key = '3f8c82acd48547a49f712a2ab1cdf9b1'  


# Load conversational model
text_generator = pipeline("text2text-generation", model="facebook/bart-large")

# Dictionary to hold user-selected recipe state and preferences
user_state = {}

# MongoDB connection
client = MongoClient('mongodb+srv://dileepchows9133:x1BOQmDi7dVVlpwm@meal.zfw3e.mongodb.net/')  # Update with your MongoDB URI
db = client.user_data  # Database
profiles_collection = db.profiles  # Collection
favorites_collection = db.favorites  # Collection for storing favorites

@app.route('/api/profile', methods=['POST'])
def save_profile():
    data = request.json
    # Extract firstName, lastName, email, and password from the request
    
    profiles_collection.insert_one(data)  # Save to MongoDB
    return jsonify({"message": "Profile saved successfully"}), 201

@app.route('/api/profile/<string:email>', methods=['GET'])
def get_profile(email):
    profile = profiles_collection.find_one({"email": email})
    if profile is not None:
        
        profile = convert_objectid_to_str(profile)  # Convert ObjectId to string
        return jsonify(profile), 200
    
    return jsonify({"message": "Profile not found"}), 404

@app.route('/api/profile/<string:email>', methods=['PUT'])
def update_profile(email):
    data = request.json
    profiles_collection.update_one({"email": email}, {"$set": data})
    return jsonify({"message": "Profile updated successfully"}), 200

def convert_objectid_to_str(data):
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(v) for v in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data


# Load the SpaCy language model for lemmatization
nlp = spacy.load('en_core_web_sm')

# Function to handle plural and singular forms using SpaCy
def handle_plural_ingredient(ingredient):
    # Use SpaCy to lemmatize the word (convert plural to singular)
    doc = nlp(ingredient)
    lemmatized = [token.lemma_ for token in doc][0]  # Get the lemmatized form

    # If the ingredient is already plural, add both singular and plural forms
    if ingredient != lemmatized:
        return [ingredient, lemmatized]    # Plural form comes first, singular form second

    # Otherwise, if the ingredient is singular, return both singular and regular plural form
    else:
        if ingredient.endswith('s'):
            plural_form = ingredient  # If it already ends in 's', treat it as plural
        elif ingredient.endswith('y'):
            plural_form = ingredient[:-1] + 'ies'  # Handle nouns like 'berry' -> 'berries'
        else:
            plural_form = ingredient + 's'  # Regular plural form

        return [plural_form, lemmatized ]   # Plural form comes first, singular form second



# Function to filter meal plans based on cooking time, cuisine, ingredients, and recipe name
def get_meal_plan(max_time_in_minutes=None, cuisine=None, ingredients=None, recipe_name=None):
    filtered_recipes = data

    # Filter by cooking time using -20% of the requested time - show recipes near the time range
    if max_time_in_minutes:
        time_range_percentage = 0.20  
        lower_bound = int(max_time_in_minutes * (1 - time_range_percentage))

        # Filter recipes that fall within this time range
        filtered_recipes = filtered_recipes[
            (filtered_recipes['TotalTimeInMins'] >= lower_bound) &
            (filtered_recipes['TotalTimeInMins'] <= max_time_in_minutes)
        ]


    # Filter by cuisine 
    if cuisine:
        # Normalize the user input cuisine to match the dataset cuisines
        user_input_lower = cuisine.lower()
        matched_cuisine = None
        for available_cuisine in sorted(data['Cuisine'].unique(), key=len, reverse=True):
            if user_input_lower in available_cuisine.lower():
                matched_cuisine = available_cuisine
                break
        
        if matched_cuisine:
            # Now filter by the matched cuisine (case-insensitive)
            filtered_recipes = filtered_recipes[filtered_recipes['Cuisine'].str.contains(matched_cuisine, case=False)]
        else:
            print(f"No matching cuisine found for: {cuisine}")
            return []


    # Filter by ingredients 
    if ingredients:
        for ingredient in ingredients:
            # Get both singular and plural forms of the ingredient
            ingredient_variants = handle_plural_ingredient(ingredient)
            print(f"Ingredient variants: {ingredient_variants}")

            # Create a regex pattern to match both singular and plural forms
            ingredient_pattern = '|'.join(ingredient_variants) 
            print(f"Ingredient pattern: {ingredient_pattern}")

            # Filter recipes that contain the current ingredient in 'Cleaned-Ingredients'
            filtered_recipes = filtered_recipes[filtered_recipes['Cleaned-Ingredients'].str.contains(ingredient_pattern, case=False)]
            
            # Print remaining recipes count after filtering by this ingredient
            print(f"Remaining recipes after filtering by {ingredient}: {len(filtered_recipes)}")

            # If no recipes match, stop filtering further
            if filtered_recipes.empty:
                print(f"No recipes found with the ingredient: {ingredient}")
                break

    
    #Filter by recipe name (for specific recipe name queries)
    if recipe_name:
        if isinstance(recipe_name, list):
            # If the recipe name is a list, use isin()
            filtered_recipes = filtered_recipes[filtered_recipes['TranslatedRecipeName'].str.lower().isin([r.lower() for r in recipe_name])]
        else:
            # If the recipe name is a string, match exactly
            filtered_recipes = filtered_recipes[filtered_recipes['TranslatedRecipeName'].str.lower() == recipe_name.lower()]


    # If the query is ingredient or time-based, return up to 10 random results
    if not filtered_recipes.empty:
        meal_plan = filtered_recipes[['TranslatedRecipeName', 'TotalTimeInMins', 'URL', 'TranslatedIngredients', 'image-url', 'Cleaned-Ingredients', 'TranslatedInstructions']].sample(n=min(10, len(filtered_recipes))).to_dict(orient='records')
    else:
        meal_plan = []

    return meal_plan

# Function to interpret user query and extract relevant information
def parse_user_query(user_message):
    
    """Time extraction"""
    time_match = re.search(r'(\d+)\s*(?:min(?:utes?)?)', user_message.lower())  # Minutes regex
    hour_match = re.search(r'(\d+)\s*(?:hour|hr)(?:s?)', user_message.lower())  # Hours regex
    max_time = None
    if time_match:
        max_time = int(time_match.group(1))  # Extracted time in minutes
        print(f"Extracted time in minutes: {max_time}")
    elif hour_match:
        max_time = int(hour_match.group(1)) * 60  # Convert hours to minutes
        print(f"Extracted time in hours (converted to minutes): {max_time}")
    else:
        print(f"Extracted time: None")


    """Cuisine extraction"""
    # Extract all unique cuisines from the dataset and sort them by length (longer terms first)
    unique_cuisines = sorted(data['Cuisine'].unique(), key=len, reverse=True)
    user_message_lower = user_message.lower()
    # Iterate through sorted cuisines and find the first matching cuisine
    cuisine = None
    for cuisine_option in unique_cuisines:
        cuisine_option_normalized = cuisine_option.lower()
        # Check if the normalized cuisine is a substring in the user message
        if cuisine_option_normalized in user_message_lower:
            cuisine = cuisine_option  # Full match found
            break
    print(f"Extracted cuisine: {cuisine}")


    """Ingredient extraction (supports both singular and plural)"""
    # Define keywords that often precede ingredient mentions
    keywords = ['of', 'from', 'with', 'has', 'have', 'having','containing', 'contain','contains','using', 'including', 'include', 'includes', 'ingredient', 'ingredients']
    # Combine the keywords into a single regex pattern
    keyword_pattern = '|'.join(re.escape(keyword) for keyword in keywords)
    # Regex pattern to capture everything after keywords like 'with', 'has', etc.
    ingredient_match = re.findall(rf'(?:(?:{keyword_pattern})\s*)([\w\s,]+(?:\s(?:and|or)\s[\w\s,]+)?)', user_message.lower())
    ingredient_list = []
    if ingredient_match:
        for ingredient_str in ingredient_match:
            # Split ingredients by commas, 'and', or 'or'
            ingredients = re.split(r',|\sand\s|\sor\s', ingredient_str)
            # Remove any leading/trailing spaces from each ingredient
            ingredient_list.extend([ingredient.strip() for ingredient in ingredients if ingredient.strip()])


    """Recipe name extraction"""
    # Use SpaCy to process the user message for NER and POS tagging to extract recipe keywords
    doc = nlp(user_message)
    # List to store unique recipe keywords while maintaining order
    recipe_keywords = []
    common_words = [
    'I', 'a', 'about', 'am', 'amazing', 'an', 'and', 'any', 'are', 'around', 'as', 'at', 'away', 
    'awesome', 'be', 'been', 'being', 'best', 'briefly', 'but', 'by', 'bye', 'can', 'comforting', 
    'could', 'containing','cuisine', 'cuisines', 'currently', 'delicious', 'did', 'directly', 'do', 'does', 
    'easy', 'else', 'excellent', 'fabulous', 'family', 'famous', 'fantastic', 'fast', 'festive', 
    'find', 'fine', 'for', 'from', 'get', 'give', 'good', 'great', 'had', 'has', 'have', 'hello', 
    'help', 'hey', 'hi', 'how', 'having', 'i', 'if', 'in', 'in no time at all', 'instantly', 'including', 'is', 'it', 
    'lately', 'like', 'looking', 'may', 'me', 'might', 'momentarily', 'must', 'my', 'need', 
    'nice', 'no', 'not', 'now', 'nowadays', 'occasion', 'of', 'ok', 'okay', 'on', 'or', 'out', 
    'over', 'party', 'please', 'pls', 'plz', 'popular', 'presently', 'promptly', 'quick', 
    'quickly', 'recently', 'recipe', 'recipes', 'recommend', 'serve', 'shall', 'shortly', 
    'should', 'show', 'simple', 'some', 'soon', 'special', 'speedily', 'suggest', 'superb', 
    'sure', 'swiftly', 'tasty', 'than', 'thank', 'thanks', 'thankyou', 'that', 'the', 'then', 
    'there', 'they', 'this', 'to', 'trending', 'using', 'want', 'was', 'we', 'well', 'were', 'what', 
    'when', 'where', 'which', 'why', 'will', 'with', 'wonderful', 'would', 'yes', 'you', 
    'your', 'yum', 'yummy', 'yumyum']

    # Use NER to find potential dish names, food items, or relevant entities
    for ent in doc.ents:
        # Check if the entity label is related to food or a dish (e.g., 'FOOD', 'PRODUCT')
        if ent.label_ in ['PRODUCT', 'FOOD']:
            recipe_keywords.append(ent.text.lower())

    # Use POS tagging to capture additional nouns/proper nouns as recipe names
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN'] and token.lemma_ not in common_words and token.text not in recipe_keywords:
            # Exclude numbers identified as time
            if not token.text.isdigit() or not max_time:
                recipe_keywords.append(token.text.lower())

    # Refine regex to capture potential recipe names while excluding common words
    food_keywords = [word for word in re.findall(r'\b\w+\b', user_message.lower()) if word not in common_words and not word.isdigit()]
    print(f"Extracted food keywords using NER and POS tagging: {food_keywords}")
    
    # Add custom regex-extracted keywords to recipe_keywords list if not already present
    for word in food_keywords:
        if word.lower() not in recipe_keywords:
            recipe_keywords.append(word.lower())

    # Join the keywords back into a single string for matching
    recipe_search_query = ' '.join(recipe_keywords)
    print(f"Extracted recipe search keywords using NER, POS tagging, and refined regex: {recipe_search_query}")

    # Now, find all recipes that match the user query using partial matching
    if recipe_search_query:
        word_boundary_query = r'\b' + re.escape(recipe_search_query) + r'\b'
        recipe_name_match = data['TranslatedRecipeName'].str.contains(word_boundary_query, case=False, regex=True)
        recipe_name = data[recipe_name_match]['TranslatedRecipeName'].tolist()
    else:
        recipe_name = []
    print(f"Extracted recipe name matches: {recipe_name}")
    
    
    return max_time, cuisine, ingredient_list, recipe_name

def process_user_request(user_message):
    # Handle casual conversation
    if 'hello' in user_message.lower():
        return "Hello! How can I assist you today?"
    if 'how are you' in user_message.lower():
        return "I'm doing great! How about you?"

    # Check for exclusion keywords like "without," "allergic to," etc.
    exclusion_keywords = ['without', 'allergic to', 'except', 'excluding']
    if any(keyword in user_message.lower() for keyword in exclusion_keywords):
        print(f"Exclusion keyword found in the query: {user_message}. Passing the request to Spoonacular.")
        # If exclusion is detected, pass the query directly to Spoonacular
        spoonacular_response = fetch_from_spoonacular(user_message)
        if 'error' not in spoonacular_response:
            return format_response(spoonacular_response)
        else:
            return spoonacular_response['error']
    
    # Parse the user's message to extract time, cuisine, ingredient, and recipe name preferences
    max_time, cuisine, ingredients, recipe_name = parse_user_query(user_message)

    # If no ingredients, recipe name, or other relevant info is found, fallback to Spoonacular
    if not ingredients and not recipe_name and not cuisine and not max_time:
        print("No relevant data found in user input. Querying Spoonacular.")
        spoonacular_response = fetch_from_spoonacular(user_message)
        if 'error' not in spoonacular_response:
            return format_response(spoonacular_response)
        else:
            return spoonacular_response['error']

    # If the user is searching for a specific cuisine
    if cuisine or max_time or ingredients:
        meal_plan = get_meal_plan(max_time_in_minutes=max_time, cuisine=cuisine, ingredients=ingredients)
        if meal_plan:
            user_state['meal_plan'] = meal_plan
            # Display a list of meal options filtered by cuisine
            response = f"Here are some meal options:\n"
            for idx, recipe in enumerate(meal_plan):
                response += f"<button>{idx + 1}. {recipe['TranslatedRecipeName']} (Takes {recipe['TotalTimeInMins']} minutes)</button><br>"
            response += "\nPlease select a recipe by clicking a button or let me know if you prefer a different cuisine or ingredient."
            return response
        
    # If the user is searching for a specific recipe by exact name    
    if recipe_name:
        for recipe in recipe_name:
            # If the exact recipe name is found in the user's input, display that recipe only
            if recipe.lower() in user_message.lower():
                meal_plan = get_meal_plan(recipe_name=recipe)
                if meal_plan:
                    selected_recipe = meal_plan[0]  # Return the first matching recipe (exact match)
                    response = f"<strong>Here is the recipe for </strong>{selected_recipe['TranslatedRecipeName']}<br>\n"
                    response += f"<strong>Ingredients:</strong> {selected_recipe['TranslatedIngredients']}<br>\n"
                    response += f"<strong>Procedure:</strong> {selected_recipe['TranslatedInstructions']}<br>\n"
                    response += f"<strong>Need more info?:</strong> <a href='{selected_recipe['URL']}' target='_blank'>{selected_recipe['URL']}</a><br>\n"
                    response += f"<img src='{selected_recipe['image-url']}' alt='Recipe Image' width='200'><br>"
                    return response

    # Handle time, cuisine, or ingredient-based queries (meal suggestions)
    meal_plan = get_meal_plan(max_time_in_minutes=max_time, cuisine=cuisine, ingredients=ingredients, recipe_name=recipe_name)
    if meal_plan:
        user_state['meal_plan'] = meal_plan
        # Display a list of up to 10 random meal options
        response = "Here are some meal options:\n"
        for idx, recipe in enumerate(meal_plan):
            response += f"<button>{idx + 1}. {recipe['TranslatedRecipeName']} (Takes {recipe['TotalTimeInMins']} minutes)</button><br>"
        response += "\nPlease select a recipe by clicking a button or let me know if you prefer a different cuisine or ingredient."
        return response
    
    # If no results found locally, fallback to Spoonacular
    print("No matching recipes found locally. Querying Spoonacular.")
    spoonacular_response = fetch_from_spoonacular(user_message)
    if 'error' not in spoonacular_response:
        return format_response(spoonacular_response)
    else:
        return spoonacular_response['error']

# Handle selected recipe
def handle_recipe_selection(user_message):
    if user_message.isdigit() and 'meal_plan' in user_state:
        selected_idx = int(user_message) - 1
        if 0 <= selected_idx < len(user_state['meal_plan']):
            selected_recipe = user_state['meal_plan'][selected_idx]
            
            # Split the procedure paragraph into sentences
            instructions = selected_recipe['TranslatedInstructions']
            instruction_points = instructions.split('.')  # Split sentences based on '.'
            
            # Format instructions into a bullet list
            formatted_instructions = "<ul>"
            for instruction in instruction_points:
                if instruction.strip():  # Avoid empty strings
                    formatted_instructions += f"<li>{instruction.strip()}.</li>"
            formatted_instructions += "</ul>"
            
            # Display the selected recipe's details
            response = f"<strong>Ok, good choice! Here's the recipe for </strong>{selected_recipe['TranslatedRecipeName']}<br>\n"
            response += f"<strong>Ingredients: </strong>{selected_recipe['TranslatedIngredients']}<br>\n"
            response += f"<strong>Procedure: </strong>{formatted_instructions}<br>\n"
            response += f"<strong>Need more info?: </strong><a href='{selected_recipe['URL']}' target='_blank'>{selected_recipe['URL']}</a><br>\n"
            response += f"<img src='{selected_recipe['image-url']}' alt='Recipe Image' width='200'><br>"
            return response
        else:
            return "Invalid selection. Please select a valid recipe number."
    else:
        return None
   
def fetch_from_spoonacular(query):
    print(f"Fetching recipe from Spoonacular API for query: {query}")
    # Step 1: Search for recipes using complexSearch
    url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={spoonacular_api_key}&addRecipeInformation=true&fillIngredients=true"
    response = requests.get(url)
    
    # Check if the response was successful (status code 200)
    if response.status_code != 200:
        print(f"Error from Spoonacular API: {response.status_code}, {response.text}")
        return {"error": f"Failed to fetch recipe. Error: {response.status_code}"}
    
    data = response.json()
    
    # Safely check if the 'results' key exists
    if 'results' in data and len(data['results']) > 0:
        # Get the first recipe from the result
        recipe_id = data['results'][0]['id']  # Extract the recipe ID
        
        # Step 2: Fetch detailed information about the recipe using the ID
        recipe_details_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={spoonacular_api_key}&includeNutrition=false"
        recipe_details_response = requests.get(recipe_details_url)
        
        # Check if the recipe details request was successful
        if recipe_details_response.status_code != 200:
            print(f"Error fetching recipe details: {recipe_details_response.status_code}, {recipe_details_response.text}")
            return {"error": f"Failed to fetch recipe details. Error: {recipe_details_response.status_code}"}
        
        recipe_details = recipe_details_response.json()
        
        # Prepare the response with detailed information
        response = {
            "recipe_name": recipe_details['title'],
            "ingredients": ', '.join([ingredient['name'] for ingredient in recipe_details.get('extendedIngredients', [])]),
            "instructions": recipe_details.get('instructions', 'Instructions not available'),
            "url": recipe_details.get('sourceUrl', 'URL not available'),
            "image_url": recipe_details.get('image', 'Image not available')
        }
        print(f"Found detailed recipe from Spoonacular: {response}")
        return response
    else:
        print("No results found in Spoonacular API response.")
        return {"error": "No recipes found for this query."}

# Helper function to format the response for display
def format_response(response_data):
    return (
        f"<strong>Here is the recipe for </strong>{response_data['recipe_name']}<br>\n"
        f"<strong>Ingredients:</strong> {response_data['ingredients']}<br>\n"
        f"<strong>Procedure:</strong> {response_data['instructions']}<br>"
        f"<strong>Need more info?:</strong> <a href='{response_data['url']}' target='_blank'>{response_data['url']}</a><br>\n"
        f"<img src='{response_data['image_url']}' alt='Recipe Image' width='200'><br>"
    )


def send_registration_email(user_email):
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    subject = "Registration Successful"
    message = f"Hello,\n\nThank you for registering! Your account has been successfully created."

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = user_email

    try:
        # Connect to the Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, msg.as_string())
            print(f"Email sent to {user_email}")
    except smtplib.SMTPAuthenticationError:
        print("Authentication error: Please check your email and password.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {str(e)}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Save a user's favorite meal  or yoga routine
@app.route('/favorite', methods=['POST'])
def add_favorite():
    #user_email = request.cookies.get('user_email')  # Retrieve the email from cookie
    # Ensure the user is logged in by checking if email is in session
    # Check if the user is authenticated
    user_email = request.cookies.get('user_email')
    if not user_email:
        return jsonify({"message": "User not authenticated"}), 401  # Unauthorized
    
    # Get the favorite item from the request body
    favorite_item = request.json.get('favorite')

    if not favorite_item:
        return jsonify({"message": "No favorite item provided"}), 400  # Bad Request

    # Check if the user already has a favorites list in the database
    existing_favorite = favorites_collection.find_one({"email": user_email})

    if existing_favorite:
        # User already has a favorite entry, so we update their favorites list
        favorites_collection.update_one(
            {"email": user_email},
            {"$addToSet": {"favorites": favorite_item}}  # Adds the item if it's not already in the list
        )
    else:
        # If user doesn't have a favorites entry, create a new one
        favorites_collection.insert_one({
            "email": user_email,
            "favorites": [favorite_item]  # Create a new list with the favorite item
        })

    return jsonify({"message": "Favorite added successfully"}), 200


@app.route('/favorite', methods=['GET'])
def get_favorites():
    user_email = request.args.get('email')  # Change to 'email' to match the frontend
    print(f"Fetching favorites for email: {user_email}")
    
    user_data = favorites_collection.find_one({"email": user_email})
    if user_data:
        # Convert ObjectId to string if necessary
        print(f"Found user data: {user_data}")
        user_data = convert_objectid_to_str(user_data)
        
        # Return both meal and yoga favorites in a unified response
        return jsonify({
            "favorites": user_data.get("favorites", [])  # Assuming you have a single "favorites" array
        }), 200
    else:
        print("No user data found.")
        return jsonify({"message": "No favorites found"}), 404



    
@app.route('/signup', methods=['POST'])
def signup():
    if request.is_json:
        # Extract user information from request
        first_name = request.json.get('firstName')
        last_name = request.json.get('lastName')
        user_email = request.json.get('email')
        password = request.json.get('password')

        # Check if required fields are provided
        if not first_name or not last_name or not user_email or not password:
            return jsonify({"message": "First name, last name, email, and password are required"}), 400

        # Hash the password for storage
        hashed_password = generate_password_hash(password)

        # Save the user information (including hashed password) to MongoDB
        profiles_collection.insert_one({
            "firstName": first_name,
            "lastName": last_name,
            "email": user_email,
            "password": hashed_password
        })

        # Send a registration email
        send_registration_email(user_email)

        return jsonify({"message": "Registration successful!"})

    else:
        return jsonify({"error": "Invalid JSON format"}), 400


@app.route('/login', methods=['POST'])
def login():
    user_email = request.json.get('email')
    password = request.json.get('password')
    
    # Retrieve the user profile from MongoDB
    user_profile = profiles_collection.find_one({"email": user_email})
    if user_profile and check_password_hash(user_profile['password'], password):
        # Store user email in session for tracking
        session['user_email'] = user_email
        # Create a response object and set a cookie for user email
        response = make_response(jsonify({"message": "Login successful!"}), 200)
        response.set_cookie('user_email', user_email, max_age=3600, domain='localhost', path='/', httponly=True, samesite='None', secure=True)  # samesite='None' for cross-origin, secure=True for HTTPS
        print(f'User email from cookie: {user_email}')  # Log the cookie value
        return response
    else:
        return jsonify({"message": "Invalid email or password!"}), 401
    
@app.route('/get_cookie', methods=['GET'])
def get_cookie():
    user_email = request.cookies.get('user_email')  # Retrieve the cookie
    if user_email:
        return jsonify({'user_email': user_email}), 200
    else:
        return jsonify({'error': 'No cookie found'}), 404
    
@app.route('/test-cookie', methods=['GET'])
def test_cookie():
    response = make_response(jsonify({"message": "Test successful!"}), 200)
    response.set_cookie('user_email', 'test@example.com', httponly=True, samesite='Lax')
    return response

# Flask route to handle chat
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    print(f"User input: {user_input}")

    # Step 1: Search the data.csv file
    # Check if the input starts with a digit (recipe selection)
    # Extract the first digit which corresponds to the selected recipe number
    recipe_selection_match = re.match(r'(\d+)', user_input)
    
    if recipe_selection_match:
        # Extract the recipe number from the input
        selected_recipe_number = recipe_selection_match.group(1)
        print(f"Selected recipe number: {selected_recipe_number}")
        
        # Handle recipe selection by the user
        bot_reply = handle_recipe_selection(selected_recipe_number)
        return jsonify({'response': bot_reply})
    
    
    # If it's not a digit, process the user query to display the meal plan or recipe
    bot_reply = process_user_request(user_input)
    if bot_reply:
        return jsonify({'response': bot_reply})
   
  
    #find data from fine_tuned model
    # fine_tuned_response = generate_response(user_input)
    # if fine_tuned_response:
    #     return jsonify({'response': fine_tuned_response})


if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)

