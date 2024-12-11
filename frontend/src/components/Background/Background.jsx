import './Background.css'
import vedio2 from '../../assets/vedio2.mp4'
import image1 from '../../assets/yoga1.jpg'
import image2 from '../../assets/image2.jpg'
import image4 from '../../assets/image4.jpg'
import mealyoga12 from '../../assets/mealyoga12.jpg'

const Background= ({playStatus, heroCount}) => {

    if(playStatus){
        return(
            <video className='background fade-in' autoPlay loop muted>
                <source src={vedio2} type='vedio/mp4' />
            </video>
        )
    }
    else if(heroCount==0)
    {
        return <img src={image1} className='background fade-in' alt="" />
    }
    else if(heroCount==1)
    {
        return <img src={image2} className='background fade-in' alt="" />
    }
    else if(heroCount==2)
    {
        return <img src={image4} className='background fade-in' alt="" />
    }
    else if(heroCount==3)
    {
        return <img src={mealyoga12} className='background fade-in' alt="" />
    }   
}

export default Background