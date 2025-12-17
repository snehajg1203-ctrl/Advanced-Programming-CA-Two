# app_backend.py - Flask Backend for StudentConnect
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pyodbc
import hashlib
from datetime import datetime

app = Flask(__name__, static_folder='.')
app.secret_key = 'studentconnect-secret-key-2025'
CORS(app)

# Database Configuration
DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': 'localhost',
    'database': 'StudentConnectDB',
    'trusted_connection': 'yes'
}

def get_db_connection():
    """Create and return database connection"""
    conn_str = (
        f"DRIVER={DB_CONFIG['driver']};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"Trusted_Connection={DB_CONFIG['trusted_connection']};"
    )
    return pyodbc.connect(conn_str)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# ==================== SERVE HTML FILES ====================

@app.route('/')
def index():
    """Serve main application"""
    return send_from_directory('.', 'candidate_frontend_rt.html')

@app.route('/admin')
def admin():
    """Serve admin interface"""
    return send_from_directory('.', 'admin_frontend_rt.html')

@app.route('/student')
def student():
    """Serve student interface"""
    return send_from_directory('.', 'candidate_frontend_rt.html')

# ==================== ADMIN ENDPOINTS ====================

@app.route('/api/admin/users', methods=['GET'])
def get_all_users():
    """Get all users (admin only)"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get students
        cursor.execute('''
            SELECT student_id, full_name, email, phone, university, major, gpa, created_at, 'student' as type
            FROM Students
        ''')
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'id': int(row[0]),
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'university': row[4],
                'major': row[5],
                'gpa': float(row[6]) if row[6] else None,
                'created_at': row[7].isoformat() if row[7] else None,
                'type': row[8]
            })
        
        # Get employers
        cursor.execute('''
            SELECT employer_id, company_name, email, phone, industry, company_size, created_at, 'employer' as type
            FROM Employers
        ''')
        
        for row in cursor.fetchall():
            users.append({
                'id': int(row[0]),
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'industry': row[4],
                'company_size': row[5],
                'created_at': row[6].isoformat() if row[6] else None,
                'type': row[7]
            })
        
        conn.close()
        return jsonify({'success': True, 'users': users}), 200
        
    except Exception as e:
        print(f"Error getting users: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== AUTHENTICATION ====================

@app.route('/api/auth/register/student', methods=['POST'])
def register_student():
    """Register a new student"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(data['password'])
        
        cursor.execute('''
            INSERT INTO Students (full_name, email, password_hash, phone, university, major, gpa)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['email'], password_hash,
              data.get('phone'), data.get('university'), data.get('major'), data.get('gpa')))
        
        conn.commit()
        cursor.execute('SELECT @@IDENTITY')
        user_id = int(cursor.fetchone()[0])
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': {'id': user_id, 'name': data['name'], 'email': data['email'], 'type': 'student'}
        }), 201
        
    except pyodbc.IntegrityError:
        return jsonify({'success': False, 'message': 'Email already exists'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/register/employer', methods=['POST'])
def register_employer():
    """Register a new employer"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(data['password'])
        
        cursor.execute('''
            INSERT INTO Employers (company_name, contact_person, email, password_hash, phone, industry, company_size)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['company'], data.get('contact_person', ''), data['email'], password_hash, 
              data.get('phone'), data.get('industry'), data.get('company_size')))
        
        conn.commit()
        cursor.execute('SELECT @@IDENTITY')
        user_id = int(cursor.fetchone()[0])
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': {'id': user_id, 'name': data['company'], 'email': data['email'], 'type': 'employer'}
        }), 201
        
    except pyodbc.IntegrityError:
        return jsonify({'success': False, 'message': 'Email already exists'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/login/student', methods=['POST'])
def login_student():
    """Student login"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(data['password'])
        
        cursor.execute('''
            SELECT student_id, full_name, email, phone, university, major, gpa, skills, created_at
            FROM Students
            WHERE email = ? AND password_hash = ?
        ''', (data['email'], password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'user': {
                    'id': int(result[0]),
                    'name': result[1],
                    'email': result[2],
                    'phone': result[3],
                    'university': result[4],
                    'major': result[5],
                    'gpa': float(result[6]) if result[6] else None,
                    'skills': result[7],
                    'type': 'student',
                    'created_at': result[8].isoformat() if result[8] else None
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/auth/login/employer', methods=['POST'])
def login_employer():
    """Employer login"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(data['password'])
        
        cursor.execute('''
            SELECT employer_id, company_name, email, phone, contact_person, created_at
            FROM Employers
            WHERE email = ? AND password_hash = ?
        ''', (data['email'], password_hash))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return jsonify({
                'success': True,
                'user': {
                    'id': int(result[0]),
                    'name': result[1],
                    'email': result[2],
                    'phone': result[3],
                    'contact_person': result[4],
                    'type': 'employer',
                    'created_at': result[5].isoformat() if result[5] else None
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== JOBS ====================

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT j.job_id, j.title, j.company, j.job_type, j.location, j.salary, j.hours,
                   j.description, j.required_skills, j.posted, j.employer_id, j.created_at
            FROM Jobs j
            ORDER BY j.created_at DESC
        ''')
        
        jobs = []
        for row in cursor.fetchall():
            jobs.append({
                'id': int(row[0]),
                'title': row[1],
                'company': row[2],
                'type': row[3],
                'location': row[4],
                'salary': row[5],
                'hours': row[6],
                'description': row[7],
                'skills': row[8].split(',') if row[8] else [],
                'posted': row[9],
                'employer_id': int(row[10]) if row[10] else None
            })
        
        conn.close()
        return jsonify({'success': True, 'jobs': jobs}), 200
        
    except Exception as e:
        print(f"Error getting jobs: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        skills_str = ','.join(data.get('skills', [])) if isinstance(data.get('skills'), list) else data.get('skills', '')
        
        cursor.execute('''
            INSERT INTO Jobs (title, company, job_type, location, salary, hours, 
                            description, required_skills, posted, employer_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['title'], data['company'], data.get('type'), data.get('location'),
              data.get('salary'), data.get('hours'), data.get('description'),
              skills_str, 'Just now', data.get('employer_id')))
        
        conn.commit()
        cursor.execute('SELECT @@IDENTITY')
        job_id = int(cursor.fetchone()[0])
        conn.close()
        
        return jsonify({'success': True, 'message': 'Job created successfully', 'job_id': job_id}), 201
        
    except Exception as e:
        print(f"Error creating job: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== APPLICATIONS ====================

@app.route('/api/applications', methods=['GET'])
def get_applications():
    """Get all applications or filter by student"""
    try:
        student_id = request.args.get('student_id', type=int)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if student_id:
            cursor.execute('''
                SELECT application_id, job_id, student_id, job_title, company, applied_date, status
                FROM Applications
                WHERE student_id = ?
                ORDER BY applied_date DESC
            ''', (student_id,))
        else:
            cursor.execute('''
                SELECT application_id, job_id, student_id, job_title, company, applied_date, status
                FROM Applications
                ORDER BY applied_date DESC
            ''')
        
        applications = []
        for row in cursor.fetchall():
            applications.append({
                'id': int(row[0]),
                'job_id': int(row[1]),
                'student_id': int(row[2]),
                'job_title': row[3],
                'company': row[4],
                'applied_date': row[5].isoformat() if row[5] else None,
                'status': row[6]
            })
        
        conn.close()
        return jsonify({'success': True, 'applications': applications}), 200
        
    except Exception as e:
        print(f"Error getting applications: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/applications', methods=['POST'])
def submit_application():
    """Submit a job application"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT application_id FROM Applications WHERE job_id = ? AND student_id = ?
        ''', (data['job_id'], data['student_id']))
        
        if cursor.fetchone():
            return jsonify({'success': False, 'message': 'Already applied to this job'}), 400
        
        cursor.execute('''
            INSERT INTO Applications (job_id, student_id, job_title, company, cover_letter)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['job_id'], data['student_id'], data.get('job_title'), 
              data.get('company'), data.get('cover_letter')))
        
        conn.commit()
        cursor.execute('SELECT @@IDENTITY')
        app_id = int(cursor.fetchone()[0])
        conn.close()
        
        return jsonify({'success': True, 'message': 'Application submitted successfully', 'application_id': app_id}), 201
        
    except Exception as e:
        print(f"Error submitting application: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/applications/student/<int:student_id>', methods=['GET'])
def get_student_applications(student_id):
    """Get all applications for a student"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT application_id, job_id, job_title, company, applied_date, status
            FROM Applications
            WHERE student_id = ?
            ORDER BY applied_date DESC
        ''', (student_id,))
        
        applications = []
        for row in cursor.fetchall():
            applications.append({
                'id': int(row[0]),
                'job_id': int(row[1]),
                'job_title': row[2],
                'company': row[3],
                'applied_date': row[4].isoformat() if row[4] else None,
                'status': row[5]
            })
        
        conn.close()
        return jsonify({'success': True, 'applications': applications}), 200
        
    except Exception as e:
        print(f"Error getting student applications: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== REFERENCES ====================

@app.route('/api/references', methods=['GET'])
def get_references():
    """Get all references or filter by student"""
    try:
        student_id = request.args.get('student_id', type=int)
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if student_id:
            cursor.execute('''
                SELECT reference_id, student_id, referee_name, referee_email, referee_phone, relationship,
                       company, position, status, request_date, response_date, rating
                FROM StudentReferences
                WHERE student_id = ?
                ORDER BY request_date DESC
            ''', (student_id,))
        else:
            cursor.execute('''
                SELECT reference_id, student_id, referee_name, referee_email, referee_phone, relationship,
                       company, position, status, request_date, response_date, rating
                FROM StudentReferences
                ORDER BY request_date DESC
            ''')
        
        references = []
        for row in cursor.fetchall():
            references.append({
                'id': int(row[0]),
                'student_id': int(row[1]),
                'referee_name': row[2],
                'referee_email': row[3],
                'referee_phone': row[4],
                'relationship': row[5],
                'company': row[6],
                'position': row[7],
                'status': row[8],
                'request_date': row[9].isoformat() if row[9] else None,
                'response_date': row[10].isoformat() if row[10] else None,
                'rating': int(row[11]) if row[11] else None
            })
        
        conn.close()
        return jsonify({'success': True, 'references': references}), 200
        
    except Exception as e:
        print(f"Error getting references: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/references', methods=['POST'])
def request_reference():
    """Request a new reference"""
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO StudentReferences (student_id, referee_name, referee_email, referee_phone,
                                    relationship, company, position)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['student_id'], data['referee_name'], data['referee_email'],
              data.get('referee_phone'), data.get('relationship'), data.get('company'),
              data.get('position')))
        
        conn.commit()
        cursor.execute('SELECT @@IDENTITY')
        ref_id = int(cursor.fetchone()[0])
        conn.close()
        
        return jsonify({'success': True, 'message': 'Reference request sent', 'reference_id': ref_id}), 201
        
    except Exception as e:
        print(f"Error requesting reference: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/references/student/<int:student_id>', methods=['GET'])
def get_student_references(student_id):
    """Get all references for a student"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT reference_id, referee_name, referee_email, referee_phone, relationship,
                   company, position, status, request_date, response_date, rating
            FROM StudentReferences
            WHERE student_id = ?
            ORDER BY request_date DESC
        ''', (student_id,))
        
        references = []
        for row in cursor.fetchall():
            references.append({
                'id': int(row[0]),
                'referee_name': row[1],
                'referee_email': row[2],
                'referee_phone': row[3],
                'relationship': row[4],
                'company': row[5],
                'position': row[6],
                'status': row[7],
                'request_date': row[8].isoformat() if row[8] else None,
                'response_date': row[9].isoformat() if row[9] else None,
                'rating': int(row[10]) if row[10] else None
            })
        
        conn.close()
        return jsonify({'success': True, 'references': references}), 200
        
    except Exception as e:
        print(f"Error getting student references: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'message': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    print("="*60)
    print("STUDENTCONNECT BACKEND SERVER")
    print("="*60)
    print("Server running on: http://localhost:5000")
    print("Student Portal: http://localhost:5000/student")
    print("Admin Portal: http://localhost:5000/admin")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)