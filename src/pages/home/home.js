import React, { useState } from 'react';
import Login from './login';
import LoggedIn from './loggedin';

function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState({
    phone: '',
    phoneNumber: '',
  });

  return (
    <div>
        {isLoggedIn ? (
            <Login />
        ) : (
            <LoggedIn />
        )}
</div>
  );
}

export default Home;