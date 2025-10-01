// src/lib/rules.ts
import { z } from "zod";

const passwordRules = z
  .string()
  .min(1, {message: "Vui lòng nhập mật khẩu." })
  .min(5, {message: "Mật khẩu phải dài ít nhất 6 kí tự." })
  .regex(/[a-zA-Z]/, {message: "Phải có một chữ cái." })
  .regex(/[0-9]/, {message: "Phải có một con số." })
  .regex(/[^a-zA-Z0-9]/, {message: "Phải có một kí tự đặc biệt." })
  .trim();

export const LoginFormSchema = z.object({
  username: z.string().min(4, "Vui lòng nhập username hợp lệ."),
  password: passwordRules,
});


