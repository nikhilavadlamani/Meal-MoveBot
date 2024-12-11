import { useEffect, useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Background from './components/Background/Background';
import Navbar from './components/Navbar/Navbar';
import Hero from './components/Hero/Hero';
import Login from './components/Login'; 
import Signup from './components/Signup'; 
import About from './components/About'; 
import Chatbot from './components/Chatbot';
import Yogabot from './components/Yogabot';
import Profile from './components/Profile'; // Adjust the path as necessary
import ProfileSetup from './components/ProfileSetup';


const App = () => {
  let heroData = [
    { text1: "Healthy living starts today", text2: "Discover the perfect balance of meals and moves." },
    { text1: "Start your journey", text2: "Fuel your body, calm your mind." },
    { text1: "Welcome to wellness", text2: "Personalized plans for your body and mind." },
  ];

  const [user, setUser] = useState(null);
  const [heroCount, setHeroCount] = useState(0);
  const [playStatus, setPlayStatus] = useState(false);

  
  // Auth guard for protected routes
  const ProtectedRoute = ({ element }) => {
    const token = localStorage.getItem("authToken");
    return token ? element : <Navigate to="/login" />;
  };
  

  return (
    <BrowserRouter>
      <Routes>
        {/* Define the main layout for all routes */}
        <Route 
          path="/" 
          element={
            <div>
              <Background playStatus={playStatus} heroCount={heroCount} />
              <Navbar />
              <Hero
                setPlayStatus={setPlayStatus}
                heroData={heroData[heroCount]}
                heroCount={heroCount}
                setHeroCount={setHeroCount}
                playStatus={playStatus}
              />
            </div>
          } 
        />
        {/* Define other routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/about" element={<About />} />
        <Route path="/chat" element={<ProtectedRoute element={<Chatbot />} />} />
        <Route path="/yoga" element={<ProtectedRoute element={<Yogabot />} />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/profileSetup" element={<ProfileSetup />} />
        {/* Optional: Redirect to home if no match is found */}
        <Route path="*" element={<Navigate to="/" />} />
        
      </Routes>
    </BrowserRouter>
  );
};

export default App;
