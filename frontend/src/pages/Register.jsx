import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api/client";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "", full_name: "" });
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await api.post("/auth/register", form);
      navigate("/login");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm">
        <h1 className="text-xl font-semibold mb-4">Register</h1>
        {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

        <input
          type="text" placeholder="Full name" required
          value={form.full_name} onChange={(e) => updateField("full_name", e.target.value)}
          className="w-full border rounded px-3 py-2 mb-3"
        />
        <input
          type="email" placeholder="Email" required
          value={form.email} onChange={(e) => updateField("email", e.target.value)}
          className="w-full border rounded px-3 py-2 mb-3"
        />
        <input
          type="password" placeholder="Password" required
          value={form.password} onChange={(e) => updateField("password", e.target.value)}
          className="w-full border rounded px-3 py-2 mb-4"
        />

        <button type="submit" disabled={submitting}
          className="w-full bg-blue-600 text-white rounded py-2 disabled:opacity-50">
          {submitting ? "Registering..." : "Register"}
        </button>

        <p className="text-sm text-center mt-4">
          Already have an account? <Link to="/login" className="text-blue-600">Log in</Link>
        </p>
      </form>
    </div>
  );
}