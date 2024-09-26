import {auth,firestore} from "../firebase/firebase"
import {signInWithEmailAndPassword} from "firebase/auth"

export const onLogin=(email,password)=>async(setState,state)=>{
    setState({
        ...state.login,
        error:{},
        user:{},
        isLoggedIn:false
    })
    try{
        const login =  await signInWithEmailAndPassword(auth,email,password)
        localStorage.setItem("user",login.user.uid)
    }catch(error){
        setState({
            ...state.login,
            error:{
                error
            },
            isLoggedIn:false
        })
    }
}

export const onSignup=(email,password)=>(setState,state)=>{
    setState({
        ...state.signup,

    })
}