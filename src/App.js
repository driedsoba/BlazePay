import React from "react";
import "./App.css";
import Navbar from "./Navbar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import User from "./pages/user";
import Contacts from "./pages/finance/contacts";
import Financial from "./pages/finance/financial";
import Home from "./pages/home/home";

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        {/* <Route exact path='/' element={<Home />} /> */}
        <Route path="/home" element={<Home />} />
        {/* <Route path="/contacts" element={<Contacts />} /> */}
        <Route path="/financial" element={<Financial />} />
        <Route path="/user" element={<User />} />
      </Routes>
    </Router>
  );
}

export default App;
