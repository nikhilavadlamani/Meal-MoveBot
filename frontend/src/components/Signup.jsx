// frontend/src/components/Signup.jsx

import React, { useState } from 'react';
import './Signup.css'; // Import the CSS for styling
import { useNavigate } from 'react-router-dom';
import axios from 'axios'; // You can use axios to make API calls

const Signup = () => {
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const [signup, setSignup] = useState({
        firstName: '',  // Added firstName field
        lastName: '',   // Added lastName field
        email: '',
        password: '',
        confirmPassword: ''
    });

    const handleChange = (e) => {
        setSignup({
            ...signup,
            [e.target.name]: e.target.value
        });
         
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
          
        if (signup.password !== signup.confirmPassword) {
            setMessage('Passwords do not match.');
            return;
        }

        try {
            // Make API call to backend (e.g., for storing user details)
            const response = await axios.post('http://localhost:5000/signup', {
                firstName: signup.firstName,  // Pass firstName
                lastName: signup.lastName,    // Pass lastName
                email: signup.email,
                password: signup.password,
            });

            // Save the user's email to local storage
            localStorage.setItem('userEmail', signup.email); // Save email

            setMessage('Registration successful! Please log in.');

            // Navigate to the login page after successful registration
            setTimeout(() => {
                navigate('/login');
            }, 3000); // Redirect to login after 3 seconds

        } catch (error) {
            setMessage('An error occurred during registration.');
            console.error("Error signing up:", error);
        }
    };

    return (
        <div className="signup-container">
            <h1>Create your account</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor="first-name" className='textcolor'>First Name</label>
                <input
                    type="text"
                    name="firstName"
                    placeholder="First Name"
                    value={signup.firstName}
                    onChange={handleChange}
                    required
                />
                
                <label htmlFor="last-name" className='textcolor'>Last Name</label>
                <input
                    type="text"
                    name="lastName"
                    placeholder="Last Name"
                    value={signup.lastName}
                    onChange={handleChange}
                    required
                />

                <label htmlFor="email" className='textcolor'>Email address</label>
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={signup.email}
                    onChange={handleChange}
                    required
                />
                
                <label htmlFor="create-password" className='textcolor'>Create Password</label>
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={signup.password}
                    onChange={handleChange}
                    required
                />

                <label htmlFor="confirm-password" className='textcolor'>Re-Enter Password</label>
                <input
                    type="password"
                    name="confirmPassword"
                    placeholder="Re-enter Password"
                    value={signup.confirmPassword}
                    onChange={handleChange}
                    required
                />

                <button type="submit" className="continue-button">Continue</button>
            </form>
            {/* Display message */}
            {message && <p>{message}</p>}

            <div className="login-prompt">
                <p>Already have an account? <a href="/login">Log in</a></p>
            </div>
        </div>
    );
};

export default Signup;
