import React, { useEffect } from "react";
import Logout from "../components/Logout"
import { useAuth } from "../lib/useAuth";
import { useNavigate } from "react-router-dom";
import "../App.css"

const Dashboard: React.FC = () => {
  const { user, isLoggedIn } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn) {
      navigate("/login");
    }
  }, [isLoggedIn, navigate]);

  if (!isLoggedIn && !user) {
    return <p>Loading user info...</p>; 
  }

  return (
    <div className="h-screen w-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-xl p-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-gray-600">Welcome, {user!.username} 👋</p>
          <Logout />
      </div>
    </div>
  </div>
  );
};

export default Dashboard;
