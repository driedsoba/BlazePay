import React from "react";
import MyContext from "./MyContext";

function Total() {
  const value = React.useContext(MyContext);
  return <div className="total">Total:{value.total} </div>;
}

export default Total;