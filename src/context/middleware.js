import { auth, db } from "../firebase/firebase";
import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
} from "firebase/auth";
import { collection, addDoc } from "firebase/firestore";
import { redirect } from "react-router-dom";

export const onLogin = (email, password) => async (setState, state) => {
  setState({
    ...state.login,
    error: {},
    user: {},
    isLoggedIn: true,
  });
  try {
    console.log("Here too");
    const login = await signInWithEmailAndPassword(auth, email, password);
    localStorage.setItem("user", login.user.uid);
    setState({
      ...state.user,
      error: {},
      user: login.user.toJSON(),
      isLoading: false,
    });
    redirect("/home");
  } catch (error) {
    console.log(error);
    setState({
      ...state.login,
      error: {
        error,
      },
      isLoggedIn: false,
    });
  }
};

export const onSignup = (email, password) => async (setState, state) => {
  console.log("====================================");
  console.log("Here");
  console.log("====================================");
  setState({
    ...state.signup,
    error: {},
    isLoading: true,
    user: {},
  });
  try {
    const signup = await createUserWithEmailAndPassword(auth, email, password);
    console.log("Here too", signup);
    setState({
      ...state.signup,
      error: {},
      isLoading: false,
      user: signup.user.toJSON(),
    });
    const docData = {
      email,
      uid: signup.user.uid,
    };
    const docRef = await addDoc(collection(db, "users"), {
      ...docData,
    });
    console.log("Doc id ", docRef.id);

    localStorage.setItem("user", signup.user.uid);
  } catch (error) {
    console.log(error);
    setState({
      ...state.signup,
      error: {
        error,
      },
      isLoggedIn: false,
      user: {},
    });
  }
};

export const onLogout = () => async (setState, state) => {
  try {
    const logout = await signOut(auth);
    console.log("logout success");
  } catch (error) {
    console.log(error);
  }
};

export const update_profile =
  (profile_data, user_id) => async (setState, state) => {
    setState({
      ...state.profile,
      error: {},
      isLoading: true,
      profile_data: {},
    });
    try {
      const {
        username,
        age,
        gender,
        height,
        weight,
        fitness_level,
        dietary_preferance,
        allergies_restrictions,
        health_goals,
      } = profile_data;
      console.log(profile_data);
      const doc_data = {
        ...profile_data,
        update_at: new Date().toLocaleDateString(),
      };
      const docRef = await addDoc(collection(db, "user_profile"), {
        ...doc_data,
      });
      console.log(docRef.id);
      setState({
        ...state.profile,
        error: {},
        isLoading: false,
        profile_data: docRef.id,
      });
    } catch (error) {
      setState({
        ...state.profile,
        error: error,
        isLoading: false,
        profile_data: {},
      });
    }
  };
