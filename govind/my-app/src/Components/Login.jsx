import React from "react";
const LoginPage = () => {
    return (
      <div className="w-full h-screen flex justify-center items-center bg-gray-100 p-4">
        <div className="w-full max-w-md bg-white shadow-lg rounded-lg p-6">
          <h2 className="text-2xl font-semibold text-center mb-6">Login</h2>
          <form className="flex flex-col space-y-4">
            <input
              type="email"
              className="p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Email"
              required
            />
            <input
              type="password"
              className="p-3 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Password"
              required
            />
            <button
              type="submit"
              className="mt-4 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-lg font-semibold shadow-md"
            >
              Login
            </button>
          </form>
        </div>
      </div>
    );
  };
  export default LoginPage;