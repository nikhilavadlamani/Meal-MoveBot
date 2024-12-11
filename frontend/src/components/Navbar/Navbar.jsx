import { useNavigate } from 'react-router-dom';
import './Navbar.css';


const Navbar = () => {
    const navigate = useNavigate(); // Hook for navigation

    // Define the click handler
    const handleClick = (path) => {
        navigate(path); // Navigate to the specified path
    };


    return (
        <div className='nav'>
            <div className='nav-logo'>Meal-Move-Bot</div>
            <ul className='nav-menu'>
                
                <li onClick={() => handleClick('/login')}>Login</li>
                <li onClick={() => handleClick('/signup')}>Signup</li>
                <li onClick={() => handleClick('/about')}>About</li>
                
            </ul>
        </div>
    );
}

export default Navbar;
