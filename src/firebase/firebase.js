import {initializeApp} from "firebase/app"
import { getAuth} from "firebase/auth";

import {getFirestore} from "firebase/firestore"
const firebaseConfig = {
    apiKey: "AIzaSyBx7KQLto-ofYFRSTt5RWF8QpDepwdfYks",
    authDomain: "capstone-57a30.firebaseapp.com",
    projectId: "capstone-57a30",
    storageBucket: "capstone-57a30.appspot.com",
    messagingSenderId: "195749402955",
    appId: "1:195749402955:web:62c75ce1fb8cb6215430ce"
  };


  const app = initializeApp(firebaseConfig);

  const auth = getAuth(app)

  

  const firestore = getFirestore(app)


  export default {auth,firestore}

