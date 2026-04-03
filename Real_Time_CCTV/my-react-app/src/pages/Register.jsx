import React, { useState } from 'react';

const ROLES = ['ADMIN', 'OPERATOR', 'VIEWER'];

const Register = ({ onRegisterSuccess, onNavigateLogin }) => {
  const [form, setForm] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    role: 'OPERATOR',
    badgeId: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  };

  const validate = () => {
    if (!form.fullName || !form.email || !form.password || !form.confirmPassword)
      return 'Please fill in all required fields.';
    if (form.password.length < 8)
      return 'Password must be at least 8 characters.';
    if (form.password !== form.confirmPassword)
      return 'Passwords do not match.';
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email))
      return 'Please enter a valid email address.';
    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationError = validate();
    if (validationError) { setError(validationError); return; }
    setLoading(true);
    setError('');
    try {
      // ── Replace with your Spring Boot API call ──
      // const res = await fetch('http://localhost:8080/api/auth/register', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({
      //     fullName: form.fullName,
      //     email: form.email,
      //     password: form.password,
      //     role: form.role,
      //     badgeId: form.badgeId,
      //   }),
      // });
      // if (!res.ok) {
      //   const err = await res.json();
      //   throw new Error(err.message || 'Registration failed');
      // }

      // Demo: simulate success
      await new Promise(r => setTimeout(r, 1800));
      setSuccess(true);
      setTimeout(() => onRegisterSuccess(), 2000);
    } catch (err) {
      setError(err.message || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getPasswordStrength = (pwd) => {
    if (!pwd) return null;
    let score = 0;
    if (pwd.length >= 8) score++;
    if (/[A-Z]/.test(pwd)) score++;
    if (/[0-9]/.test(pwd)) score++;
    if (/[^A-Za-z0-9]/.test(pwd)) score++;
    if (score <= 1) return { label: 'WEAK', color: '#ef4444', width: '25%' };
    if (score === 2) return { label: 'FAIR', color: '#f59e0b', width: '50%' };
    if (score === 3) return { label: 'GOOD', color: '#3b82f6', width: '75%' };
    return { label: 'STRONG', color: '#22c55e', width: '100%' };
  };

  const strength = getPasswordStrength(form.password);

  return (
    <div className="min-h-screen bg-[#060a10] flex flex-col" style={{ fontFamily: "'Rajdhani', sans-serif" }}>
      {/* Background */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute inset-0"
          style={{
            background: `radial-gradient(ellipse at 80% 50%, rgba(30,58,138,0.12) 0%, transparent 60%),
                         radial-gradient(ellipse at 20% 80%, rgba(67,20,128,0.10) 0%, transparent 60%),
                         radial-gradient(ellipse at 50% 10%, rgba(15,118,110,0.06) 0%, transparent 50%)`
          }} />
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
        <button onClick={onNavigateLogin}
          className="flex items-center gap-1.5 text-[11px] text-gray-500 hover:text-blue-400 font-mono tracking-wider transition-colors">
          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          BACK TO LOGIN
        </button>
      </div>

      {/* Main */}
      <div className="flex-1 flex items-center justify-center px-4 py-10 relative z-10">
        <div className="w-full max-w-md">

          {/* Success overlay */}
          {success && (
            <div className="rounded-2xl p-10 flex flex-col items-center gap-4 text-center"
              style={{
                background: 'linear-gradient(160deg, #052e16 0%, #042f14 100%)',
                border: '1px solid rgba(34,197,94,0.3)',
                boxShadow: '0 0 40px rgba(34,197,94,0.15)',
              }}>
              <div className="w-16 h-16 rounded-full bg-green-500/20 border border-green-500/40 flex items-center justify-center">
                <svg className="w-8 h-8 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-green-400 tracking-wide">Registration Successful!</h3>
              <p className="text-sm text-gray-400 font-mono">Account created. Redirecting to login...</p>
              <div className="w-full h-1 rounded-full bg-green-900/40 overflow-hidden mt-2">
                <div className="h-full bg-green-500 rounded-full" style={{ animation: 'progress 2s linear forwards' }} />
              </div>
            </div>
          )}

          {!success && (
            <div className="rounded-2xl overflow-hidden"
              style={{
                background: 'linear-gradient(160deg, #0c1525 0%, #080d18 100%)',
                border: '1px solid rgba(59,130,246,0.15)',
                boxShadow: '0 24px 64px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.02)',
              }}>

              {/* Card Header */}
              <div className="px-8 pt-7 pb-5 flex items-center gap-4"
                style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500/20 to-purple-600/20 flex items-center justify-center flex-shrink-0"
                  style={{ border: '1px solid rgba(99,102,241,0.3)' }}>
                  <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                      d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                </div>
                <div>
                  <h2 className="text-lg font-bold tracking-wide text-white">Create Account</h2>
                  <p className="text-[10px] text-gray-500 font-mono tracking-wider uppercase">
                    New Operator Registration
                  </p>
                </div>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="px-8 py-6 flex flex-col gap-4">

                {error && (
                  <div className="flex items-center gap-2 bg-red-950/50 border border-red-800/40 rounded-lg px-3 py-2.5">
                    <svg className="w-3.5 h-3.5 text-red-400 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                    <span className="text-[11px] text-red-400 font-mono">{error}</span>
                  </div>
                )}

                {/* 2-col row: Full name + Badge ID */}
                <div className="grid grid-cols-2 gap-3">
                  <InputField label="Full Name *" name="fullName" type="text" value={form.fullName}
                    onChange={handleChange} placeholder="John Doe"
                    icon={<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>}
                  />
                  <InputField label="Badge ID" name="badgeId" type="text" value={form.badgeId}
                    onChange={handleChange} placeholder="EMP-001"
                    icon={<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" /></svg>}
                  />
                </div>

                {/* Email */}
                <InputField label="Email Address *" name="email" type="email" value={form.email}
                  onChange={handleChange} placeholder="you@ghrcep.edu.in"
                  icon={<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>}
                />

                {/* Role selector */}
                <div className="flex flex-col gap-1.5">
                  <label className="text-[10px] font-bold tracking-[0.2em] uppercase text-gray-500 font-mono">
                    Role *
                  </label>
                  <div className="grid grid-cols-3 gap-2">
                    {ROLES.map(r => (
                      <button key={r} type="button" onClick={() => setForm({ ...form, role: r })}
                        className="py-2 rounded-lg text-[11px] font-bold tracking-wider font-mono transition-all duration-150"
                        style={{
                          background: form.role === r
                            ? r === 'ADMIN' ? 'rgba(239,68,68,0.2)' : r === 'OPERATOR' ? 'rgba(59,130,246,0.2)' : 'rgba(34,197,94,0.15)'
                            : 'rgba(255,255,255,0.03)',
                          border: `1px solid ${form.role === r
                            ? r === 'ADMIN' ? 'rgba(239,68,68,0.5)' : r === 'OPERATOR' ? 'rgba(59,130,246,0.5)' : 'rgba(34,197,94,0.4)'
                            : 'rgba(255,255,255,0.07)'}`,
                          color: form.role === r
                            ? r === 'ADMIN' ? '#f87171' : r === 'OPERATOR' ? '#60a5fa' : '#4ade80'
                            : '#6b7280',
                        }}>
                        {r}
                      </button>
                    ))}
                  </div>
                  <p className="text-[10px] text-gray-700 font-mono">
                    {form.role === 'ADMIN' && '⚡ Full system access & user management'}
                    {form.role === 'OPERATOR' && '🎯 Manage detection & view all feeds'}
                    {form.role === 'VIEWER' && '👁 View-only access to camera feeds'}
                  </p>
                </div>

                {/* Password */}
                <div>
                  <InputField label="Password *" name="password" type={showPassword ? 'text' : 'password'}
                    value={form.password} onChange={handleChange} placeholder="Min. 8 characters"
                    icon={<svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>}
                    suffix={
                      <button type="button" onClick={() => setShowPassword(!showPassword)} className="text-gray-500 hover:text-blue-400 transition-colors">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
                            d={showPassword ? "M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                              : "M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"} />
                        </svg>
                      </button>
                    }
                  />
                  {/* Strength bar */}
                  {strength && (
                    <div className="mt-1.5 flex items-center gap-2">
                      <div className="flex-1 h-1 rounded-full bg-gray-800 overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-300"
                          style={{ width: strength.width, background: strength.color }} />
                      </div>
                      <span className="text-[9px] font-bold font-mono tracking-widest" style={{ color: strength.color }}>
                        {strength.label}
                      </span>
                    </div>
                  )}
                </div>

                {/* Confirm Password */}
                <InputField label="Confirm Password *" name="confirmPassword"
                  type={showConfirm ? 'text' : 'password'}
                  value={form.confirmPassword} onChange={handleChange} placeholder="Re-enter password"
                  icon={
                    form.confirmPassword && form.confirmPassword === form.password
                      ? <svg className="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" /></svg>
                      : <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
                  }
                  suffix={
                    <button type="button" onClick={() => setShowConfirm(!showConfirm)} className="text-gray-500 hover:text-blue-400 transition-colors">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
                          d={showConfirm ? "M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                            : "M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"} />
                      </svg>
                    </button>
                  }
                />

                {/* Submit */}
                <button type="submit" disabled={loading}
                  className="w-full py-3 rounded-xl font-bold tracking-[0.15em] uppercase text-sm text-white transition-all duration-200 flex items-center justify-center gap-2 mt-1 disabled:opacity-60"
                  style={{
                    background: loading ? 'linear-gradient(135deg, #3730a3, #312e81)' : 'linear-gradient(135deg, #4f46e5, #7c3aed)',
                    boxShadow: loading ? 'none' : '0 4px 20px rgba(79,70,229,0.35)',
                  }}>
                  {loading ? (
                    <>
                      <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      Creating Account...
                    </>
                  ) : (
                    <>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                          d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                      </svg>
                      Create Account
                    </>
                  )}
                </button>

                <p className="text-center text-[11px] text-gray-500 font-mono">
                  ALREADY HAVE AN ACCOUNT?{' '}
                  <button type="button" onClick={onNavigateLogin}
                    className="text-blue-400 hover:text-blue-300 font-bold tracking-wider transition-colors">
                    SIGN IN
                  </button>
                </p>
              </form>
            </div>
          )}

          <p className="text-center text-[9px] text-gray-700 font-mono tracking-widest mt-6 uppercase">
            GH Raisoni College · CSE-AI · FYP 2025–26
          </p>
        </div>
      </div>

      <style>{`
        @keyframes progress {
          from { width: 0% }
          to { width: 100% }
        }
      `}</style>
    </div>
  );
};

/* ── Reusable Input Field ── */
const InputField = ({ label, name, type, value, onChange, placeholder, icon, suffix }) => {
  const [focused, setFocused] = useState(false);
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-[10px] font-bold tracking-[0.2em] uppercase text-gray-500 font-mono">{label}</label>
      <div className="flex items-center gap-2 rounded-xl px-3 py-2.5 transition-all duration-200"
        style={{
          background: 'rgba(255,255,255,0.03)',
          border: `1px solid ${focused ? 'rgba(59,130,246,0.5)' : 'rgba(255,255,255,0.07)'}`,
          boxShadow: focused ? '0 0 0 3px rgba(59,130,246,0.08)' : 'none',
        }}>
        <span className={`flex-shrink-0 transition-colors ${focused ? 'text-blue-400' : 'text-gray-600'}`}>{icon}</span>
        <input name={name} type={type} value={value} onChange={onChange}
          onFocus={() => setFocused(true)} onBlur={() => setFocused(false)}
          placeholder={placeholder}
          className="flex-1 bg-transparent text-sm text-gray-200 placeholder-gray-700 outline-none font-mono tracking-wider"
          style={{ caretColor: '#60a5fa' }} />
        {suffix && <span className="flex-shrink-0">{suffix}</span>}
      </div>
    </div>
  );
};

export default Register;