import { useAuth } from "../lib/useAuth";
import { useNavigate } from "react-router-dom";
import "../App.css"

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
      className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition disabled:bg-indigo-400 disabled:cursor-not-allowed"
    >
        Đăng xuất
    </button>
  );
}
