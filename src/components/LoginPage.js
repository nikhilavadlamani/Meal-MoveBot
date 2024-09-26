import React, { useState, useEffect } from 'react';
import { auth } from '../firebase';
import { signInWithEmailAndPassword } from 'firebase/auth';
import './LoginPage.css';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  const images = [
    require('../assets/image1.jpg'),
    require('../assets/image2.jpg'),
    require('../assets/image3.jpg'),
    require('../assets/image4.jpg'),
  ];

  const quotes = [
    "Eat healthy, live healthy.",
    "Fitness is not a destination, it’s a way of life.",
    "Your body is a temple, but only if you treat it as one.",
    "You don’t have to be extreme, just consistent."
  ];

  const [currentQuoteIndex, setCurrentQuoteIndex] = useState(0);

  useEffect(() => {
    const imageInterval = setInterval(() => {
      const nextIndex = ((currentImageIndex - 1 + 1) % (images.length - 1)) + 1;
      setCurrentImageIndex(nextIndex);
    }, 5000); // Change images every 10 seconds

    const quoteInterval = setInterval(() => {
      const nextQuoteIndex = (currentQuoteIndex + 1) % quotes.length;
      setCurrentQuoteIndex(nextQuoteIndex);
    }, 8000); // Change quotes every 8 seconds

    return () => {
      clearInterval(imageInterval);
      clearInterval(quoteInterval);
    };
  }, [currentImageIndex, currentQuoteIndex, images.length, quotes.length]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await signInWithEmailAndPassword(auth, email, password);
      console.log('Login successful');
      // Redirect to another page (e.g., dashboard)
    } catch (err) {
      setError('Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="background-image" />
      <div className="image-carousel">
        {[...Array(3)].map((_, i) => {
          const index = (currentImageIndex + i) % images.length;
          return (
            <img
              key={i}
              src={images[index]}
              alt={`Background ${index}`}
              className={`carousel-image drop-in-${i}`} // Different drop-in animations
            />
          );
        })}
      </div>
      <div className="login-box">
        <h1 className="login-title">Login</h1>
        <form className="login-form" onSubmit={handleLogin}>
          <input
            className="login-input"
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            className="login-input"
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button className="login-button" type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
          {error && <p className="login-error">{error}</p>}
        </form>

        <div className="register-section">
          <p>Don't have an account? <button className="register-button" onClick={() => navigate('/register')}>Register</button></p>
        </div>
      </div>
      <div className="quote-overlay">
        <p>{quotes[currentQuoteIndex]}</p>
      </div>
    </div>
  );
}

export default LoginPage;
