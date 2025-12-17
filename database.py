# database.py - Database Handler Module
"""
Database operations module for StudentConnect
Handles all database connections and queries
"""

import pyodbc
import logging
from datetime import datetime, timedelta
import hashlib
import uuid
from config import get_connection_string, PASSWORD_SALT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            conn_str = get_connection_string()
            self.connection = pyodbc.connect(conn_str)
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute a database query"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            self.connection.rollback()
            raise
    
    def hash_password(self, password):
        """Hash password with salt"""
        salted = password + PASSWORD_SALT
        return hashlib.sha256(salted.encode()).hexdigest()
    
    def verify_connection(self):
        """Verify database connection is active"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT 1")
            return True
        except:
            return False
    
    # Student Operations
    def create_student(self, student_data):
        """Create a new student account"""
        query = '''
            INSERT INTO Students (full_name, email, password_hash, phone, university, major)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        password_hash = self.hash_password(student_data['password'])
        params = (
            student_data['full_name'],
            student_data['email'],
            password_hash,
            student_data.get('phone'),
            student_data.get('university'),
            student_data.get('major')
        )
        cursor = self.execute_query(query, params)
        cursor.execute('SELECT @@IDENTITY')
        student_id = int(cursor.fetchone()[0])
        return student_id
    
    def authenticate_student(self, email, password):
        """Authenticate student login"""
        query = '''
            SELECT student_id, full_name, email, university, major
            FROM Students
            WHERE email = ? AND password_hash = ?
        '''
        password_hash = self.hash_password(password)
        results = self.execute_query(query, (email, password_hash), fetch=True)
        
        if results:
            row = results[0]
            return {
                'student_id': int(row[0]),
                'full_name': row[1],
                'email': row[2],
                'university': row[3],
                'major': row[4]
            }
        return None
    
    def update_student_profile(self, student_id, profile_data):
        """Update student profile"""
        query = '''
            UPDATE Students
            SET phone = ?, university = ?, major = ?, gpa = ?, skills = ?
            WHERE student_id = ?
        '''
        params = (
            profile_data.get('phone'),
            profile_data.get('university'),
            profile_data.get('major'),
            profile_data.get('gpa'),
            profile_data.get('skills'),
            student_id
        )
        self.execute_query(query, params)
    
    # Reference Operations
    def create_reference_request(self, reference_data):
        """Create a new reference request"""
        token = str(uuid.uuid4())
        expiry = datetime.now() + timedelta(days=30)
        
        query = '''
            INSERT INTO StudentReferences 
            (student_id, referee_name, referee_email, referee_phone, 
             relationship, company, token, expiry_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            reference_data['student_id'],
            reference_data['referee_name'],
            reference_data['referee_email'],
            reference_data.get('referee_phone'),
            reference_data.get('relationship'),
            reference_data.get('company'),
            token,
            expiry
        )
        cursor = self.execute_query(query, params)
        cursor.execute('SELECT @@IDENTITY')
        reference_id = int(cursor.fetchone()[0])
        return reference_id, token
    
    def get_student_references(self, student_id):
        """Get all references for a student"""
        query = '''
            SELECT reference_id, referee_name, referee_email, relationship, 
                   company, status, request_date, response_date, rating
            FROM StudentReferences
            WHERE student_id = ?
            ORDER BY request_date DESC
        '''
        results = self.execute_query(query, (student_id,), fetch=True)
        
        references = []
        for row in results:
            references.append({
                'reference_id': int(row[0]),
                'referee_name': row[1],
                'referee_email': row[2],
                'relationship': row[3],
                'company': row[4],
                'status': row[5],
                'request_date': str(row[6]) if row[6] else None,
                'response_date': str(row[7]) if row[7] else None,
                'rating': int(row[8]) if row[8] else None
            })
        return references
    
    def submit_reference_response(self, reference_id, reference_text, rating):
        """Submit a reference response"""
        query = '''
            UPDATE StudentReferences
            SET status = 'completed',
                response_date = GETDATE(),
                reference_text = ?,
                rating = ?
            WHERE reference_id = ?
        '''
        self.execute_query(query, (reference_text, rating, reference_id))
    
    def get_reference_stats(self, student_id):
        """Get reference statistics for a student"""
        query = '''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                AVG(CAST(rating AS FLOAT)) as avg_rating
            FROM StudentReferences
            WHERE student_id = ?
        '''
        results = self.execute_query(query, (student_id,), fetch=True)
        row = results[0]
        
        return {
            'total': int(row[0]) if row[0] else 0,
            'completed': int(row[1]) if row[1] else 0,
            'pending': int(row[2]) if row[2] else 0,
            'avg_rating': round(float(row[3]), 2) if row[3] else 0.0
        }
    
    # Notification Operations
    def create_notification(self, recipient_id, recipient_type, message, notification_type):
        """Create a new notification"""
        query = '''
            INSERT INTO Notifications (recipient_id, recipient_type, message, notification_type)
            VALUES (?, ?, ?, ?)
        '''
        self.execute_query(query, (recipient_id, recipient_type, message, notification_type))
    
    def get_user_notifications(self, user_id, user_type):
        """Get notifications for a user"""
        query = '''
            SELECT notification_id, message, notification_type, is_read, created_at
            FROM Notifications
            WHERE recipient_id = ? AND recipient_type = ?
            ORDER BY created_at DESC
        '''
        results = self.execute_query(query, (user_id, user_type), fetch=True)
        
        notifications = []
        for row in results:
            notifications.append({
                'notification_id': int(row[0]),
                'message': row[1],
                'type': row[2],
                'is_read': bool(row[3]),
                'created_at': str(row[4])
            })
        return notifications
    
    def mark_notification_read(self, notification_id):
        """Mark a notification as read"""
        query = 'UPDATE Notifications SET is_read = 1 WHERE notification_id = ?'
        self.execute_query(query, (notification_id,))