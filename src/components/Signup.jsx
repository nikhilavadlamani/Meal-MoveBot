import React from 'react'

const Signup = () => {
    const [signup,setSignup] = useState({
        email:"",
        password:""
    })
    const handleChange = (e)=>{
        setSignup({
            ...signup,
            [e.target.name]:e.target.value
        })
    }
    const handleSubmit=(e)=>{
        e.preventDefault()
    }
  return (
    <div>
        <form>
            <input name="email" placeholder='email' onChange={handleChange} />
            <input name="password" placeholder='password' onChange={handleChange} />
        </form>
    </div>
  )
}

export default Signup