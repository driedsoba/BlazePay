import React from "react";
import MyContext from './MyContext'

function Bank() {
  const value = React.useContext(MyContext)
  return (
    <div>
      <h2>Bank received <span style={value.amountStyle}>{value.amount}</span> from Wallet through Card!</h2>
      
    </div>
  );
}

export default Bank;