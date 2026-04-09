import React, { useState } from "react";
import axios from "axios"; // ✅ IMPORTANT (added)

const Login = ({ onLogin, onNavigateRegister }) => {
  const [form, setForm] = useState({ email: "", password: "" });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError("");
  };

  // ✅ UPDATED HANDLE SUBMIT
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.email || !form.password) {
      setError("Please fill in all fields.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const res = await axios.post("http://localhost:5000/api/auth/login", {
        email: form.email,
        password: form.password,
      });

      // ✅ Save token
      localStorage.setItem("token", res.data.token);

      // ✅ Move to dashboard
      onLogin(res.data);
    } catch (err) {
      setError(err.response?.data?.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen bg-[#060a10] flex flex-col"
      style={{ fontFamily: "'Rajdhani', sans-serif" }}
    >
      {/* Your UI remains SAME — no change needed */}

      <form onSubmit={handleSubmit} className="px-8 py-6 flex flex-col gap-4">
        {error && <p className="text-red-400 text-sm">{error}</p>}

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          className="p-2 rounded"
        />

        <input
          type={showPassword ? "text" : "password"}
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          className="p-2 rounded"
        />

        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white p-2 rounded"
        >
          {loading ? "Loading..." : "Login"}
        </button>

        <button type="button" onClick={onNavigateRegister}>
          Register
        </button>
      </form>
    </div>
  );
};

export default Login;
