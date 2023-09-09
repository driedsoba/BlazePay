import React, { useState, useEffect } from "react";
import MyContext from "./MyContext";
import Bank from "./Bank";
import { useAuthContext } from "../../context/AuthContext";
import { getToken } from "../../helper";

const style = {
  background: "lightblue",
  color: "black",
  padding: "0.1rem",
  display: "flex",
  width: 100,
  alignitems: "center",
};

const amountStyle = {
  color: "green",
};

function Wallet() {
  const { setUser, user, refreshData } = useAuthContext();
  const jwt = getToken();
  const [phone, setPhone] = useState("");
  const [transferAmount, setTransferAmount] = useState("");
  const [addMoneyAmount, setAddMoneyAmount] = useState("");
  // const [balance, setBalance] = useState(1000);
  const [errorMessage, setErrorMessage] = useState("");
  const [transferComplete, setTransferComplete] = useState(false);

  const handleTransfer = async () => {
    try {
      const response = await fetch("http://localhost:8000/payment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwt}`,
        },
        body: JSON.stringify({
          receiver: phone,
          amount: parseInt(transferAmount),
          currency: "SGD",
        }),
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      // Handle the response as needed
      const responseData = await response.json();
      // setJWT(responseData["access_token"]);
      // setUserData(responseData["user_data"]);
      console.log("Response from server:", responseData);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleTopUp = async () => {
    try {
      const response = await fetch("http://localhost:8000/topUp", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${jwt}`,
        },
        body: JSON.stringify({
          amount: parseInt(addMoneyAmount),
          currency: "SGD",
        }),
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      // Handle the response as needed
      const responseData = await response.json();
      // setJWT(responseData["access_token"]);
      // setUserData(responseData["user_data"]);

      console.log("Response from server:", responseData);
      window.location.replace(responseData["stripe_url"]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    if (transferComplete) {
      const timer = setTimeout(() => {
        setTransferComplete(false);
        refreshData();
      }, 2000); // 2 seconds in milliseconds

      return () => clearTimeout(timer);
    }
  }, [transferComplete]);

  useEffect(() => {
    refreshData();
  }, []);

  const handleTransaction = (transactionAmount) => {
    if (transactionAmount <= 0) {
      setErrorMessage("Amount must be greater than zero.");
    } else if (transactionAmount > user?.balance.SGD) {
      setErrorMessage("Insufficient balance.");
    } else {
      setErrorMessage("");
      handleTransfer();
      setTransferComplete(true);
    }
  };

  const handleAddMoney = (moneyAmount) => {
    if (moneyAmount <= 0) {
      setErrorMessage("Amount must be greater than zero.");
    } else {
      setErrorMessage("");
      handleTopUp();
    }
  };

  // const updateBalance = (amount) => {
  //   setBalance((prevBalance) => prevBalance + amount);
  // };

  const handleInputChange = (e, type) => {
    const value = e.target.value;
    if (type === "transfer") {
      setTransferAmount(value);
    } else if (type === "addMoney") {
      setAddMoneyAmount(value);
    } else if (type === "phone") {
      setPhone(value);
    }
  };

  return (
    <MyContext.Provider
      value={{
        transferAmount,
        amountStyle,
        handleTransaction,
      }}
    >
      <div>
        <div>
          <div className="sign-up-container">
            <h1 style={{ color: "black", fontFamily: "Oxygen" }}>
              Payment Status
            </h1>
            <h2 style={{ color: "black", fontFamily: "Segoe Bold" }}>Wallet</h2>
            <div className="Wallet" style={style}>
              <div className="Balance">Balance: {user?.balance.SGD} SGD</div>
            </div>
            <a>&nbsp;</a>

            <label>
              <a style={{ color: "#4760c2" }}>Transfer To:&nbsp;</a>
              <input
                type="number"
                placeholder="Phone Number"
                value={phone}
                onChange={(e) => handleInputChange(e, "phone")}
              />
            </label>
            <a>&nbsp;</a>

            <label>
              <a style={{ color: "#4760c2" }}>Transfer Amount:&nbsp;</a>
              <input
                type="number"
                placeholder="100"
                value={transferAmount}
                onChange={(e) => handleInputChange(e, "transfer")}
              />
            </label>
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
              onClick={() => handleTransaction(parseInt(transferAmount))}
              disabled={!transferAmount || parseInt(transferAmount) <= 0}
            >
              Transfer
            </button>

            {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
            {transferComplete && (
              <p style={{ color: "green" }}>
                Transfered {parseInt(transferAmount)} from Wallet!
              </p>
            )}
          </div>
        </div>

        <div>
          <div className="sign-up-container">
            <label>
              <a style={{ color: "#4760c2" }}>Add Money:&nbsp;</a>
              <input
                type="number"
                placeholder="100"
                value={addMoneyAmount}
                onChange={(e) => handleInputChange(e, "addMoney")}
              />
            </label>
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
              onClick={() => handleAddMoney(parseInt(addMoneyAmount))}
              disabled={!addMoneyAmount || parseInt(addMoneyAmount) <= 0}
            >
              Add
            </button>
          </div>
        </div>
        <Bank />
      </div>
    </MyContext.Provider>
  );
}

export default Wallet;
