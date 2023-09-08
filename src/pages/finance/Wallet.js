import React, { useState, useEffect } from "react";
import Balance from "./Balance";
import MyContext from "./MyContext";
import Bank from "./Bank";

const style = {
  background: "green",
  color: "white",
  padding: "0.5rem",
  display: "flex",
};

const amountStyle = {
  color: "green",
};

function Wallet() {
  const [amount, setAmount] = useState(""); 
  const [balance, setBalance] = useState(1000); 
  const [errorMessage, setErrorMessage] = useState("");
  const [transferComplete, setTransferComplete] = useState(false);

  useEffect(() => {
    if (transferComplete) {
      const timer = setTimeout(() => {
        setTransferComplete(false);
      }, 3000); // 4 seconds in milliseconds

      return () => clearTimeout(timer);
    }
  }, [transferComplete]);

  const handleTransaction = (transactionAmount) => {
    if (transactionAmount <= 0) {
      setErrorMessage("Amount must be greater than zero.");
    } else if (transactionAmount > balance) {
      setErrorMessage("Insufficient balance.");
    } else {
      setErrorMessage("");
      updateBalance(-transactionAmount);
      setTransferComplete(true);
    }
  };

  const updateBalance = (amount) => {
    setBalance((prevBalance) => prevBalance + amount);
  };

  const handleAmountChange = (e) => {
    setAmount(e.target.value);
  };

  return (
    <MyContext.Provider
      value={{
        amount,
        balance,
        amountStyle,
        handleTransaction,
      }}
    >
      <div>
        <div className="Wallet" style={style}>
          <Balance />
        </div>
        <h2>Wallet</h2>
        <div>
          <label>
            Transfer Amount:
            <input
              type="number"
              value={amount}
              onChange={handleAmountChange}
            />
          </label>
          <button
            onClick={() => handleTransaction(parseInt(amount))}
            disabled={!amount || parseInt(amount) <= 0}
          >
          Transfer
          </button>
          {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
          {transferComplete && (
            <p style={{ color: "green" }}>
              Bank received {parseInt(amount)} from Wallet through Card!
            </p>
          )}
        </div>
        <Bank />
      </div>
    </MyContext.Provider>
  );
}

export default Wallet;