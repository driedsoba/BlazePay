import React, { useState } from 'react';
import Login from './login';
import LoggedIn from './loggedin';

function Home() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [data, setData]=useState({})

  return (
    <div>
        {isLoggedIn ? (
            <LoggedIn />
        ) : (
            <Login setIsLoggedIn={{setIsLoggedIn}}/>
        )}
    </div>
  );
}

export default Home;