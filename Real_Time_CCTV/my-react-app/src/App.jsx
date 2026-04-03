import React, { useState } from 'react';
import Header from './components/Header';
import CameraGrid from './components/CameraGrid';
import DetectionControl from './components/DetectionControl';
import Login from './pages/Login';
import Register from './pages/Register';

// Pages: 'login' | 'register' | 'dashboard'
function App() {
  const [page, setPage] = useState('login');
  const [user, setUser] = useState(null);

  const handleLogin = (userData) => {
    setUser(userData);
    setPage('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    setPage('login');
  };

  if (page === 'login') {
    return <Login onLogin={handleLogin} onNavigateRegister={() => setPage('register')} />;
  }

  if (page === 'register') {
    return <Register onRegisterSuccess={() => setPage('login')} onNavigateLogin={() => setPage('login')} />;
  }

  // Dashboard
  return (
    <div className="min-h-screen bg-[#060a10] flex flex-col" style={{ fontFamily: "'Rajdhani', sans-serif" }}>
      <Header user={user} onLogout={handleLogout} />
      <div className="h-px bg-gradient-to-r from-transparent via-blue-600/20 to-transparent" />

      <main className="flex-1 p-4 flex gap-4 overflow-hidden">
        <div className="flex-1 min-w-0 flex flex-col gap-4">
          <CameraGrid />
          <div className="flex items-center justify-between px-4 py-2 rounded-xl text-[10px] font-mono text-gray-600 tracking-wider"
            style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.04)' }}>
            <span>GHRCEP · CSE-AI DEPT · FINAL YEAR PROJECT 2025-26</span>
            <span className="flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse inline-block" />
              ALL FEEDS NOMINAL
            </span>
          </div>
        </div>
        <div className="w-72 flex-shrink-0 flex flex-col">
          <DetectionControl />
        </div>
      </main>
    </div>
  );
}

export default App;