import React from "react";
import MyContext from "./MyContext";

function Balance() {
  const value = React.useContext(MyContext);

  return <div className="Balance">Balance: {value.balance}</div>;
}

export default Balance;