import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { LoginFormSchema } from "../lib/rules";
import { useAuth } from "../lib/useAuth";
import { useNavigate } from "react-router-dom";
import "../App.css";

type LoginFormData = z.infer<typeof LoginFormSchema>;

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(LoginFormSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      await login(data.email, data.password);
      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("password", {
        type: "manual",
        message: "Email hoặc mật khẩu không hợp lệ",
      });
    }
  };

  return (
    <div className="form-container">
      <h2>Form Đăng Nhập</h2>
      <form className="form" onSubmit={handleSubmit(onSubmit)}>
        <input 
          type="email" 
          {...register("email")} 
          placeholder="Email" />
        {errors.email && (
          <span className="error">
            {errors.email.message}
          </span>
        )}

        <input 
          type="password" 
          {...register("password")} 
          placeholder="Password" />
        {errors.password && (
          <span className="error">
            {errors.password.message}
          </span>
        )}

        <input
          type="submit"
          value={isSubmitting ? "Logging in..." : "Đăng nhập"}
          style={{ backgroundColor: "#a1eafb" }}
          disabled={isSubmitting}
          className="button"
        />
      </form>
    </div>
  );
}

export default Login;
