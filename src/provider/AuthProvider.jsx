//Stores and provides the data defined by AuthContext to all the components below it

import React, { useState } from "react";
import { AuthContext } from "../context/AuthContext";

const AuthProvider = ({ children }) => {
  const [userData, setUserData] = useState();
  const [jwt, setJWT] = useState();
  const [isLoading, setIsLoading] = useState(false);

  const handleUser = (user) => {
    setUserData(user);
  };

  const handleJWT = (user) => {
    setJWT(user);
  };

  return (
    <AuthContext.Provider
      value={{
        user: userData,
        setUser: handleUser,
        jwt: jwt,
        setJWT: handleJWT,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
