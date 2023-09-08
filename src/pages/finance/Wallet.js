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
  const [transferAmount, setTransferAmount] = useState("");
  const [addMoneyAmount, setAddMoneyAmount] = useState("");
  const [balance, setBalance] = useState(1000);
  const [errorMessage, setErrorMessage] = useState("");
  const [transferComplete, setTransferComplete] = useState(false);

  useEffect(() => {
    if (transferComplete) {
      const timer = setTimeout(() => {
        setTransferComplete(false);
      }, 2000); // 2 seconds in milliseconds

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

  const handleAddMoney = (moneyAmount) => {
    if (moneyAmount <= 0) {
      setErrorMessage("Amount must be greater than zero.");
    } else {
      setErrorMessage("");
      updateBalance(moneyAmount);
    }
  };

  const updateBalance = (amount) => {
    setBalance((prevBalance) => prevBalance + amount);
  };

  const handleInputChange = (e, type) => {
    const value = e.target.value;
    if (type === "transfer") {
      setTransferAmount(value);
    } else if (type === "addMoney") {
      setAddMoneyAmount(value);
    }
  };

  return (
    <MyContext.Provider
      value={{
        transferAmount,
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
              value={transferAmount}
              onChange={(e) => handleInputChange(e, "transfer")}
            />
          </label>
          <button
            onClick={() => handleTransaction(parseInt(transferAmount))}
            disabled={!transferAmount || parseInt(transferAmount) <= 0}
          >
            Transfer
          </button>
          {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
          {transferComplete && (
            <p style={{ color: "green" }}>
              Bank received {parseInt(transferAmount)} from Wallet through Card!
            </p>
          )}
        </div>
        <div>
          <label>
            Add Money:
            <input
              type="number"
              value={addMoneyAmount}
              onChange={(e) => handleInputChange(e, "addMoney")}
            />
          </label>
          <button
            onClick={() => handleAddMoney(parseInt(addMoneyAmount))}
            disabled={!addMoneyAmount || parseInt(addMoneyAmount) <= 0}
          >
            Add
          </button>
        </div>
        <Bank />
      </div>
    </MyContext.Provider>
  );
}

export default Wallet;
