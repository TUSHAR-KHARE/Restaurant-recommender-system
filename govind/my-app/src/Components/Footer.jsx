import React from 'react';
const Footer = () => {
    return (
      <footer className="w-full bg-gray-900 text-white text-center p-6 mt-8">
        <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
          <div>
            <h3 className="font-semibold mb-2">About Zomato</h3>
            <ul>
              <li>Who We Are</li>
              <li>Blog</li>
              <li>Work With Us</li>
              <li>Investor Relations</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">For Restaurants</h3>
            <ul>
              <li>Partner With Us</li>
              <li>Apps For You</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Contact & Social</h3>
            <ul>
              <li>Help & Support</li>
              <li>Terms & Conditions</li>
              <li>Privacy Policy</li>
              <li className="flex gap-4 justify-center mt-2">
                <span>📘</span>
                <span>🐦</span>
                <span>📸</span>
              </li>
            </ul>
          </div>
        </div>
        <p className="text-sm mt-4">&copy; 2025 Zomato Clone. All Rights Reserved.</p>
      </footer>
    );
  };
  export default Footer;
  