import React, { useState } from "react";
import { getToken, setToken } from "../../helper";
import { useAuthContext } from "../../context/AuthContext";

function Login({ setUserData }) {
  // const { setUserData } = useAuthContext();
  const [data, setData] = useState({
    phone: "",
    pin: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://localhost:8000/profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      // Handle the response as needed
      const responseData = await response.json();
      setToken(responseData["access_token"]);
      setUserData(responseData["user_data"]);
      console.log("Response from server:", responseData);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div>
      <div className="sign-up-container">
        <h1 style={{ color: "black", fontFamily: "Oxygen" }}> Log In!</h1>
        <a style={{ color: "#4760c2" }}>Phone Number</a>
        <input
          style={{
            backgroundColor: "#e5f3f7",
            color: "black",
            width: 200,
          }}
          type="number"
          name="phone"
          value={data.phone}
          onChange={handleChange}
          placeholder="Phone No."
        />

        <a>&nbsp;&nbsp;</a>

        <div className="sign-up-container">
          <a style={{ color: "#4760c2" }}>Pin</a>
          <input
            style={{
              backgroundColor: "#e5f3f7",
              color: "black",
              width: 200,
            }}
            type="password"
            name="pin"
            value={data.pin}
            onChange={handleChange}
            placeholder="Password"
          />
        </div>

        <div>&nbsp;</div>

        <button
          style={{
            backgroundColor: "#4760c2",
            color: "white",
            borderColor: "white",
            borderTopLeftRadius: 35,
            borderTopRightRadius: 35,
            borderBottomLeftRadius: 35,
            borderBottomRightRadius: 35,
            width: 150,
          }}
          onClick={handleSubmit}
        >
          Submit
        </button>
      </div>
    </div>
  );
}

export default Login;
