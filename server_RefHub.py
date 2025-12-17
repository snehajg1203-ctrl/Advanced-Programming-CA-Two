# server_RefHub.py - Web Server for StudentConnect Frontend
"""
This server handles the web interface (HTML frontend)
Run this for web-based access
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.')
app.secret_key = 'studentconnect-refhub-2025'
CORS(app)

@app.route('/')
def index():
    """Serve the main candidate/student interface"""
    if os.path.exists('candidate_frontend_rt.html'):
        return send_from_directory('.', 'candidate_frontend_rt.html')
    return "<h1>Frontend not found</h1><p>Please ensure candidate_frontend_rt.html exists</p>"

@app.route('/admin')
def admin():
    """Serve the admin interface"""
    if os.path.exists('admin_frontend_rt.html'):
        return send_from_directory('.', 'admin_frontend_rt.html')
    return "<h1>Admin frontend not found</h1><p>Please ensure admin_frontend_rt.html exists</p>"

@app.route('/student')
def student():
    """Serve the student interface"""
    if os.path.exists('candidate_frontend_rt.html'):
        return send_from_directory('.', 'candidate_frontend_rt.html')
    return "<h1>Student frontend not found</h1>"

@app.route('/employer')
def employer():
    """Serve the employer interface"""
    if os.path.exists('candidate_frontend_rt.html'):
        return send_from_directory('.', 'candidate_frontend_rt.html')
    return "<h1>Employer frontend not found</h1>"

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'message': 'RefHub server is running'}

if __name__ == '__main__':
    print("="*70)
    print("STUDENTCONNECT - REFHUB WEB SERVER")
    print("="*70)
    print("\nThis server serves the HTML frontend files.")
    print("Make sure app_backend.py is running on port 5000 for API calls!")
    print("\n📱 Access Points:")
    print("   Student/Employer Portal: http://localhost:8080/")
    print("   Admin Dashboard:         http://localhost:8080/admin")
    print("\n⚠️  Important: Backend API must be running on port 5000")
    print("   Start it with: python app_backend.py")
    print("\n⌨️  Press CTRL+C to stop this server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)