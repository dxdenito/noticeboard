import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { api } from "../api/client";
import bgImage from "../images/jkuat.jpg"
import { useToast } from "../context/ToastContext";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "", full_name: "" });
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const { showError } = useToast();

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
      showError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="grid grid-cols-1 md: grid-cols-2">
      <div style={{ backgroundImage: `url(${bgImage})` }} className="hidden md:block w-full h-screen bg-cover bg-center bg-no-repeat flex items-center justify-center"></div>
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-md w-full max-w-sm">
        <h1 className="text-xl font-semibold mb-4">Register</h1>
        {error && <p className="text-red-600 text-sm mb-3">{error}</p>}

        <label className="font-bold mb-2 ">Full Name</label>

        <input
          type="text" placeholder="Full name" required
          value={form.full_name} onChange={(e) => updateField("full_name", e.target.value)}
          className="w-full border rounded px-3 py-2 mb-3"
        />

        <label className="font-bold mb-2 ">Email</label>
        <input
          type="email" placeholder="Email" required
          value={form.email} onChange={(e) => updateField("email", e.target.value)}
          className="w-full border rounded px-3 py-2 mb-3"
        />
        <label className="font-bold mb-2 " >Password</label>
        <input
          type="password" placeholder="Password" required
          value={form.password} onChange={(e) => updateField("password", e.target.value)}
          className="w-full border rounded px-3 py-2 mb-4"
        />

        <button type="submit" disabled={submitting}
          className="w-full bg-jkuat-green text-white hover:bg-blue-800 cursor-pointer text-white rounded py-2 disabled:opacity-50">
          {submitting ? "Registering..." : "Register"}
        </button>

        <p className="text-sm text-center mt-4">
          Already have an account? <Link to="/login" className="text-blue-600">Log in</Link>
        </p>
      </form>
    </div>
    </div>
  );
}