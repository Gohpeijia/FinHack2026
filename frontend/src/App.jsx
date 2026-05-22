import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import Advisor from './pages/Advisor';
import Auth from './pages/Auth';
import Zakat from './pages/Zakat';
import Stocks from './pages/Stocks';

import { FaCalculator, FaThLarge, FaRobot, FaSignOutAlt, FaChartLine } from 'react-icons/fa';
import { signOut } from 'firebase/auth';
import { auth } from './firebase';
/**
 * NavBar — collapses to icon-only when on /stocks,
 * because the stocks page has its own side panel.
 */

function NavBar() {
  const location = useLocation();
  const isStocks = location.pathname === '/stocks';

  return (
    <nav className={isStocks ? 'nav-icon-only' : ''}>
      <Link className="nav-zakat" to="/zakat" title="Zakat">
        <FaCalculator />
        {!isStocks && <span>Zakat</span>}
      </Link>
      <Link className="nav-stocks" to="/stocks" title="Stocks">
        <FaChartLine />
        {!isStocks && <span>Stocks</span>}
      </Link>
      <Link className="nav-advisor" to="/advisor" title="AI Advisor">
        <FaRobot />
        {!isStocks && <span>AI Advisor</span>}
      </Link>
      <Link className="nav-logout" to="/" title="Log out">
        <FaSignOutAlt />
        {!isStocks && <span>Log out</span>}
      </Link>
    </nav>
  );
}

function App() {
  return (
    <>
      <BrowserRouter>
        <NavBar />
        <Routes>
          <Route path="/stocks"    element={<Stocks />} />
          <Route path="/zakat"     element={<Zakat />} />
          <Route path="/stocks" element={<Stocks />} />
          <Route path="/advisor"   element={<Advisor />} />
          <Route path="/"          element={<Auth />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;