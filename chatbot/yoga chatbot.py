from flask import Flask, render_template, request, jsonify, url_for
import os

# Initialize Flask app
app = Flask(__name__)

# Define the directory where your asana dataset is stored
asana_directory = 'C:/Users/user/Desktop/Capstone/extracted_files/dataset'

# Function to load asanas from the dataset folder
def load_asanas_from_folder(asana_directory):
    asanas = {}
    for filename in os.listdir(asana_directory):
        if filename.endswith(('.jpg', '.png', '.jpeg')):
            asana_name = os.path.splitext(filename)[0]  # Remove file extension
            asanas[asana_name] = filename  # Store filename to use with static folder path
    return asanas

# Load asanas with image paths from your folder
asanas_in_dataset = load_asanas_from_folder(asana_directory)

# Define the body part to asanas mapping
body_part_to_asanas = {
    "shoulders": ["adho mukha svanasana", "anjaneyasana", "bhujangasana", "garudasana", "chakrasana"],
    "legs": ["uttanasana", "balasana", "virabhadrasana", "padangusthasana", "parsvottanasana", "malasana"],
    "back": ["bhujangasana", "chakrasana", "dhanurasana", "setu bandhaasana", "makarasana", "salabhasana"],
    "core": ["phalakasana", "dandasana", "naukasana", "bhujangasana", "utkatasana", "paripurna navasana"],
    "hips": ["baddha konasana", "garudasana", "malasana", "parivrtta janu sirsasana", "gomukhasana"],
    "arms": ["bakasana", "adho mukha svanasana", "chaturanga dandasana", "vasisthasana", "plank"],
    "neck": ["sarvangasana", "halasana", "setu bandhaasana", "supta baddha konasana", "viparita karani"],
    "ankles": ["virasana", "gomukhasana", "supta virasana", "padmasana", "utkatasana"],
    "spine": ["bhujangasana", "dhanurasana", "marjaryasana", "paschimottanasana", "matsyasana"],
    "chest": ["bhujangasana", "gomukhasana", "urdhva mukha svanasana", "setu bandhaasana", "fish pose"],
    "wrists": ["bakasana", "adho mukha svanasana", "chaturanga dandasana", "plank", "phalakasana"],
    "abdomen": ["phalakasana", "naukasana", "dhanurasana", "pawanmuktasana", "utkatasana", "urdhva dhanurasana"],
    "belly": ["naukasana", "dhanurasana", "phalakasana", "pawanmuktasana", "utkatasana", "paripurna navasana"],
    "thighs": ["uttanasana", "anjaneyasana", "virabhadrasana", "utkatasana", "malasana"],
    "hamstrings": ["parighasana", "janu sirsasana", "parsvottanasana", "paschimottanasana", "padangusthasana"],
}

# Function to find asanas and their images for a given body part
def get_asanas_for_body_part(body_part):
    body_part = body_part.lower()
    if body_part in body_part_to_asanas:
        available_asanas = [
            {'name': asana, 'image': url_for('static', filename=f'dataset/{asanas_in_dataset[asana]}')}
            for asana in body_part_to_asanas[body_part]
            if asana in asanas_in_dataset
        ]
        return available_asanas if available_asanas else f"No asanas found for {body_part}. Try another body part!"
    else:
        return f"Sorry, I don't have any asanas for {body_part}."

@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the user's input and respond with asanas and image paths
@app.route('/get_asanas', methods=['POST'])
def get_asanas():
    body_part = request.form.get('body_part')
    if body_part:
        asanas = get_asanas_for_body_part(body_part)
        return jsonify({'asanas': asanas})
    return jsonify({'asanas': "Please provide a body part."})

if __name__ == '__main__':
    app.run(debug=True)
