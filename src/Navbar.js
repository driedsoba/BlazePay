import React from "react";
import { Nav, NavLink, NavMenu } from "./NavbarElements";
import { removeToken } from "./helper";

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
          {/* <NavLink to="/user" activeStyle>
            Registration Page
          </NavLink> */}
          <NavLink
            onClick={() => {
              removeToken();
              window.location.replace("http://localhost:3000/home");
            }}
            activeStyle
          >
            Logout
          </NavLink>
        </NavMenu>
      </Nav>
    </>
  );
};

export default Navbar;
