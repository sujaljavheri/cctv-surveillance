import React, { useState, useEffect } from 'react';

const Header = ({ user, onLogout }) => {
  const [dateTime, setDateTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setDateTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatDate = (date) =>
    date.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });

  const formatTime = (date) =>
    date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });

  return (
    <header
      className="relative bg-[#080c14] border-b border-blue-900/30 px-5 flex items-center justify-between overflow-hidden"
      style={{ minHeight: '56px' }}
    >
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-blue-500/40 to-transparent" />
      </div>

      {/* LEFT */}
      <div className="flex items-center gap-3 z-10">
        <div className="relative w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-700 flex items-center justify-center shadow-lg shadow-blue-900/50 flex-shrink-0">
          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
              d="M15 10l4.553-2.069A1 1 0 0121 8.82v6.36a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <span className="absolute -top-1 -right-1 w-2 h-2 rounded-full bg-green-400 border border-[#080c14] animate-pulse" />
        </div>
        <div>
          <h1 className="text-base font-bold tracking-wide text-white leading-tight whitespace-nowrap">
            CCTV Face Recognition System
          </h1>
          <p className="text-[9px] text-blue-400/60 tracking-[0.2em] uppercase font-mono">
            Real-Time Surveillance Dashboard
          </p>
        </div>
      </div>

      {/* CENTER */}
      <div className="hidden md:flex items-center gap-5 z-10">
        <Stat value="4" label="Cameras" color="text-cyan-400" />
        <div className="w-px h-6 bg-white/5" />
        <Stat value="AI" label="Active" color="text-purple-400" />
        <div className="w-px h-6 bg-white/5" />
        <Stat value="30" label="FPS" color="text-yellow-400" />
        <div className="w-px h-6 bg-white/5" />
        <Stat value="97%" label="Accuracy" color="text-green-400" />
      </div>

      {/* RIGHT */}
      <div className="flex items-center gap-3 z-10">
        <div className="hidden sm:flex items-center gap-1.5 bg-green-900/20 border border-green-800/40 rounded-full px-2.5 py-1">
          <span className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
          <span className="text-[10px] text-green-400 font-mono tracking-wider font-semibold">ONLINE</span>
        </div>
        <div className="w-px h-7 bg-white/5" />
        <div className="text-right">
          <div className="text-sm font-mono font-bold text-blue-300 tracking-wider tabular-nums">
            {formatTime(dateTime)}
          </div>
          <div className="text-[9px] text-gray-500 font-mono tracking-wide">
            {formatDate(dateTime)}
          </div>
        </div>
        {user && (
          <>
            <div className="w-px h-7 bg-white/5" />
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center flex-shrink-0">
                <span className="text-[11px] font-bold text-white">
                  {user.name ? user.name[0].toUpperCase() : user.email[0].toUpperCase()}
                </span>
              </div>
              <div className="hidden sm:block">
                <p className="text-[11px] font-bold text-gray-300 leading-tight">{user.name || user.email}</p>
                <p className="text-[9px] text-gray-600 font-mono tracking-wider">{user.role || 'USER'}</p>
              </div>
              <button onClick={onLogout}
                className="ml-1 w-7 h-7 rounded-lg flex items-center justify-center text-gray-600 hover:text-red-400 hover:bg-red-900/20 transition-all"
                title="Logout">
                <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </>
        )}
      </div>
    </header>
  );
};

const Stat = ({ value, label, color }) => (
  <div className="flex flex-col items-center">
    <span className={`text-xs font-bold font-mono ${color}`}>{value}</span>
    <span className="text-[9px] text-gray-500 tracking-wider uppercase">{label}</span>
  </div>
);

export default Header;