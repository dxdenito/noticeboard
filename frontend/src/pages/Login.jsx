import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import bgImage from "../images/jkuat.jpg"
import { useToast } from "../context/ToastContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const { showError } = useToast();

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      showError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2">
      <div style={{ backgroundImage: `url(${bgImage})` }} className="hidden md:block w-full h-screen bg-cover bg-center bg-no-repeat flex items-center justify-center">
        
      </div>
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm"
      >
        <h1 className="text-xl font-semibold mb-4">Log in</h1>

        {error && <p className="text-red-600 text-sm mb-3">{error}</p>}
        <label className="font-bold mb-2" >Email</label>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 mb-3"
          required
        />
        <label className="font-bold mb-2 ">Password</label>
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full border border-gray-300 rounded px-3 py-2 mb-4"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-jkuat-green text-white hover:bg-blue-800 cursor-pointer rounded py-2 disabled:opacity-50"
        >
          {loading ? "Logging in..." : "Log in"}
        </button>
        <p className="text-sm text-center mt-4">
          Don't have an account? <Link to="/register" className="text-blue-600">Register</Link>
        </p>
      </form>
    </div>
    </div>
  );
}