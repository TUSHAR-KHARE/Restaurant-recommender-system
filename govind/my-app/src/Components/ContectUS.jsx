import React from "react";
import Contact from '../assets/contact.webp';

const ContactPage = () => {
  return (
    <div id="Contact" className="mt-20 w-full h-screen flex flex-col justify-center items-center gap-8 p-4">
      <div className="text-3xl font-semibold">Contact Us</div>

      <div className="w-full max-w-6xl h-[80vh] flex flex-col md:flex-row justify-center items-center rounded-lg overflow-hidden shadow-lg">
        {/* Left Section */}
        <div className="w-full md:w-1/2 h-full flex justify-center items-center animate-slideFromLeft">
          <div
            className="w-full h-100 bg-cover bg-center bg-no-repeat"
            style={{ backgroundImage: "url('https://raw.githubusercontent.com/Govindshukla880/Major-Project-UI-Demo/refs/heads/main/Image/contact.webp')", backgroundSize: "cover" }}
          ></div>
        </div>

        {/* Right Section - Contact Form */}
        <div className="w-full md:w-1/2 h-full flex flex-col justify-center items-center bg-white shadow-lg p-6 animate-slideFromRight rounded-lg">
          <div className="w-full text-center text-xl font-medium">Restaurant Feedback Form</div>

          <form className="w-full flex flex-col items-center space-y-4 mt-4">
            <div className="flex flex-col space-y-2 w-3/4">
              <input
                type="text"
                className="p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="First Name"
                required
              />
              <input
                type="text"
                className="p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Second Name"
                required
              />
            </div>

            <div className="w-3/4">
              <input
                type="number"
                className="p-3 w-full border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter Your Phone Number"
                required
              />
            </div>

            <div className="w-3/4">
              <input
                type="email"
                className="p-3 w-full border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter your Email here"
                required
              />
            </div>

            <div className="w-3/4">
              <textarea
                className="p-3 w-full border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Write your Message here..."
                rows="4"
              ></textarea>
            </div>

            <div>
              <button
                type="submit"
                className="mt-4 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-lg font-semibold shadow-md"
              >
                Submit
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;
