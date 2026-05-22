import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Advisor from './pages/Advisor';
import Auth from './pages/Auth';
import Zakat from './pages/Zakat';

import { FaCalculator, FaThLarge, FaRobot, FaSignOutAlt} from 'react-icons/fa';

function App() {
  

  return (
    <>
      <BrowserRouter>
        <nav>
          <Link className="nav-zakat" to="/zakat">
            <FaCalculator />
            Zakat
          </Link>
          <Link className="nav-dashboard" to="/">
            <FaThLarge />
            Dashboard
          </Link>
          <Link className="nav-advisor" to="/advisor">
            <FaRobot />
            AI Advisor
          </Link>
          <Link className="nav-logout" to="/">
            <FaSignOutAlt />
            Log out
          </Link>
        </nav>

        <Routes>
          <Route path="/zakat" element={<Zakat />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/advisor" element={<Advisor />} />
          <Route path="/" element={<Auth />} />
          
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
