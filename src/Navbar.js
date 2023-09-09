
import React from "react";
import { Nav, NavLink, NavMenu }
    from "./NavbarElements";
 
const Navbar = () => {
    return (
        <>
            <Nav>
                <NavMenu>
                    <NavLink to="/home" activeStyle>
                        Home
                    </NavLink>
                    <NavLink to="/financial" activeStyle>
                        Financial Services
                    </NavLink>
                    <NavLink to="/user" activeStyle>
                        Registration Page
                    </NavLink>
                </NavMenu>
            </Nav>
        </>
    );
};
 
export default Navbar;