import React, { useState } from "react";
import Total from "./Total";
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
  const [total, setTotal] = useState(700);
  const [amount, setAmount] = useState(""); // Initialize user input amount as an empty string
  const [balance, setBalance] = useState(700); // Initialize balance to 700
  const [errorMessage, setErrorMessage] = useState(""); // State for error messages

  // Function to update the balance and total when a transaction is made
  const handleTransaction = (transactionAmount) => {
    if (transactionAmount <= 0) {
      setErrorMessage("Amount must be greater than zero.");
    } else if (transactionAmount > balance) {
      setErrorMessage("Insufficient balance.");
    } else {
      // Clear any previous error messages
      setErrorMessage("");

      // Update the balance by subtracting the transaction amount
      setBalance((prevBalance) => prevBalance - transactionAmount);

      // Update the total by subtracting the transaction amount
      setTotal((prevTotal) => prevTotal - transactionAmount);
    }
  };

  const handleAmountChange = (e) => {
    // Update the amount state when the user types in the input field
    setAmount(e.target.value);
  };

  return (
    <MyContext.Provider
      value={{
        amount,
        total,
        setTotal,
        balance,
        setBalance,
        amountStyle,
        handleTransaction, // Pass the transaction function to child components
      }}
    >
      <div>
        <div className="Wallet" style={style}>
          <Total />
          &nbsp;
          &nbsp;
          &nbsp;
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
        </div>
        <Bank />
      </div>
    </MyContext.Provider>
  );
}

export default Wallet;
