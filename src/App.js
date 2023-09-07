import React from 'react';
import './App.css';
import Navbar from './Navbar';
import { BrowserRouter as Router, Routes, Route }
    from 'react-router-dom';
import Transfer from './pages/transfer';
import User from './pages/user';
import Financial from './pages/finance/financial';
import Home from './pages/home';
 
function App() {
    return (

          <Router>
                <Navbar />
                <Routes>
                    <Route exact path='/' element={<Home />} />
                    <Route path='/home' element={<Home />} />
                    <Route path='/financial' element={<Financial />} />
                    <Route path='/transfer' element={<Transfer />} />
                    <Route path='/user' element={<User />} />
                </Routes>
            </Router>


    );
}
 
export default App;