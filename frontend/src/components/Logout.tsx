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
      className="button"
    >
        Đăng xuất
    </button>
  );
}


