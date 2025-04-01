import React from 'react';
import './App.css';
import Navbar from './Components/NavBar';
import HomePage from './Components/Home ';
import AboutSection from './Components/About';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import ContactPage from './Components/ContectUS';
import LoginPage from './Components/Login';
import Footer from './Components/Footer';

function App() {
  return (
    <BrowserRouter>
      {/* Navbar will be visible on all pages */}
      <Navbar />

      {/* Define all routes */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutSection />} />
        <Route path='/contectus' element={<ContactPage/>}/>
        <Route path='/login' element={<LoginPage/>}/>
      </Routes>
      <Footer/>
    </BrowserRouter>
  );
}

export default App;
