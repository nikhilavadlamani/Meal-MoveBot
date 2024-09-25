import React from 'react'

const Login = () => {
    const [login,setLogin] = React.useState({
        email:"",
        password:""
    })
    const handleChange=(e)=>{
        setLogin({
            ...login,
            [e.target.name]:e.target.value
        })
    }
    console.log(login)
  return (
    <div className="bg-red-600">
        <form className='flex bg-red-600'>
            <label htmlFor='email'>
                Enter your Email
            </label>
            <input name="email" placeholder='Email' value={login.email} onChange={handleChange}/>
            <label htmlFor="password">Enter Your Password</label>
            <input name="password" placeholder='Password' value={login.password} onChange={handleChange}/>
        </form>
    </div>
  )
}

export default Login