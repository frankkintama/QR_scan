// src/lib/auth.ts
import axios from "axios";

const API_URL = "http://localhost:8000"; // adjust if backend runs elsewhere

export async function login(email: string, password: string) {
  const params = new URLSearchParams();
  params.append("username", email.trim().toLowerCase());
  params.append("password", password);

  const response = await axios.post<{ access_token: string }>(
    `${API_URL}/login`,
    params,
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
  );

  const token = response.data.access_token;
  localStorage.setItem("token", token);
  return token;
}

export function logout() {
  localStorage.removeItem("token");
}

export function getToken() {
  return localStorage.getItem("token");
}
