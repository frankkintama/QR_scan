import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Dashboard from "./components/Dashboard";
import { AuthProvider } from "./lib/AuthProvider";
import { useAuth } from "./lib/useAuth";

// 👇 type-only import
import type { ReactNode } from "react";

type PrivateRouteProps = {
  children: ReactNode;
};

 const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
  const { isLoggedIn } = useAuth();
  
  if (isLoggedIn == null) {
    return <div>Loading...</div>;
  }
  return isLoggedIn ? <>{children}</> : <Navigate to="/login" replace />;
 }

const App: React.FC = () => {
  return (
    <AuthProvider>
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        {/* Default route */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
    </AuthProvider>
  );
};

export default App;
