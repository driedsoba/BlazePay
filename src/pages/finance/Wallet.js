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
  color: "green"
};

function Wallet() {
  const [total, setTotal] = useState(700);
  const [amount, setAmount] = useState(500);
  const [balance, setBalance] = useState(null);

  //Goal: send Wallet money to Bank

  return (
    <MyContext.Provider
      value={{
        amount,
        total,
        setTotal,
        balance,
        setBalance,
        amountStyle
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
        <Bank />
      </div>
    </MyContext.Provider>
  );
}

export default Wallet;