import { createContext, useContext, useState, useEffect } from "react";
import { api } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const [pendingCount, setPendingCount] = useState(0);

  async function loadPendingCount() {
    if (user?.role.role !== "admin") {
      setPendingCount(0);
      return;
    }
    try {
      const data = await api.get("/notices/pending");
      setPendingCount(data.length);
    } catch {
      setPendingCount(0);
    }
  }

  async function loadCurrentUser() {
    try {
      const data = await api.get("/users/me");
      setUser(data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadCurrentUser();
  }, []);

  useEffect(() => {
    loadPendingCount();
  }, [user]);

  async function login(email, password) {
    const formBody = new URLSearchParams();
    formBody.append("username", email);
    formBody.append("password", password);

    await fetch(`${import.meta.env.VITE_API_URL}/auth/login`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formBody,
    }).then(async (res) => {
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Login failed");
      }
    });

    await loadCurrentUser();
  }

  async function logout() {
    await api.post("/auth/logout");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout , pendingCount, refreshPendingCount: loadPendingCount}}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}