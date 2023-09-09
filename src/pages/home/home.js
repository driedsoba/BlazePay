import React, { useState } from "react";
import Login from "./login";
import LoggedIn from "./loggedin";
import { useAuthContext } from "../../context/AuthContext";
import { getToken } from "../../helper";

function Home() {
  const { setUser } = useAuthContext();
  const jwt = getToken();

  // const [data, setData] = useState({});

  return <div>{jwt ? <LoggedIn /> : <Login setUserData={setUser} />}</div>;
}

export default Home;
