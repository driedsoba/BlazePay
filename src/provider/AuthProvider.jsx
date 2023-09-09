//Stores and provides the data defined by AuthContext to all the components below it

import React, { useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { getToken, removeToken } from "../helper";

const AuthProvider = ({ children }) => {
  const [userData, setUserData] = useState();

  const [isLoading, setIsLoading] = useState(false);

  const handleUser = (user) => {
    setUserData(user);
  };

  const refreshData = async () => {
    const jwt = getToken();
    try {
      const response = await fetch("http://localhost:8000/data", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwt}`,
        },
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      // Handle the response as needed
      const responseData = await response.json();
      setUserData(responseData["user_data"]);
      console.log("Response from server:", responseData);
    } catch (error) {
      console.error("Error:", error);
      removeToken();
      window.location.replace("http://localhost:3000/home");
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user: userData,
        setUser: handleUser,
        refreshData: refreshData,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
