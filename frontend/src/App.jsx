import { useState } from 'react'
import './App.css'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Stocks from './pages/Stocks';
import Advisor from './pages/Advisor';
import Auth from './pages/Auth';
import Zakat from './pages/Zakat';

function App() {
  

  return (
    <>
      <BrowserRouter>
        <nav>
          <Link to="/zakat">Zakat</Link>
          <Link to="/">Dashboard</Link>
          <Link to="/stocks">Stocks</Link>
          <Link to="/advisor">AI Advisor</Link>
          <Link to="/auth">Log out</Link>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/stocks" element={<Stocks />} />
          <Route path="/advisor" element={<Advisor />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/zakat" element={<Zakat />} />
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App
