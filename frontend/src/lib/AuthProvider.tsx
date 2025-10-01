// src/lib/AuthProvider.tsx
import { createContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000"

interface User {
  id: string;
  email: string
}

interface AuthContextType {
  user: User | null;
  isLoggedIn: boolean;
  login: (email: string, password: string) => Promise<void>;
}


const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

    // Fetch current user from backend
  const fetchCurrentUser = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/users/me`, {
        method: "GET",
        credentials: "include", // sends cookie
      });
      if (res.ok) {
        const data = await res.json();
        setUser(data);
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentUser();
  }, []);

 /*lấy email và password từ login, gọi request tới backend*/
 const login = async (email: string, password: string) => {

    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const res = await fetch(`${BACKEND_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      credentials: "include",
      body: formData,
    });

    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        const errorMessage = errorData.detail || "Invalid email or password";
        throw new Error(errorMessage);
    }

    await fetchCurrentUser();
  };


  return (
    <AuthContext.Provider value={{ user, isLoggedIn: !!user, login }}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

export { AuthContext };
