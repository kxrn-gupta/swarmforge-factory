"""
Stage 4: Production Dark Factory HTTP Server & REST Telemetry API.
Pure standard library http.server with JSON API endpoints.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
try:
    from .band_connector import BandDesktopConnector
except ImportError:
    from band_connector import BandDesktopConnector

class FactoryHTTPHandler(BaseHTTPRequestHandler):
    connector = BandDesktopConnector()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/status":
            self._send_json(200, {
                "service": "SwarmForge Dark Factory Service",
                "status": "ONLINE",
                "stages_ready": 4,
                "engine": "Python 3.8+ Standard Library"
            })
        elif parsed.path == "/api/band-room":
            telemetry = self.connector.export_room_telemetry()
            self._send_json(200, telemetry)
        elif parsed.path == "/":
            html = """<!DOCTYPE html>
<html>
<head><title>SwarmForge Dark Factory</title></head>
<body style="background:#0d1117;color:#c9d1d9;font-family:sans-serif;padding:2rem;">
<h1>[🏭] SwarmForge Dark Factory Service</h1>
<p>Status: <span style="color:#3fb950;">ONLINE (Stages 1-4 Operational)</span></p>
<p>All 3 BAND seats connected with zero external runtime dependencies.</p>
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
        else:
            self._send_json(404, {"error": "Not Found"})

    def _send_json(self, status: int, data: dict):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        pass # Silence default HTTP request logs during testing

def run_server(port: int = 8090):
    server = HTTPServer(("127.0.0.1", port), FactoryHTTPHandler)
    print(f"Factory service running on http://127.0.0.1:{port}")
    return server
