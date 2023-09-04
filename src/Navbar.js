
import React from "react";
import { Nav, NavLink, NavMenu }
    from "./NavbarElements";
 
const Navbar = () => {
    return (
        <>
            <Nav>
                <NavMenu>
                    <NavLink to="/home" activeStyle>
                        My Wallet
                    </NavLink>
                    <NavLink to="/financial" activeStyle>
                        Financial Services
                    </NavLink>
                    <NavLink to="/transfer" activeStyle>
                        Transfer
                    </NavLink>
                    <NavLink to="/user" activeStyle>
                        User Settings
                    </NavLink>
                </NavMenu>
            </Nav>
        </>
    );
};
 
export default Navbar;