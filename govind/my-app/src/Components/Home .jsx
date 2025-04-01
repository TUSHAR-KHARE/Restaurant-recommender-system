import React from "react";
import { motion } from "framer-motion";
import AboutSection from "./About";

const HomePage = () => {
  return (
    <>
    <div className="relative h-screen w-full flex items-center justify-center px-4 md:px-8">
      {/* Background Image */}
      <img
        src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        alt="Zomato Background"
        className="absolute inset-0 w-full h-full object-cover opacity-85"
      />

      {/* Main Container */}
      <div className="relative z-10 flex flex-col md:flex-row w-full max-w-6xl gap-10">
        {/* Left Content Section - Moves Left to Right */}
        <motion.div
          initial={{ x: -200, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="flex-1 flex flex-col justify-center bg-black bg-opacity-60 p-8 rounded-lg shadow-lg"
        >
          <div className="opacity-90 text-white">
            <h1 className="text-3xl md:text-5xl font-bold">Zomato Dataset</h1>
            <p className="mt-4 text-md md:text-lg font-semibold">Based on Indore Location...</p>
            <p className="mt-4 text-sm md:text-base leading-relaxed">
              Welcome to our Restaurant Recommender System! Finding the perfect
              restaurant can be overwhelming, but we make it simple and effortless.
              Our AI-powered recommendation system helps you discover top-rated
              restaurants based on your location and favorite cuisine.
            </p>
            <button className="mt-6 px-5 py-3 w-60 bg-purple-700 hover:bg-red-600 rounded-lg text-white text-lg font-semibold">
              Explore Now
            </button>
          </div>
        </motion.div>

        {/* Right Form Section - Moves Right to Left */}
        <motion.div
          initial={{ x: 200, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="flex-1 flex flex-col justify-center bg-black p-8 rounded-lg shadow-lg"
        >
          <div className="opacity-90 text-white">
            <h2 className="text-3xl md:text-4xl font-bold">Find Your Best Restaurant</h2>
            <form className="space-y-4 mt-4">
              <div>
                <label htmlFor="locality" className="block text-sm font-medium">Locality</label>
                <input
                  id="locality"
                  type="text"
                  placeholder="Enter your locality"
                  className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 bg-white text-black"
                />
              </div>
              <div>
                <label htmlFor="cuisine" className="block text-sm font-medium">Cuisine</label>
                <select
                  id="cuisine"
                  className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500 bg-white text-black"
                >
                  <option value="">Select Cuisine</option>
                  <option value="indian">Indian</option>
                  <option value="chinese">Chinese</option>
                  <option value="italian">Italian</option>
                  <option value="mexican">Mexican</option>
                  <option value="thai">Thai</option>
                </select>
              </div>
              <button
                type="submit"
                className="w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg text-lg font-semibold"
              >
                Predict
              </button>
            </form>
          </div>
        </motion.div>
      </div>
    </div>
 
    </>
    

  

  );
};

export default HomePage;
