import { BrowserRouter, Routes, Route } from "react-router-dom";

import NavBar from "./components/NavBar.jsx";
import Home from "./pages/Home.jsx";
import Character from "./pages/Character.jsx";
import Inventory from "./pages/Inventory.jsx";
import World from "./pages/World.jsx";
import Battle from "./features/Battles/Battle.jsx";
import Quests from "./pages/Quests.jsx";
import Companions from "./pages/Companions.jsx";
import Journal from "./pages/Journal.jsx";


function App() {
  return (
    <BrowserRouter>
      <NavBar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/character" element={<Character />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/world" element={<World />} />
        <Route path="/battle" element={<Battle />} />
        <Route path="/quests" element={<Quests />} />
        <Route path="/companions" element={<Companions />} />
        <Route path="/journal" element={<Journal />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;