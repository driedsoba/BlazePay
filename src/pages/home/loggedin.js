import React, { useState } from "react";
import { useAuthContext } from "../../context/AuthContext";

function LoggedIn() {
  const { jwt, setJWT, setUser, user } = useAuthContext();
  return (
    <div>
      <h2 style={{ color: "black", fontFamily: "Oxygen" }}>
        Welcome, {user?.name}!
      </h2>
      <h2 style={{ color: "black", fontFamily: "Oxygen" }}>{user?.email}</h2>
      Logged In!
    </div>
  );
}

export default LoggedIn;
