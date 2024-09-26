import React, { useState } from 'react';

function ProfilePage({ user }) {
  const [name, setName] = useState(user.name);
  const [height, setHeight] = useState(user.height);
  const [weight, setWeight] = useState(user.weight);

  const updateProfile = (e) => {
    e.preventDefault();
    console.log('Profile updated');
  };

  return (
    <div>
      <h1>Your Profile</h1>
      <form onSubmit={updateProfile}>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="number"
          placeholder="Height"
          value={height}
          onChange={(e) => setHeight(e.target.value)}
        />
        <input
          type="number"
          placeholder="Weight"
          value={weight}
          onChange={(e) => setWeight(e.target.value)}
        />
        <button type="submit">Update Profile</button>
      </form>
    </div>
  );
}

export default ProfilePage;
