// src/lib/AuthProvider.tsx
import { createContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000"
console.log("Backend URL:", BACKEND_URL)

interface User {
  id: string;
  username: string
}

interface AuthContextType {
  user: User | null;
  isLoggedIn: boolean;
  login: (username: string, password: string) => Promise<void>;
}


const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

    // Fetch current user from backend
  const fetchCurrentUser = async () => {
    console.log("Fetching current user..."); //check
    try {
      const res = await fetch(`${BACKEND_URL}/users/me`, {
        method: "GET",
        credentials: "include", // sends cookie
      });

      console.log("/users/me status:", res.status); //check

      if (res.ok) {
        const data = await res.json();
        console.log("User data:", data); // Add
        setUser(data);
      } else {
        console.log("Failed to fetch user"); // Add
        setUser(null);
      }
    } catch (error) {
      console.error("Error fetching user:", error); // Add
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

 /*lấy username và password từ login, gọi request tới backend*/
 const login = async (username: string, password: string) => {
    console.log("Login attempt for:", username); // Add

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const res = await fetch(`${BACKEND_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      credentials: "include",
      body: formData,
    });

    console.log("Login response:", res.status); // Add

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        const errorMessage = errorData.detail || "Invalid username or password";
        throw new Error(errorMessage);
    }
    console.log("Login successful, fetching user..."); // Add
    await fetchCurrentUser();
    console.log("Current user state:", user); // Add - but this might be stale
  };


  return (
    <AuthContext.Provider value={{ user, isLoggedIn: !!user, login }}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

export { AuthContext };
