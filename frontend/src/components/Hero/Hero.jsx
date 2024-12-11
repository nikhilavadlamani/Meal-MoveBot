
import { useNavigate } from 'react-router-dom';
import './Hero.css'
import up_button from '../../assets/up_button.jpg'
//import pause_button from '../../assets/pause_button.jpg'
//import play_button from '../../assets/play_button.jpg'

const Hero =({heroData, setHeroCount, heroCount, setPlayStatus, playStatus}) => {

    const navigate = useNavigate(); // Initialize useNavigate hook

    const handleNavigate = () => {
        navigate('/login'); // Navigate to the login page
    };
    return(
        <div className='hero'>
            <div className='hero-text'>
                <p>{heroData.text1}</p>
                <p>{heroData.text2}</p>

            </div>
            <div className='hero-explore' onClick={handleNavigate}>
                <p>Click Here</p>
                <img src={up_button} alt="" />
            </div>

            
            
        </div>
    )

}
  
export default Hero