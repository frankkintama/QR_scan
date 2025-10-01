import React, { useEffect } from "react";
import { useAuth } from "../lib/useAuth";
import { useNavigate } from "react-router-dom";

const Dashboard: React.FC = () => {
  const { user, isLoggedIn } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoggedIn) {
      navigate("/login");
    }
  }, [isLoggedIn, navigate]);

  if (!user) {
    return <p>Loading user info...</p>; 
  }

  return (
    <div style={{ maxWidth: "500px", margin: "2rem auto" }}>
      <h1>Dashboard</h1>
        <p>Welcome, {user.username} 👋</p>
    </div>
  );
};

export default Dashboard;
