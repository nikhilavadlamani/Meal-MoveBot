import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import {onAuthStateChanged} from "firebase/auth"
import ContextProvider from "./context/context";
import "./App.css";
import Login from "./components/Login";
import Signup from "./components/Signup";
import { auth } from "./firebase/firebase";
import Home from "./components/Home";


function App() {
  const [user,setUser]= React.useState()
  React.useEffect(()=>{
    onAuthStateChanged(auth,user=>{
      setUser(user.uid)
    })
  },[])
  console.log("user",user)
  return (
    <>
      <ContextProvider>
        <Router>
          <Routes>
            <Route path="/login" Component={Login} />
            <Route path="/signup" Component={Signup} />
            <Route path="/home" Component={Home} />
          </Routes>
        </Router>
      </ContextProvider>
    </>
  );
}

export default App;
