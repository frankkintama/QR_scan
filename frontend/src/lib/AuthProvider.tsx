import { createContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000"

// Interface định nghĩa cấu trúc User
interface User {
  id: string;
  username: string
}

interface FastAPIErrorDetail {
  loc: string[];
  msg: string;
  type: string;
}

// Interface định nghĩa những gì Context cung cấp cho components
interface AuthContextType {
  user: User | null;           //null nếu chưa login
  isLoggedIn: boolean;    
  register: (email: string, username: string, password:string, confirmPassword:string) => Promise<void>;    
  login: (username: string, password: string) => Promise<void>; 
  logout: () => Promise<void>;
}

// Tạo Context - nơi lưu trữ authentication state
const AuthContext = createContext<AuthContextType | undefined>(undefined);

//
//
//

// Provider component - wrap toàn bộ app để chia sẻ auth state
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);  // State lưu user
  const [loading, setLoading] = useState(true);         // State loading khi fetch user

  // Function lấy thông tin user hiện tại từ backend
  const fetchCurrentUser = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/users/me`, {
        method: "GET",
        credentials: "include",  // Gửi COOKIE
      });

      if (res.ok) {  // Status 200-299
        const data = await res.json();
        setUser(data);  // Lưu user vào state
      } else {  // 401 Unauthorized hoặc lỗi khác
        setUser(null);  // Không có user
      }
    } catch (error) {  // Network error
      console.error("Error fetching user:", error);
      setUser(null);
    } finally {
      setLoading(false);  // Dừng loading dù thành công hay thất bại
    }
  };

  // useEffect chạy 1 lần khi component mount
  // Kiểm tra xem user đã login chưa (có cookie hay không)
  useEffect(() => {
    fetchCurrentUser();
  }, []);  // [] = chỉ chạy 1 lần khi component mount

//
//
//

  //REGISTER
const register = async (
  email: string,
  username: string,
  password: string,
  confirmPassword: string
) => {
  const res = await fetch(`${BACKEND_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ email, username, password, confirmPassword }),
  });

  if (!res.ok) {
    let errorMessage = "Đăng ký thất bại";

    try {
      const errorData = await res.json();

      if (typeof errorData.detail === "string") {
        errorMessage = errorData.detail;
      } else if (Array.isArray(errorData.detail)) {
        const details = errorData.detail as FastAPIErrorDetail[];
        errorMessage = details.map((e) => e.msg).join(", ");
      }
    } catch {
      // ignore parse errors
    }

    throw new Error(errorMessage);
  }

  await login(username, password);
  
  await fetchCurrentUser();
};

//
//
//

  //LOGIN
  const login = async (
    username: string, 
    password: string
  ) => {

    // Tạo form data theo chuẩn OAuth2
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const res = await fetch(`${BACKEND_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },  // Form data, không phải JSON
      credentials: "include",  // Nhận COOKIE từ backend
      body: formData,
    });


    if (!res.ok) {  // Login thất bại
      const errorData = await res.json().catch(() => ({}));
      const errorMessage = errorData.detail || "Đăng nhập thất bại";
      throw new Error(errorMessage);  // Throw error để Login component catch
    }
    
    // Login thành công (status 204)
    await fetchCurrentUser();  // Lấy thông tin user và lưu vào state
  };

//
//
//

  //LOGOUT
  const logout = async () => {
    try {
       const res = await fetch(`${BACKEND_URL}/auth/logout`, {
        method: "POST",
        credentials: "include",
      });
      console.log("Logout response:", res.status);
    } catch (error) {
      console.error("Error logging out:", error);
    } finally {

      setUser(null);  // reset state
    }
  };


  // Render Provider với value chứa state và functions
  return (
    <AuthContext.Provider value={{ user, isLoggedIn: !!user, register, login, logout }}>
      {!loading && children}  {/* Chỉ render children khi đã kiểm tra xong auth status */}
    </AuthContext.Provider>
  );
}

export { AuthContext };
