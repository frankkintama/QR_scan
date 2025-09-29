import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api"; // axios instance

interface User {
  id: string;
  email: string;
}

const Dashboard: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await api.get<User>("/users/me");
        setUser(response.data);
      } catch (error) {
        console.error("Failed to fetch user:", error);
        // If unauthorized, send back to login
        navigate("/login", { replace: true });
      }
    };

    fetchUser();
  }, [navigate]);

  return (
    <div style={{ maxWidth: "500px", margin: "2rem auto" }}>
      <h1>Dashboard</h1>
      {user ? (
        <p>Welcome, {user.email} 👋</p>
      ) : (
        <p>Loading user info...</p>
      )}
    </div>
  );
};

export default Dashboard;
