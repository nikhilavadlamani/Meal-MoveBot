import React, { memo } from 'react';
import { useNavigate } from 'react-router-dom';
import './ProfileSetup.css';

// Import the images
import image1 from '../assets/meal4.jpg';
import image2 from '../assets/image4.jpg';

const ProfileSetup = () => {
  const navigate = useNavigate();

  const handleProfileClick = () => {
    navigate('/profile');
  };

  const handleSignOutClick = () => {
    navigate('/');
  };

  const handleImage1Click = () => {
    navigate('/chat');
  };

  const handleImage2Click = () => {
    navigate('/yoga');
  };

  return (
    <div className="profile-setup-body">
      <header className="profile-setup-header">
        <div className="header-text">Welcome to Meal-Move Bot</div>
        <div className="button-container">
          
          <button onClick={handleProfileClick} className="button">Profile</button>
          <button onClick={handleSignOutClick} className="button">SignOut</button>
        </div>
      </header>

      <div className="images-container">
        <div className="image-wrapper">
          <img
            src={image1} // Use imported image
            alt="Image 1"
            className="clickable-image"
            onClick={handleImage1Click}
          />
          <p className="bold-black-text">Meal Bot</p>
        </div>
        <div className="image-wrapper">
          <img
            src={image2} // Use imported image
            alt="Image 2"
            className="clickable-image"
            onClick={handleImage2Click}
          />
          <p className="bold-black-text">Yoga Bot</p>
        </div>
      </div>
    </div>
  );
};

export default memo(ProfileSetup);
