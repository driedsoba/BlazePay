import React, { useState } from "react";
import Login from "./login";
import LoggedIn from "./loggedin";
import { useAuthContext } from "../../context/AuthContext";

function Home() {
  const { jwt, setJWT } = useAuthContext();
  const [data, setData] = useState({});

  return <div>{jwt ? <LoggedIn /> : <Login setIsLoggedIn={setJWT} />}</div>;
}

export default Home;
