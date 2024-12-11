import React, { memo } from 'react';
import { useNavigate } from 'react-router-dom'; // for navigation functionality
import './Yogabot.css'; // Import the CSS file for styling
import { getCookie } from './utils.js';

// Now you can use getCookie() wherever you need to get a cookie

const Chatgpt = () => {
  const navigate = useNavigate();  // useNavigate hook from react-router-dom for navigation

  const handleProfileClick = () => {
    navigate('/profile');  // Navigates to the profile page
  };

  const handleSignOutClick = () => {
    navigate('/');  // Navigates to the home page or log out page
  };

  const handleChatClick = () => {
    navigate('/ProfileSetup');  // Navigates to the home page or log out page
  };

  return (
    <div className='body'>
      {/* Header with left-side welcome text and right-side buttons */}
      <header className="header">
        <div className="welcome-message">Welcome - Chat with us!</div>
        <div className="button-container">
        <button onClick={handleChatClick} className="button">Back</button>
          <button onClick={handleProfileClick} className="button">Profile</button>
          <button onClick={handleSignOutClick} className="button">SignOut</button>
        </div>
      </header>

      {/* Chatbot iframe */}
      <iframe
        src="http://localhost:5000/yogabot"  // URL where your Flask app serves the HTML
        title="Yogabot"
      />
    </div>
  );
};

export default memo(Chatgpt);
