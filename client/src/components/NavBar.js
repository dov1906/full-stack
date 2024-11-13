import React from "react";
import { NavLink } from "react-router-dom";

function NavBar() {
    return (
        <nav>
            <NavLink to="/">Home</NavLink>
            <NavLink to="/entities">View Entities</NavLink>
            <NavLink to="/add_entity">Add New Entity</NavLink>
            <NavLink to="/statistics">Statistics</NavLink>
        </nav>
    );
}

export default NavBar;
