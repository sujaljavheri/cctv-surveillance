import React, { useState, useRef } from 'react';

const DetectionControl = () => {
  const [status, setStatus] = useState('stopped'); // 'stopped' | 'running' | 'training'
  const [uploadedImages, setUploadedImages] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  function dataURLtoFile(dataurl, filename) {
  const arr = dataurl.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new File([u8arr], filename, { type: mime });
}

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    const newPreviews = files.map(file => ({ name: file.name, url: URL.createObjectURL(file) }));
    setUploadedImages(prev => [...prev, ...newPreviews].slice(0, 10));
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const files = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'));
    const newPreviews = files.map(file => ({ name: file.name, url: URL.createObjectURL(file) }));
    setUploadedImages(prev => [...prev, ...newPreviews].slice(0, 10));
  };

  // const handleTrainModel = () => {
  //   if (uploadedImages.length === 0) return alert('Please upload at least 3 images first.');
  //   setStatus('training');
  //   setTimeout(() => setStatus('stopped'), 3000);
  // };

  const handleTrainModel = async () => {
  if (uploadedImages.length < 3) {
    alert("Upload at least 3 images");
    return;
  }

  const name = prompt("Enter person's name:");
  if (!name) return;

  setStatus('training');

  const formData = new FormData();
  formData.append("name", name);

  uploadedImages.forEach((img, index) => {
    formData.append("images", dataURLtoFile(img.url, `img${index}.jpg`));
  });

  try {
    const res = await fetch("http://localhost:5000/upload_faces", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    alert(data.message || data.error);
  } catch (err) {
    console.error(err);
    alert("Upload failed");
  }

  setStatus('stopped');
};

  const handleStartDetection = () => setStatus('running');
  const handleStopAndDelete = () => { setStatus('stopped'); setUploadedImages([]); };
  const removeImage = (index) => setUploadedImages(prev => prev.filter((_, i) => i !== index));

  const statusConfig = {
    stopped: {
      label: 'STOPPED',
      sub: 'Detection is currently inactive',
      dot: 'bg-red-500',
      bg: 'bg-red-950/40',
      border: 'border-red-800/40',
      text: 'text-red-400',
      icon: '■',
    },
    running: {
      label: 'RUNNING',
      sub: 'Detection is currently active',
      dot: 'bg-green-400',
      bg: 'bg-green-950/40',
      border: 'border-green-800/40',
      text: 'text-green-400',
      icon: '●',
    },
    training: {
      label: 'TRAINING...',
      sub: 'Model training in progress',
      dot: 'bg-yellow-400',
      bg: 'bg-yellow-950/30',
      border: 'border-yellow-800/40',
      text: 'text-yellow-300',
      icon: '⟳',
    },
  };

  const s = statusConfig[status];

  return (
    <div className="flex flex-col rounded-xl overflow-hidden h-full"
      style={{
        background: 'linear-gradient(160deg, #0c1220 0%, #080d18 100%)',
        border: '1px solid rgba(59,130,246,0.15)',
        boxShadow: '0 4px 24px rgba(0,0,0,0.4)',
      }}>

      {/* Panel Header */}
      <div className="flex items-center gap-2 px-4 py-3"
        style={{ background: 'rgba(0,0,0,0.4)', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
        <div className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
        <h2 className="text-[11px] font-bold tracking-[0.2em] uppercase text-gray-300 font-mono">
          Face Detection Control
        </h2>
      </div>

      <div className="p-4 flex flex-col gap-4 flex-1 overflow-y-auto">

        {/* Status Card */}
        <div className={`rounded-xl p-3.5 flex flex-col items-center gap-1 border ${s.bg} ${s.border}`}>
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${s.dot} animate-pulse`} />
            <span className={`text-base font-bold tracking-widest uppercase font-mono ${s.text}`}>
              {s.label}
            </span>
          </div>
          <span className="text-[10px] text-gray-500 tracking-wider">{s.sub}</span>
        </div>

        {/* Divider */}
        <div className="flex items-center gap-2">
          <div className="flex-1 h-px bg-white/5" />
          <span className="text-[9px] text-gray-600 tracking-[0.2em] uppercase font-mono">Target Images</span>
          <div className="flex-1 h-px bg-white/5" />
        </div>

        {/* Upload Zone */}
        <div
          className={`relative rounded-xl p-5 flex flex-col items-center justify-center gap-2 cursor-pointer transition-all duration-200
            ${isDragging ? 'border-blue-400 bg-blue-900/20' : 'border-white/8 hover:border-blue-500/30 hover:bg-blue-900/10'}`}
          style={{
            border: `2px dashed ${isDragging ? 'rgba(96,165,250,0.7)' : 'rgba(255,255,255,0.08)'}`,
          }}
          onClick={() => fileInputRef.current?.click()}
          onDragOver={e => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
        >
          <div className="w-11 h-11 rounded-full flex items-center justify-center"
            style={{ background: 'radial-gradient(circle, rgba(59,130,246,0.2) 0%, rgba(99,102,241,0.1) 100%)', border: '1px solid rgba(59,130,246,0.25)' }}>
            <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.8}
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
          </div>
          <div className="text-center">
            <p className="text-xs font-semibold text-gray-300">Click to Upload Images</p>
            <p className="text-[10px] text-gray-600 mt-0.5">Upload 3–10 images of the person</p>
          </div>
          <input ref={fileInputRef} type="file" multiple accept="image/*" className="hidden" onChange={handleFileChange} />
        </div>

        {/* Image Previews */}
        {uploadedImages.length > 0 && (
          <div>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-1.5">
                <span className="text-[10px] text-gray-500 font-mono">{uploadedImages.length}/10</span>
                <div className="flex gap-0.5">
                  {Array.from({ length: 10 }).map((_, i) => (
                    <div key={i} className={`w-2 h-1 rounded-full ${i < uploadedImages.length ? 'bg-blue-500' : 'bg-gray-700'}`} />
                  ))}
                </div>
              </div>
              <button onClick={() => setUploadedImages([])}
                className="text-[10px] text-red-400/70 hover:text-red-400 transition-colors font-mono">
                clear all
              </button>
            </div>
            <div className="grid grid-cols-5 gap-1.5">
              {uploadedImages.map((img, i) => (
                <div key={i} className="relative group/img">
                  <img src={img.url} alt="" className="w-full h-11 object-cover rounded-lg border border-white/8" />
                  <div className="absolute inset-0 bg-black/0 group-hover/img:bg-black/40 transition-all rounded-lg" />
                  <button onClick={() => removeImage(i)}
                    className="absolute top-0.5 right-0.5 w-3.5 h-3.5 bg-red-600 rounded-full text-white text-[8px] hidden group-hover/img:flex items-center justify-center">
                    ×
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Spacer */}
        <div className="flex-1" />

        {/* Divider */}
        <div className="h-px bg-white/5" />

        {/* Action Buttons */}
        <div className="flex flex-col gap-2">
          <ActionButton
            onClick={handleTrainModel}
            disabled={status === 'training'}
            gradient="linear-gradient(135deg, #4f46e5, #7c3aed)"
            hoverGlow="rgba(99,102,241,0.35)"
            icon={
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            }
            label="Train Model"
          />

          <ActionButton
            onClick={handleStartDetection}
            disabled={status === 'running' || status === 'training'}
            gradient="linear-gradient(135deg, #15803d, #166534)"
            hoverGlow="rgba(34,197,94,0.3)"
            icon={
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            }
            label="Start Detection"
          />

          <ActionButton
            onClick={handleStopAndDelete}
            gradient="linear-gradient(135deg, #b91c1c, #991b1b)"
            hoverGlow="rgba(239,68,68,0.3)"
            icon={
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            }
            label="Stop & Delete Data"
          />
        </div>

        {/* Footer note */}
        <p className="text-center text-[9px] text-gray-700 font-mono tracking-wider">
          GH RAISONI · CSE-AI · FYP 2026
        </p>
      </div>
    </div>
  );
};

const ActionButton = ({ onClick, disabled, gradient, hoverGlow, icon, label }) => {
  const [hovered, setHovered] = useState(false);

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      className="w-full py-2.5 rounded-xl text-[11px] font-bold tracking-[0.15em] uppercase text-white disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-all duration-200"
      style={{
        background: gradient,
        boxShadow: hovered && !disabled ? `0 0 20px ${hoverGlow}, 0 4px 12px rgba(0,0,0,0.3)` : '0 2px 8px rgba(0,0,0,0.3)',
        transform: hovered && !disabled ? 'translateY(-1px)' : 'none',
      }}
    >
      {icon}
      {label}
    </button>
  );
};

export default DetectionControl;