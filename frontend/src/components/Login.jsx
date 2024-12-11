import React, { useState } from 'react';
import './Login.css'; // Import the CSS for styling
import { useNavigate } from 'react-router-dom';
//import { getCookie } from './utils.js';
// Now you can use getCookie() wherever you need to get a cookie
import axios from 'axios'; // Import axios for making API calls

const Login = () => {
    const navigate = useNavigate();
    const [login, setLogin] = useState({
        email: "",
        password: ""
    });
    const [message, setMessage] = useState(''); // To store error messages

    const handleChange = (e) => {
        setLogin({
            ...login,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Authenticate user with email and password
            const response = await axios.post('http://localhost:5000/login', {
                email: login.email,
                password: login.password,
            }, { withCredentials: true }); // Ensure cookies are included

            // Assuming the token is in response.data.token
            const token = response.data.token;
            const userEmail = login.email;
            
            console.log("User email saved in localStorage:", localStorage.getItem('userEmail'));

            // Save the token in localStorage
            localStorage.setItem('authToken', token);
            localStorage.setItem('userEmail', userEmail);
            // Navigate to the Chatbot page on success
            navigate("/profileSetup");
        } catch (error) {
            // Handle errors (e.g., invalid email, wrong password)
            setMessage('Invalid email or password. Please try again.');
            console.error("Error signing in:", error);
        }
    };

    return (
        <div className="login-container">
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <label htmlFor='email'>Email address</label>
                <input
                    type="email"
                    name="email"
                    placeholder='Email'
                    value={login.email}
                    onChange={handleChange}
                    autoComplete="username"
                    required
                />
                <label htmlFor="password">Password</label>
                <input
                    type="password"
                    name="password"
                    placeholder='Password'
                    value={login.password}
                    onChange={handleChange}
                    autoComplete="current-password"
                    required
                />
                <button type="submit" className="continue-button">Continue</button>
            </form>

            {/* Display error message */}
            {message && <p className="error-message">{message}</p>}

            <div className="signup-prompt">
                <p>Don't have an account? <a href="/signup">Sign up</a></p>
            </div>
        </div>
    );
};

export default Login;
