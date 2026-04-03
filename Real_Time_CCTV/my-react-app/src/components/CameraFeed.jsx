// import React, { useState, useEffect } from 'react';

// const CameraFeed = ({ id, name }) => {
//   const [time, setTime] = useState(new Date());

//   useEffect(() => {
//     const t = setInterval(() => setTime(new Date()), 1000);
//     return () => clearInterval(t);
//   }, []);

//   // Simulated signal strength (static per camera)
//   const signal = [4, 3, 4, 3][id - 1];

//   return (
//     <div className="group relative rounded-xl overflow-hidden flex flex-col"
//       style={{
//         background: 'linear-gradient(145deg, #0f1729 0%, #0a1020 100%)',
//         border: '1px solid rgba(59,130,246,0.15)',
//         boxShadow: '0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03)',
//         transition: 'border-color 0.3s, box-shadow 0.3s',
//       }}
//       onMouseEnter={e => {
//         e.currentTarget.style.borderColor = 'rgba(59,130,246,0.4)';
//         e.currentTarget.style.boxShadow = '0 4px 32px rgba(0,0,0,0.5), 0 0 20px rgba(59,130,246,0.08), inset 0 1px 0 rgba(255,255,255,0.04)';
//       }}
//       onMouseLeave={e => {
//         e.currentTarget.style.borderColor = 'rgba(59,130,246,0.15)';
//         e.currentTarget.style.boxShadow = '0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03)';
//       }}
//     >
//       {/* ── Header Bar ── */}
//       <div className="flex items-center justify-between px-3 py-2"
//         style={{ background: 'rgba(0,0,0,0.5)', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
//         <div className="flex items-center gap-2">
//           <svg className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
//               d="M15 10l4.553-2.069A1 1 0 0121 8.82v6.36a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
//           </svg>
//           <span className="text-[11px] font-bold text-gray-200 tracking-wider uppercase font-mono">{name}</span>
//         </div>

//         <div className="flex items-center gap-3">
//           {/* Signal bars */}
//           <div className="flex items-end gap-0.5 h-3">
//             {[1,2,3,4].map(i => (
//               <div key={i}
//                 className={`w-1 rounded-sm ${i <= signal ? 'bg-green-400' : 'bg-gray-700'}`}
//                 style={{ height: `${i * 3}px` }}
//               />
//             ))}
//           </div>

//           {/* Live badge */}
//           <div className="flex items-center gap-1 bg-green-500/10 border border-green-500/30 rounded-full px-2 py-0.5">
//             <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse" />
//             <span className="text-[9px] font-bold text-green-400 tracking-widest">LIVE</span>
//           </div>
//         </div>
//       </div>

//       {/* ── Feed Area ── */}
//       <div className="relative flex-1 flex items-center justify-center overflow-hidden" style={{ minHeight: '160px' }}>
//         {/* Background gradient */}
//         <div className="absolute inset-0"
//           style={{
//             background: `radial-gradient(ellipse at 30% 40%, rgba(30,58,138,0.18) 0%, transparent 60%),
//                          radial-gradient(ellipse at 70% 70%, rgba(67,20,128,0.12) 0%, transparent 60%),
//                          linear-gradient(160deg, #0e1a30 0%, #080d1a 100%)`
//           }} />

//         {/* Subtle grid */}
//         <div className="absolute inset-0 opacity-[0.06]"
//           style={{
//             backgroundImage: `linear-gradient(rgba(99,179,237,1) 1px, transparent 1px),
//                                linear-gradient(90deg, rgba(99,179,237,1) 1px, transparent 1px)`,
//             backgroundSize: '36px 36px'
//           }} />

//         {/* Scan line sweep */}
//         <div className="absolute inset-0 overflow-hidden pointer-events-none">
//           <div className="absolute left-0 right-0 h-12 opacity-[0.04]"
//             style={{
//               background: 'linear-gradient(to bottom, transparent, rgba(99,179,237,0.8), transparent)',
//               animation: 'scanline 5s linear infinite',
//             }} />
//         </div>

//         {/* Corner brackets */}
//         {[
//           'top-2 left-2 border-t-2 border-l-2',
//           'top-2 right-2 border-t-2 border-r-2',
//           'bottom-2 left-2 border-b-2 border-l-2',
//           'bottom-2 right-2 border-b-2 border-r-2',
//         ].map((cls, i) => (
//           <div key={i} className={`absolute w-4 h-4 border-blue-400/40 ${cls}`} />
//         ))}

//         {/* Center icon */}
//         <div className="relative z-10 flex flex-col items-center gap-2 opacity-25 group-hover:opacity-40 transition-opacity duration-300">
//           <svg className="w-12 h-12 text-blue-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
//             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={0.8}
//               d="M15 10l4.553-2.069A1 1 0 0121 8.82v6.36a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
//           </svg>
//           <span className="text-[10px] text-blue-300/80 tracking-[0.3em] font-mono">CAM {String(id).padStart(2,'0')}</span>
//         </div>

//         {/* REC badge */}
//         <div className="absolute top-3 left-3 flex items-center gap-1.5 bg-red-950/80 border border-red-800/50 rounded px-1.5 py-0.5 backdrop-blur-sm">
//           <div className="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse" />
//           <span className="text-[9px] font-bold text-red-300 tracking-widest font-mono">REC</span>
//         </div>

//         {/* Cam ID top right */}
//         <div className="absolute top-3 right-3 text-[9px] text-blue-400/50 font-mono tracking-wider">
//           CH-0{id}
//         </div>

//         {/* Bottom bar */}
//         <div className="absolute bottom-0 left-0 right-0 flex items-center justify-between px-3 py-1.5"
//           style={{ background: 'rgba(0,0,0,0.6)', borderTop: '1px solid rgba(255,255,255,0.03)' }}>
//           <span className="text-[9px] text-blue-300/50 font-mono tracking-wider tabular-nums">
//             {time.toLocaleTimeString('en-US', { hour12: false })}
//           </span>
//           <div className="flex items-center gap-2">
//             <span className="text-[9px] text-gray-600 font-mono">30 FPS</span>
//             <span className="text-[9px] text-blue-400/40 font-mono">1080p</span>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default CameraFeed;


import React, { useState, useEffect, useRef } from 'react';

const CameraFeed = ({ id, name, streamUrl }) => {
  const [time, setTime]         = useState(new Date());
  const [status, setStatus]     = useState('connecting'); // 'connecting' | 'live' | 'error'
  const imgRef                  = useRef(null);
  const signal                  = [4, 3, 4, 3][id - 1] ?? 3;

  // Clock
  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  // Detect when the MJPEG stream loads or errors
  const handleLoad  = () => setStatus('live');
  const handleError = () => setStatus('error');

  return (
    <div
      className="group relative rounded-xl overflow-hidden flex flex-col"
      style={{
        background: 'linear-gradient(145deg, #0f1729 0%, #0a1020 100%)',
        border: `1px solid ${status === 'live' ? 'rgba(59,130,246,0.3)' : 'rgba(59,130,246,0.15)'}`,
        boxShadow: '0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03)',
        transition: 'border-color 0.3s, box-shadow 0.3s',
      }}
      onMouseEnter={e => {
        e.currentTarget.style.borderColor = 'rgba(59,130,246,0.5)';
        e.currentTarget.style.boxShadow   = '0 4px 32px rgba(0,0,0,0.5), 0 0 20px rgba(59,130,246,0.1)';
      }}
      onMouseLeave={e => {
        e.currentTarget.style.borderColor = status === 'live' ? 'rgba(59,130,246,0.3)' : 'rgba(59,130,246,0.15)';
        e.currentTarget.style.boxShadow   = '0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03)';
      }}
    >
      {/* ── Header Bar ── */}
      <div
        className="flex items-center justify-between px-3 py-2"
        style={{ background: 'rgba(0,0,0,0.5)', borderBottom: '1px solid rgba(255,255,255,0.04)' }}
      >
        <div className="flex items-center gap-2">
          <svg className="w-3.5 h-3.5 text-blue-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
              d="M15 10l4.553-2.069A1 1 0 0121 8.82v6.36a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
          </svg>
          <span className="text-[11px] font-bold text-gray-200 tracking-wider uppercase font-mono">{name}</span>
        </div>

        <div className="flex items-center gap-3">
          {/* Signal bars */}
          <div className="flex items-end gap-0.5 h-3">
            {[1, 2, 3, 4].map(i => (
              <div
                key={i}
                className={`w-1 rounded-sm ${i <= signal ? 'bg-green-400' : 'bg-gray-700'}`}
                style={{ height: `${i * 3}px` }}
              />
            ))}
          </div>

          {/* Live / Error / Connecting badge */}
          {status === 'live' && (
            <div className="flex items-center gap-1 bg-green-500/10 border border-green-500/30 rounded-full px-2 py-0.5">
              <div className="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"/>
              <span className="text-[9px] font-bold text-green-400 tracking-widest">LIVE</span>
            </div>
          )}
          {status === 'connecting' && (
            <div className="flex items-center gap-1 bg-yellow-500/10 border border-yellow-500/30 rounded-full px-2 py-0.5">
              <div className="w-1.5 h-1.5 rounded-full bg-yellow-400 animate-pulse"/>
              <span className="text-[9px] font-bold text-yellow-400 tracking-widest">CONNECTING</span>
            </div>
          )}
          {status === 'error' && (
            <div className="flex items-center gap-1 bg-red-500/10 border border-red-500/30 rounded-full px-2 py-0.5">
              <div className="w-1.5 h-1.5 rounded-full bg-red-400"/>
              <span className="text-[9px] font-bold text-red-400 tracking-widest">NO SIGNAL</span>
            </div>
          )}
        </div>
      </div>

      {/* ── Feed Area ── */}
      <div className="relative flex-1 overflow-hidden" style={{ minHeight: '160px' }}>

        {/* Real MJPEG stream */}
        {streamUrl && (
          <img
            ref={imgRef}
            src={streamUrl}
            alt={`Camera ${id} feed`}
            onLoad={handleLoad}
            onError={handleError}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              display: status === 'error' ? 'none' : 'block',
            }}
          />
        )}

        {/* Placeholder shown while connecting or on error */}
        {(status === 'connecting' || status === 'error' || !streamUrl) && (
          <div
            className="absolute inset-0 flex flex-col items-center justify-center"
            style={{
              background: `radial-gradient(ellipse at 30% 40%, rgba(30,58,138,0.18) 0%, transparent 60%),
                           linear-gradient(160deg, #0e1a30 0%, #080d1a 100%)`
            }}
          >
            {/* Grid overlay */}
            <div
              className="absolute inset-0 opacity-[0.06]"
              style={{
                backgroundImage: `linear-gradient(rgba(99,179,237,1) 1px, transparent 1px),
                                   linear-gradient(90deg, rgba(99,179,237,1) 1px, transparent 1px)`,
                backgroundSize: '36px 36px'
              }}
            />
            {/* Corner brackets */}
            {[
              'top-2 left-2 border-t-2 border-l-2',
              'top-2 right-2 border-t-2 border-r-2',
              'bottom-2 left-2 border-b-2 border-l-2',
              'bottom-2 right-2 border-b-2 border-r-2',
            ].map((cls, i) => (
              <div key={i} className={`absolute w-4 h-4 border-blue-400/40 ${cls}`}/>
            ))}

            <svg className="w-10 h-10 text-blue-300 opacity-20 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={0.8}
                d="M15 10l4.553-2.069A1 1 0 0121 8.82v6.36a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"/>
            </svg>

            <span className="text-[10px] text-blue-300/40 tracking-[0.3em] font-mono relative z-10 mt-2">
              {status === 'error' ? 'NO SIGNAL' : 'CAM ' + String(id).padStart(2, '0')}
            </span>
            {status === 'error' && (
              <span className="text-[9px] text-red-400/60 font-mono mt-1 relative z-10">
                Check server.py is running
              </span>
            )}
          </div>
        )}

        {/* REC badge (only when live) */}
        {status === 'live' && (
          <div className="absolute top-2 left-2 flex items-center gap-1.5 bg-red-950/80 border border-red-800/50 rounded px-1.5 py-0.5 backdrop-blur-sm">
            <div className="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"/>
            <span className="text-[9px] font-bold text-red-300 tracking-widest font-mono">REC</span>
          </div>
        )}

        {/* CH-0X badge */}
        <div className="absolute top-2 right-2 text-[9px] text-blue-400/50 font-mono tracking-wider">
          CH-0{id}
        </div>

        {/* Bottom bar */}
        <div
          className="absolute bottom-0 left-0 right-0 flex items-center justify-between px-3 py-1.5"
          style={{ background: 'rgba(0,0,0,0.6)', borderTop: '1px solid rgba(255,255,255,0.03)' }}
        >
          <span className="text-[9px] text-blue-300/50 font-mono tracking-wider tabular-nums">
            {time.toLocaleTimeString('en-US', { hour12: false })}
          </span>
          <div className="flex items-center gap-2">
            <span className="text-[9px] text-gray-600 font-mono">30 FPS</span>
            <span className="text-[9px] text-blue-400/40 font-mono">1080p</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CameraFeed;