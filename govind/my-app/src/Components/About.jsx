import React from "react";

const AboutSection = () => {
  return (
    <section className="py-12 px-4 md:px-8 bg-white text-black mt-20">
      <h2 className="text-3xl md:text-4xl font-bold text-center mb-6">
        About Us
      </h2>
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center gap-8">
        {/* Left Content */}
        <div className="flex-1 h-80 bg-gray-100 p-6 rounded-lg shadow-lg flex flex-col justify-center">
          <h3 className="text-2xl font-semibold mb-4">About Zomato Dataset</h3>
          <p className="text-gray-700 text-sm md:text-base leading-relaxed">
            In today’s fast-paced world, choosing the right restaurant can be
            overwhelming. With thousands of dining options available, how do you
            know which one suits your taste and budget? Our Restaurant
            Recommender System solves this problem by providing personalized
            restaurant recommendations based on ratings, location, cuisine
            preferences, and data-driven insights.
          </p>
          <p className="mt-4 text-gray-700 text-sm md:text-base leading-relaxed">
            Whether you’re craving Italian, Indian, or Chinese cuisine, our
            system helps you discover the best places to eat with just a few
            clicks.
          </p>
        </div>

        {/* Right Image */}
        <div className="flex-1 h-80">
          <img
            src="https://github.com/Govindshukla880/Major-Project-UI-Demo/blob/main/Image/BG%202%20(1).jpg?raw=true"
            alt="Delicious food"
            className="w-full h-full object-cover rounded-lg shadow-lg"
          />
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
