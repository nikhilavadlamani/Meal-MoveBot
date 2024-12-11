import React from 'react';
import './About.css'; // Import the CSS for styling

const About = () => {
    return (
        <div className="about-container">
            <h1>About Meal-Move-Bot</h1>
            <p>
                This application helps you create individualized meal suggestions and yoga routines based on your health objectives, dietary preferences, and fitness capabilities.
                <br /><br />
                The Meal & Move Bot is an interactive application designed to help users maintain a healthy lifestyle by offering personalized meal plans and yoga routines through an intuitive chatbot interface. Users can sign up, log in, and access a variety of meal and workout recommendations tailored to their needs. The chatbot provides recipe suggestions based on user preferences, such as ingredients, cuisine, and preparation time, leveraging the Spoonacular API for diverse meal options. Each recipe displays detailed information, including ingredients, procedure, and an accompanying image and URL. Users can mark their favorite meals with a star icon, which saves them to a personal profile page for easy access later.
                <br /><br />
                In addition to meal planning, the bot is being developed to offer customized yoga routines, which users can also save as favorites. The app’s design focuses on accessibility and user convenience, allowing individuals to quickly find and bookmark their preferred meal plans and routines. This personalization is achieved through fine-tuned models that adjust recommendations based on user interactions, making the Meal & Move Bot a helpful companion for anyone looking to improve their wellness with minimal effort.
            </p>
        </div>
    );
};

export default About;
