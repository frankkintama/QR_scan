// src/lib/AuthProvider.tsx
import { createContext,  useState } from "react";
import type { ReactNode } from "react";
import { login as apiLogin, logout as apiLogout, getToken } from "./auth";

interface AuthContextType {
  token: string | null;
  isLoggedIn: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(getToken());

  const login = async (email: string, password: string) => {
    const newToken = await apiLogin(email, password);
    setToken(newToken);
  };

  const logout = () => {
    apiLogout();
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, isLoggedIn: !!token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export { AuthContext };