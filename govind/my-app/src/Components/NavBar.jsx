import React, { useState } from "react";
import { FaBars, FaTimes } from "react-icons/fa";
import AboutSection from "./About";


const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-black text-white p-4 fixed w-full top-0 z-50 shadow-md">
      <div className="max-w-screen-xl flex items-center justify-between mx-auto px-4">
        <a href="#" className="text-2xl font-semibold">Zomato</a>
        
        {/* Mobile Menu Button */}
        <button
          type="button"
          className="md:hidden p-2 text-white focus:outline-none"
          aria-label="Toggle menu"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <FaTimes className="w-6 h-6" /> : <FaBars className="w-6 h-6" />}
        </button>
        
        {/* Navigation Links */}
        <div className={`absolute md:static top-16 left-0 w-full md:w-auto bg-black md:bg-transparent md:flex items-center transition-all duration-300 ${isOpen ? "block" : "hidden"}`}>
          <ul className="flex flex-col md:flex-row md:space-x-6 md:items-center w-full md:w-auto text-center md:text-left">
            <li><a href="/" className="block py-2 px-6 md:px-4 hover:text-gray-400">Home</a></li>
            <li><a href='/about' className="block py-2 px-6 md:px-4 hover:text-gray-400">About</a></li>
            <li><a href="#" className="block py-2 px-6 md:px-4 hover:text-gray-400">Top-Rated</a></li>
            <li><a href="/contectus" className="block py-2 px-6 md:px-4 hover:text-gray-400">Contact Us</a></li>
          </ul>
          <button className="w-full md:w-auto mx-6 md:ml-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"><a href="/login">Login</a></button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
