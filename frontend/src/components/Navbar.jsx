import { NavLink } from "react-router-dom";
import "../styles/NavBar.css";

function NavBar() {
  return (
    <header className="atlas-header">
      <NavLink className="atlas-logo" to="/">
        🏔️ Project Atlas
      </NavLink>

      <nav className="atlas-navigation">
        <NavLink to="/">Home</NavLink>
        <NavLink to="/character">Character</NavLink>
        <NavLink to="/inventory">Inventory</NavLink>
        <NavLink to="/world">World</NavLink>
        <NavLink to="/battle">Battle</NavLink>
        <NavLink to="/quests">Quests</NavLink>
        <NavLink to="/companions">Companions</NavLink>
        <NavLink to="/journal">Journal</NavLink>
      </nav>
    </header>
  );
}

export default NavBar;