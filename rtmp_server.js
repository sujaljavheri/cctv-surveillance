/**
 * rtmp_server.js — Local RTMP server
 * Receives OBS stream and makes it available to server.py
 *
 * Install: npm install node-media-server
 * Run:     node rtmp_server.js
 *
 * Then in OBS:
 *   Settings → Stream → Custom
 *   Server:     rtmp://localhost/live
 *   Stream Key: stream1
 *
 * Add to camera_config.py:
 *   "type":   "rtsp",
 *   "source": "rtmp://localhost/live/stream1"
 */

const NodeMediaServer = require('node-media-server');

const config = {
    rtmp: {
        port:      1935,       // standard RTMP port
        chunk_size: 60000,
        gop_cache:  true,
        ping:       30,
        ping_timeout: 60,
    },
    http: {
        port:       8000,      // HTTP-FLV playback port
        allow_origin: '*',     // allow CCTV dashboard to access
        mediaroot:  './media',
    },
};

const nms = new NodeMediaServer(config);

nms.on('preConnect', (id, args) => {
    console.log('[RTMP] Client connecting:', id, args.ip);
});

nms.on('postConnect', (id, args) => {
    console.log('[RTMP] Client connected:', id);
});

nms.on('prePublish', (id, StreamPath, args) => {
    console.log('[RTMP] Stream starting:', StreamPath);
    console.log('[RTMP] Now available at: rtmp://localhost' + StreamPath);
    console.log('[RTMP] Add this URL to camera_config.py as the source');
});

nms.on('postPublish', (id, StreamPath, args) => {
    console.log('[RTMP] Stream live:', StreamPath);
});

nms.on('donePublish', (id, StreamPath, args) => {
    console.log('[RTMP] Stream ended:', StreamPath);
});

nms.on('prePlay', (id, StreamPath, args) => {
    console.log('[RTMP] Viewer connected:', StreamPath);
});

nms.run();

console.log('');
console.log('╔══════════════════════════════════════════════╗');
console.log('║         Local RTMP Server Running            ║');
console.log('╠══════════════════════════════════════════════╣');
console.log('║  RTMP port : 1935                            ║');
console.log('║  HTTP port : 8000                            ║');
console.log('╠══════════════════════════════════════════════╣');
console.log('║  OBS Settings → Stream:                      ║');
console.log('║    Service    : Custom                       ║');
console.log('║    Server     : rtmp://localhost/live        ║');
console.log('║    Stream Key : stream1                      ║');
console.log('╠══════════════════════════════════════════════╣');
console.log('║  camera_config.py source URL:                ║');
console.log('║  rtmp://localhost/live/stream1               ║');
console.log('╚══════════════════════════════════════════════╝');
console.log('');
console.log('Waiting for OBS to connect...');