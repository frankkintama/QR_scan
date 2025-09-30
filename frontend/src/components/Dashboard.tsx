import React from "react";
import { useAuth } from "../lib/useAuth";

const Dashboard: React.FC = () => {
  const { user, isLoggedIn } = useAuth();

  if (!isLoggedIn) {
    return <p>Loading user info...</p>; 
  }

  return (
    <div style={{ maxWidth: "500px", margin: "2rem auto" }}>
      <h1>Dashboard</h1>
      {user ? (
        <p>Welcome, {user.email} 👋</p>
      ) : (
        <p>User not found</p>
      )}
    </div>
  );
};

export default Dashboard;
