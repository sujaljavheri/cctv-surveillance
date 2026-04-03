import React from 'react';
import CameraFeed from './CameraFeed';

// ================================================================
// CAMERA CONFIGURATION
// Change streamUrl to match your actual camera sources:
//   - Local webcam served by server.py:  http://localhost:5000/video_feed/0
//   - Another PC on same network:        http://192.168.1.X:5000/video_feed/0
//   - Different camera index:            http://localhost:5000/video_feed/1
// ================================================================
const FLASK_BASE = 'http://localhost:5000';

const cameras = [
  { id: 1, name: 'Camera 1 — Main Entrance', streamUrl: `${FLASK_BASE}/video_feed/0` },
  { id: 2, name: 'Camera 2 — Parking Area',  streamUrl: `${FLASK_BASE}/video_feed/1` },
  { id: 3, name: 'Camera 3 — Side Gate',     streamUrl: `${FLASK_BASE}/video_feed/2` },
  { id: 4, name: 'Camera 4 — Back Exit',     streamUrl: `${FLASK_BASE}/video_feed/3` },
];

const CameraGrid = () => {
  return (
    <div className="grid grid-cols-2 gap-4 flex-1">
      {cameras.map((cam) => (
        <CameraFeed
          key={cam.id}
          id={cam.id}
          name={cam.name}
          streamUrl={cam.streamUrl}
        />
      ))}
    </div>
  );
};

export default CameraGrid;