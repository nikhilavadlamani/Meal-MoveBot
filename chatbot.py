from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import pandas as pd
import re

# Load the dataset with the 'TranslatedInstructions' column
data = pd.read_csv('data.csv')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load conversational model
text_generator = pipeline("text2text-generation", model="facebook/bart-large")

# Dictionary to hold user-selected recipe state and preferences
user_state = {}

# Function to filter meal plans based on cooking time, cuisine, ingredient, and recipe name
def get_meal_plan(max_time_in_minutes=None, cuisine=None, ingredient=None, recipe_name=None):
    filtered_recipes = data

    # Filter by cooking time
    if max_time_in_minutes:
        filtered_recipes = filtered_recipes[filtered_recipes['TotalTimeInMins'] <= max_time_in_minutes]

    # Filter by cuisine
    if cuisine:
        filtered_recipes = filtered_recipes[filtered_recipes['Cuisine'].str.contains(cuisine, case=False)]

    # Filter by ingredient
    if ingredient:
        filtered_recipes = filtered_recipes[filtered_recipes['Cleaned-Ingredients'].str.contains(ingredient, case=False)]

    # Filter by recipe name
    if recipe_name:
        filtered_recipes = filtered_recipes[filtered_recipes['TranslatedRecipeName'].str.contains(recipe_name, case=False)]

    # Limit the results to a manageable number (e.g., 10 recipes)
    meal_plan = filtered_recipes[['TranslatedRecipeName', 'URL', 'image-url', 'Cleaned-Ingredients', 'TranslatedInstructions']].head(10).to_dict(orient='records')
    return meal_plan

# Function to interpret user query and extract relevant information
def parse_user_query(user_message):
    # Extract time (in minutes) from the user message
    time_match = re.search(r'(\d+)\s*minutes?', user_message.lower())
    max_time = int(time_match.group(1)) if time_match else None

    # Extract potential cuisine
    cuisine_match = re.search(r'(indian|south indian|andhra|chinese|italian|mexican)', user_message.lower())
    cuisine = cuisine_match.group(1) if cuisine_match else None

    # Extract potential ingredients
    ingredient_match = re.search(r'with (\w+)', user_message.lower())
    ingredient = ingredient_match.group(1) if ingredient_match else None

    # Extract recipe name (if mentioned)
    recipe_match = re.search(r'(\w+)\s*recipe', user_message.lower())
    recipe_name = recipe_match.group(1) if recipe_match else None

    return max_time, cuisine, ingredient, recipe_name

# Function to process and respond to user queries
def process_user_request(user_message):
    # Handle casual conversation with explicit conditions
    if 'hello' in user_message.lower():
        return "Hello! How can I assist you today?"
    if 'how are you' in user_message.lower():
        return "I'm doing great! How about you?"

    # Parse the user's message to extract time, cuisine, ingredient, and recipe name preferences
    max_time, cuisine, ingredient, recipe_name = parse_user_query(user_message)

    # If the user is searching for a specific recipe
    if recipe_name:
        meal_plan = get_meal_plan(recipe_name=recipe_name)
        if meal_plan:
            selected_recipe = meal_plan[0]  # Return the first matching recipe (assumed unique)
            response = f"<strong>Here is the recipe for </strong>{selected_recipe['TranslatedRecipeName']}<br>"
            response += f"<strong>Ingredients:</strong> {selected_recipe['Cleaned-Ingredients']}<br>"
            response += f"<strong>Procedure:</strong> {selected_recipe['TranslatedInstructions']}<br>"
            response += f"<strong>Need more info?:</strong> <a href='{selected_recipe['URL']}' target='_blank'>{selected_recipe['URL']}</a><br>"
            response += f"<img src='{selected_recipe['image-url']}' alt='Recipe Image' width='200'><br>"
            return response
        else:
            return "Sorry, I couldn't find that recipe."

    # Get meal plan based on parsed data (for general queries)
    meal_plan = get_meal_plan(max_time, cuisine, ingredient)
    if meal_plan:
        user_state['meal_plan'] = meal_plan
        # Format the meal plan to be displayed with buttons
        response = "Here are some meal options:\n"
        for idx, recipe in enumerate(meal_plan):
            response += f"<button>{idx + 1}. {recipe['TranslatedRecipeName']}</button><br>"
        response += "\nPlease select a recipe by clicking a button or let me know if you prefer a different cuisine or ingredient."
        return response
    else:
        return f"Sorry, no recipes found for your preferences."

# Handle selected recipe
def handle_recipe_selection(user_message):
    if user_message.isdigit() and 'meal_plan' in user_state:
        selected_idx = int(user_message) - 1
        if 0 <= selected_idx < len(user_state['meal_plan']):
            selected_recipe = user_state['meal_plan'][selected_idx]
            # Display the selected recipe's ingredients, instructions, URL, and image
            response = f"<strong>Ok, good choice! Here's the recipe for </strong>{selected_recipe['TranslatedRecipeName']}<br>"
            response += f"<strong>Ingredients: </strong>{selected_recipe['Cleaned-Ingredients']}<br>"
            response += f"<strong>Procedure: </strong>{selected_recipe['TranslatedInstructions']}<br>"
            response += f"<strong>Need more info?: </strong><a href='{selected_recipe['URL']}' target='_blank'>{selected_recipe['URL']}</a><br>"
            response += f"<img src='</strong>{selected_recipe['image-url']}' alt='Recipe Image' width='200'><br>"
            return response
        else:
            return "Invalid selection. Please select a valid recipe number."
    else:
        return "Sorry, I didn't understand that."

# Flask route to handle chat
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')

    if user_input.isdigit():
        # Handle recipe selection
        bot_reply = handle_recipe_selection(user_input)
    else:
        # Handle user query
        bot_reply = process_user_request(user_input)

    return jsonify({'response': bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
