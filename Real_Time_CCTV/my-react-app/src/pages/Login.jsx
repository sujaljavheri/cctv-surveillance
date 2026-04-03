import React, { useState } from 'react';

const Login = ({ onLogin, onNavigateRegister }) => {
  const [form, setForm] = useState({ email: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.email || !form.password) {
      setError('Please fill in all fields.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      // ── Replace this block with your actual Spring Boot API call ──
      // const res = await fetch('http://localhost:8080/api/auth/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ email: form.email, password: form.password }),
      // });
      // if (!res.ok) throw new Error('Invalid credentials');
      // const data = await res.json();
      // localStorage.setItem('token', data.token);
      // onLogin(data.user);

      // Demo: simulate success after 1.5s
      await new Promise(r => setTimeout(r, 1500));
      onLogin({ email: form.email, name: 'Admin User', role: 'ADMIN' });
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#060a10] flex flex-col" style={{ fontFamily: "'Rajdhani', sans-serif" }}>
      {/* Background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute inset-0"
          style={{
            background: `radial-gradient(ellipse at 20% 50%, rgba(30,58,138,0.12) 0%, transparent 60%),
                         radial-gradient(ellipse at 80% 20%, rgba(67,20,128,0.10) 0%, transparent 60%),
                         radial-gradient(ellipse at 60% 80%, rgba(15,118,110,0.06) 0%, transparent 50%)`
          }} />
        {/* Grid */}
        <div className="absolute inset-0 opacity-[0.025]"
          style={{
            backgroundImage: `linear-gradient(rgba(99,179,237,1) 1px, transparent 1px),
                               linear-gradient(90deg, rgba(99,179,237,1) 1px, transparent 1px)`,
            backgroundSize: '48px 48px'
          }} />
      </div>

      {/* Top bar */}
      <div className="relative z-10 flex items-center justify-between px-6 py-3 border-b border-white/5"
        style={{ background: 'rgba(6,10,16,0.8)', backdropFilter: 'blur(8px)' }}>
        <div className="flex items-center gap-3">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-700 flex items-center justify-center">
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
                d="M15 10l4.553-2.069A1 1 0 0121 8.82v6.36a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
          <span className="text-sm font-bold tracking-wide text-white">CCTV Face Recognition System</span>
        </div>
        <div className="flex items-center gap-1.5 bg-green-900/20 border border-green-800/30 rounded-full px-2.5 py-1">
          <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
          <span className="text-[10px] text-green-400 font-mono tracking-wider">SYSTEM ONLINE</span>
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex items-center justify-center px-4 py-12 relative z-10">
        <div className="w-full max-w-sm">

          {/* Card */}
          <div className="rounded-2xl overflow-hidden"
            style={{
              background: 'linear-gradient(160deg, #0c1525 0%, #080d18 100%)',
              border: '1px solid rgba(59,130,246,0.15)',
              boxShadow: '0 24px 64px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.02)',
            }}>

            {/* Card Header */}
            <div className="px-8 pt-8 pb-6 text-center"
              style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
              <div className="flex justify-center mb-4">
                <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/20 to-indigo-600/20 flex items-center justify-center"
                  style={{ border: '1px solid rgba(99,102,241,0.3)' }}>
                  <svg className="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                      d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                  <span className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-green-500 border-2 border-[#080d18] flex items-center justify-center">
                    <span className="text-[8px] text-white font-bold">✓</span>
                  </span>
                </div>
              </div>
              <h2 className="text-xl font-bold tracking-wide text-white">Secure Access</h2>
              <p className="text-[11px] text-gray-500 font-mono tracking-wider mt-1 uppercase">
                Surveillance Command Center
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="px-8 py-6 flex flex-col gap-4">

              {/* Error */}
              {error && (
                <div className="flex items-center gap-2 bg-red-950/50 border border-red-800/40 rounded-lg px-3 py-2.5">
                  <svg className="w-3.5 h-3.5 text-red-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                  <span className="text-[11px] text-red-400 font-mono">{error}</span>
                </div>
              )}

              {/* Email */}
              <InputField
                label="Email Address"
                name="email"
                type="email"
                value={form.email}
                onChange={handleChange}
                placeholder="admin@ghrcep.edu.in"
                icon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
                      d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                }
              />

              {/* Password */}
              <InputField
                label="Password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                value={form.password}
                onChange={handleChange}
                placeholder="••••••••"
                icon={
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
                      d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                }
                suffix={
                  <button type="button" onClick={() => setShowPassword(!showPassword)}
                    className="text-gray-500 hover:text-blue-400 transition-colors">
                    {showPassword
                      ? <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                        </svg>
                      : <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                    }
                  </button>
                }
              />

              {/* Forgot password */}
              <div className="flex justify-end -mt-2">
                <button type="button" className="text-[11px] text-blue-400/70 hover:text-blue-400 font-mono tracking-wider transition-colors">
                  FORGOT PASSWORD?
                </button>
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 rounded-xl font-bold tracking-[0.15em] uppercase text-sm text-white transition-all duration-200 flex items-center justify-center gap-2 mt-1 disabled:opacity-60"
                style={{
                  background: loading
                    ? 'linear-gradient(135deg, #1e40af, #1e3a8a)'
                    : 'linear-gradient(135deg, #2563eb, #1d4ed8)',
                  boxShadow: loading ? 'none' : '0 4px 20px rgba(37,99,235,0.35)',
                }}
              >
                {loading ? (
                  <>
                    <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                    Authenticating...
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                        d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    Sign In
                  </>
                )}
              </button>

              {/* Divider */}
              <div className="flex items-center gap-3 my-1">
                <div className="flex-1 h-px bg-white/5" />
                <span className="text-[10px] text-gray-600 font-mono tracking-widest">OR</span>
                <div className="flex-1 h-px bg-white/5" />
              </div>

              {/* Register link */}
              <p className="text-center text-[11px] text-gray-500 font-mono">
                DON'T HAVE AN ACCOUNT?{' '}
                <button type="button" onClick={onNavigateRegister}
                  className="text-blue-400 hover:text-blue-300 font-bold tracking-wider transition-colors">
                  REGISTER
                </button>
              </p>
            </form>
          </div>

          {/* Footer */}
          <p className="text-center text-[9px] text-gray-700 font-mono tracking-widest mt-6 uppercase">
            GH Raisoni College · CSE-AI · FYP 2025–26
          </p>
        </div>
      </div>
    </div>
  );
};

/* ── Reusable Input Field ── */
const InputField = ({ label, name, type, value, onChange, placeholder, icon, suffix }) => {
  const [focused, setFocused] = useState(false);

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-[10px] font-bold tracking-[0.2em] uppercase text-gray-500 font-mono">{label}</label>
      <div
        className="flex items-center gap-2 rounded-xl px-3 py-2.5 transition-all duration-200"
        style={{
          background: 'rgba(255,255,255,0.03)',
          border: `1px solid ${focused ? 'rgba(59,130,246,0.5)' : 'rgba(255,255,255,0.07)'}`,
          boxShadow: focused ? '0 0 0 3px rgba(59,130,246,0.08)' : 'none',
        }}
      >
        <span className={`flex-shrink-0 transition-colors ${focused ? 'text-blue-400' : 'text-gray-600'}`}>{icon}</span>
        <input
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder={placeholder}
          className="flex-1 bg-transparent text-sm text-gray-200 placeholder-gray-700 outline-none font-mono tracking-wider"
          style={{ caretColor: '#60a5fa' }}
        />
        {suffix && <span className="flex-shrink-0">{suffix}</span>}
      </div>
    </div>
  );
};

export default Login;