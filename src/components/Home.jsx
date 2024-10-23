import React, { useState, useContext } from "react";
import { Context } from "../context/context";
import { update_profile, onLogout } from "../context/middleware";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../firebase/firebase";
import { useNavigate } from "react-router-dom";
const Home = () => {
  const navigate = useNavigate();
  const [details, setDetails] = useState({
    username: "",
    age: "",
    gender: "",
    height: "",
    weight: "",
    fitness_level: "",
    dietary_preferance: "",
    allergies_restrictions: "",
    health_goals: "",
  });

  const [user, setUser] = React.useState();
  React.useEffect(() => {
    onAuthStateChanged(auth, (user) => {
      setUser(user.uid);
      if (user === undefined) {
        navigate("/login");
      }
    });
  }, []);

  const handleChange = (e) => {
    setDetails({
      ...details,
      [e.target.name]: e.target.value,
    });
  };

  const [state, dispatch] = useContext(Context);

  const setState = (obj) => {
    dispatch({
      type: "SET_STATE",
      payload: obj,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("here");
    update_profile(details, user)(setState, state);
  };

  const handleLogout = () => {
    onLogout()(setState, state);
    navigate("/login");
  };

  return (
    <div>
      <button
        className="text-white bg-red-700 hover:bg-red-800 focus:outline-none focus:ring-4 focus:ring-red-300 font-medium rounded-full text-sm px-5 py-2.5 text-center me-2 mb-2 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-900"
        onClick={handleLogout}
      >
        Logout
      </button>
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-400 via-blue-500 to-green-400">
        {/* Form Wrapper */}

        <div className="w-full max-w-lg bg-white rounded-lg shadow-xl dark:border dark:bg-gray-800 dark:border-gray-700 p-6 space-y-6">
          <h1 className="text-2xl font-bold leading-tight tracking-tight text-gray-900 dark:text-white text-center">
            User Profile
          </h1>
          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label
                htmlFor="username"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Your Username
              </label>
              <input
                type="text"
                name="username"
                id="username"
                onChange={handleChange}
                className="bg-gray-100 border border-gray-300 text-gray-900 rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
                required
                placeholder="Enter username"
              />
            </div>

            <div>
              <label
                htmlFor="age"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Your Age
              </label>
              <input
                type="number"
                name="age"
                id="age"
                onChange={handleChange}
                className="bg-gray-100 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
                placeholder="Enter age"
              />
            </div>

            <div>
              <label
                htmlFor="gender"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Select Your Gender
              </label>
              <select
                id="gender"
                name="gender"
                onChange={handleChange}
                className="bg-gray-100 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-purple-500 focus:border-purple-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-purple-500 dark:focus:border-purple-500"
              >
                <option value="" disabled selected>
                  Choose Gender
                </option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="rnts">Rather not to say</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="weight"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Your Weight
              </label>
              <input
                type="number"
                name="weight"
                id="weight"
                onChange={handleChange}
                className="bg-gray-100 border border-gray-300 text-gray-900 rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
                required
                placeholder="Enter weight"
              />
            </div>

            <div>
              <label
                htmlFor="height"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Your Height
              </label>
              <input
                type="number"
                name="height"
                id="height"
                onChange={handleChange}
                className="bg-gray-100 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
                placeholder="Enter height"
              />
            </div>

            <div>
              <label
                htmlFor="fitness_level"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Select Your Fitness Level
              </label>
              <select
                id="fitness_level"
                name="fitness_level"
                onChange={handleChange}
                className="bg-gray-100 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-purple-500 focus:border-purple-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-purple-500 dark:focus:border-purple-500"
              >
                <option value="" disabled selected>
                  Select your fitness level
                </option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
                <option value="Expert">Expert</option>
                <option value="Active">Active</option>
                <option value="Very Active">Very Active</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="dietary_preferance"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Select Your Dietary Preference
              </label>
              <select
                id="dietary_preferance"
                name="dietary_preferance"
                onChange={handleChange}
                className="bg-gray-100 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-green-500 focus:border-green-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-green-500 dark:focus:border-green-500"
              >
                <option value="" disabled selected>
                  Select your Dietary Preference
                </option>
                <option value="Omnivore">Omnivore</option>
                <option value="Vegetarian">Vegetarian</option>
                <option value="Vegan">Vegan</option>
                <option value="Pescatarian">Pescatarian</option>
                <option value="Gluten-Free">Gluten-Free</option>
                <option value="Low-Fat">Low-Fat</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="allergies_restrictions"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Your Allergies or Dietary Restrictions
              </label>
              <textarea
                name="allergies_restrictions"
                id="allergies_restrictions"
                rows="5"
                onChange={handleChange}
                className="bg-gray-100 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                required
                placeholder="Enter any allergies or dietary restrictions"
              />
            </div>
            <div>
              <button
                onClick={handleSubmit}
                type="button"
                class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
              >
                Update Profile
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Home;
