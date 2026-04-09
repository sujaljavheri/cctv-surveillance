import React, { useState } from "react";
import axios from "axios"; // ✅ added

const ROLES = ["ADMIN", "OPERATOR", "VIEWER"];

const Register = ({ onRegisterSuccess, onNavigateLogin }) => {
  const [form, setForm] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "OPERATOR",
    badgeId: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError("");
  };

  // ✅ Validation
  const validate = () => {
    if (
      !form.fullName ||
      !form.email ||
      !form.password ||
      !form.confirmPassword
    )
      return "Please fill in all required fields.";
    if (form.password.length < 8)
      return "Password must be at least 8 characters.";
    if (form.password !== form.confirmPassword)
      return "Passwords do not match.";
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email))
      return "Please enter a valid email address.";
    return null;
  };

  // ✅ UPDATED HANDLE SUBMIT
  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationError = validate();
    if (validationError) {
      setError(validationError);
      return;
    }

    setLoading(true);
    setError("");

    try {
      await axios.post("http://localhost:5000/api/auth/register", {
        name: form.fullName,
        email: form.email,
        password: form.password,
      });

      // ✅ success
      alert("Registration successful");

      // ✅ redirect to login
      onRegisterSuccess();
    } catch (err) {
      setError(err.response?.data?.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-black text-white">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-900 p-6 rounded-lg w-96 space-y-4"
      >
        <h2 className="text-xl font-bold text-center">Register</h2>

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <input
          type="text"
          name="fullName"
          placeholder="Full Name"
          value={form.fullName}
          onChange={handleChange}
          className="w-full p-2 rounded bg-gray-800"
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          className="w-full p-2 rounded bg-gray-800"
        />

        <input
          type={showPassword ? "text" : "password"}
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          className="w-full p-2 rounded bg-gray-800"
        />

        <input
          type={showConfirm ? "text" : "password"}
          name="confirmPassword"
          placeholder="Confirm Password"
          value={form.confirmPassword}
          onChange={handleChange}
          className="w-full p-2 rounded bg-gray-800"
        />

        <button
          type="button"
          onClick={() => setShowPassword(!showPassword)}
          className="text-sm text-blue-400"
        >
          Toggle Password
        </button>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 p-2 rounded"
        >
          {loading ? "Registering..." : "Register"}
        </button>

        <p className="text-center text-sm">
          Already have an account?{" "}
          <button onClick={onNavigateLogin} className="text-blue-400">
            Login
          </button>
        </p>
      </form>
    </div>
  );
};

export default Register;
