// src/components/Logout.tsx
import { useAuth } from "../lib/useAuth";
import { useNavigate } from "react-router-dom";

export default function Logout() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/login"); // quay về trang login
  };

  return (
    <button
      onClick={handleLogout}
      value="Đăng xuất"
      className="button"
    >
    </button>
  );
}
