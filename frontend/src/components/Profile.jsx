import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Profile.css';

const Profile = () => {
    const [favorites, setFavorites] = useState([]);
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const [expandedFavorites, setExpandedFavorites] = useState({});

    // Function to get cookie value from backend
    const fetchCookie = async () => {
        try {
            const response = await fetch('http://localhost:5000/get_cookie', {
                method: 'GET',
                credentials: 'include', // Ensure cookies are included in the request
            });
            const data = await response.json();
            console.log("User email from cookie:", data.user_email);  // Log user email
            if (data.user_email) {
                return data.user_email; // Return user email from the cookie
            } else {
                throw new Error('No user email found in cookie');
            }
        } catch (error) {
            console.error('Error fetching cookie:', error);
            setMessage('Failed to retrieve user email. Please log in again.');
            navigate('/login'); // Redirect to login if cookie is not found
        }
    };

    useEffect(() => {
        const loadFavorites = async () => {
            const userEmail = await fetchCookie(); // Fetch email from cookie
            if (userEmail) {
                fetchFavorites(userEmail); // Proceed to fetch favorites if email exists
            }
        };

        loadFavorites();
    }, [navigate]);

    const fetchFavorites = async (email) => {
        try {
            const response = await axios.get('http://localhost:5000/favorite', {
                params: { email },  // Ensure the email is passed correctly
                withCredentials: true,
            });
            console.log('Favorites response from backend:', response.data);  // Log the response from backendS
    
            if (response.data.favorites && response.data.favorites.length > 0) {
                setFavorites(response.data.favorites);  // Assuming the backend returns a "favorites" array
            } else {
                setMessage('You have no saved favorites.');
            }
        } catch (error) {
            console.error('Error fetching favorites:', error);
            setMessage('Failed to load favorites. Please try again later.');
        } finally {
            setLoading(false);
        }
    };
    console.log("Displaying favorites:", favorites);

    // Toggle expanded view for each favorite
    const toggleExpand = (index) => {
        setExpandedFavorites((prevState) => ({
            ...prevState,
            [index]: !prevState[index],
        }));
    };

    return (
        <div className="profile-container">
            <header className="header">
                <div className="profile">PROFILE</div>
                <div className="button-container">
                    <button onClick={() => navigate('/ProfileSetup')} className="button">Back</button>
                    <button onClick={() => navigate('/')} className="button">SignOut</button>
                </div>
            </header>
            {loading ? (
                <p>Loading favorites...</p>
            ) : (
                <div className="favorites-box">
                    <h4>Your Favorites</h4>
                    {favorites.length > 0 ? (
                        <ul>
                            {favorites.map((item, index) => (
                                <li key={index} className="favorite-item">
                                    <div
                                        className={`favorite-content ${
                                            expandedFavorites[index] ? 'expanded' : ''
                                        }`}
                                        dangerouslySetInnerHTML={{
                                            __html: expandedFavorites[index]
                                                ? item
                                                : item.slice(0, 100) + '...',
                                        }}
                                    />
                                    <button
                                        className="view-more-button"
                                        onClick={() => toggleExpand(index)}
                                    >
                                        {expandedFavorites[index] ? 'View Less' : 'View More'}
                                    </button>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>{message}</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default Profile;