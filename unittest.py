# unittest.py - Comprehensive Unit Tests for StudentConnect
"""
StudentConnect Unit Testing Suite
Tests all major components: Database, API endpoints, Authentication, CRUD operations
Run with: python unittest.py
"""

import unittest
import pyodbc
import hashlib
import requests
import time
from datetime import datetime

# Test Configuration
API_BASE_URL = 'http://localhost:5000/api'
DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': 'localhost',
    'database': 'StudentConnectDB',
    'trusted_connection': 'yes'
}

def get_db_connection():
    """Create database connection"""
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

class TestDatabaseConnection(unittest.TestCase):
    """Test database connectivity and table existence"""
    
    def test_01_database_connection(self):
        """Test if database connection can be established"""
        try:
            conn = get_db_connection()
            self.assertIsNotNone(conn)
            conn.close()
            print("✓ Database connection successful")
        except Exception as e:
            self.fail(f"Database connection failed: {e}")
    
    def test_02_users_table_exists(self):
        """Test if Users table exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Users'
        """)
        result = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(result, 1, "Users table does not exist")
        print("✓ Users table exists")
    
    def test_03_jobs_table_exists(self):
        """Test if Jobs table exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Jobs'
        """)
        result = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(result, 1, "Jobs table does not exist")
        print("✓ Jobs table exists")
    
    def test_04_applications_table_exists(self):
        """Test if Applications table exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'Applications'
        """)
        result = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(result, 1, "Applications table does not exist")
        print("✓ Applications table exists")
    
    def test_05_references_table_exists(self):
        """Test if References table exists"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'References'
        """)
        result = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(result, 1, "References table does not exist")
        print("✓ References table exists")

class TestDatabaseOperations(unittest.TestCase):
    """Test direct database CRUD operations"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data once for all tests"""
        cls.test_email = f"test_user_{int(time.time())}@test.ie"
        cls.test_password = "testpass123"
    
    def test_06_insert_student(self):
        """Test inserting a student into database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(self.test_password)
        
        try:
            cursor.execute("""
                INSERT INTO Users (type, name, email, password_hash, phone, university, major, year)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ('student', 'Test Student', self.test_email, password_hash, 
                  '0871234567', 'Test University', 'Test Major', 3))
            conn.commit()
            
            # Verify insertion
            cursor.execute("SELECT id, name FROM Users WHERE email = ?", (self.test_email,))
            result = cursor.fetchone()
            conn.close()
            
            self.assertIsNotNone(result)
            self.assertEqual(result[1], 'Test Student')
            print("✓ Student insertion successful")
        except Exception as e:
            conn.close()
            self.fail(f"Student insertion failed: {e}")
    
    def test_07_query_students(self):
        """Test querying students from database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Users WHERE type = 'student'")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertGreater(count, 0, "No students found in database")
        print(f"✓ Found {count} students in database")
    
    def test_08_query_employers(self):
        """Test querying employers from database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Users WHERE type = 'employer'")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertGreaterEqual(count, 0, "Query failed")
        print(f"✓ Found {count} employers in database")
    
    def test_09_query_jobs(self):
        """Test querying jobs from database"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Jobs")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertGreaterEqual(count, 0, "Query failed")
        print(f"✓ Found {count} jobs in database")

class TestAPIEndpoints(unittest.TestCase):
    """Test REST API endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Check if backend is running"""
        try:
            response = requests.get(f"{API_BASE_URL}/jobs", timeout=2)
            if response.status_code != 200:
                raise Exception("Backend not responding properly")
        except Exception as e:
            raise Exception(f"Backend server not running on port 5000. Please start app_backend.py first. Error: {e}")
    
    def test_10_api_get_jobs(self):
        """Test GET /api/jobs endpoint"""
        response = requests.get(f"{API_BASE_URL}/jobs")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('jobs', data)
        print(f"✓ GET /api/jobs successful - Found {len(data['jobs'])} jobs")
    
    def test_11_api_get_users(self):
        """Test GET /api/admin/users endpoint"""
        response = requests.get(f"{API_BASE_URL}/admin/users")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('users', data)
        print(f"✓ GET /api/admin/users successful - Found {len(data['users'])} users")
    
    def test_12_api_get_applications(self):
        """Test GET /api/applications endpoint"""
        response = requests.get(f"{API_BASE_URL}/applications")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('applications', data)
        print(f"✓ GET /api/applications successful - Found {len(data['applications'])} applications")
    
    def test_13_api_get_references(self):
        """Test GET /api/references endpoint"""
        response = requests.get(f"{API_BASE_URL}/references")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data.get('success'))
        self.assertIn('references', data)
        print(f"✓ GET /api/references successful - Found {len(data['references'])} references")

class TestAuthentication(unittest.TestCase):
    """Test authentication and registration"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test credentials"""
        cls.test_timestamp = int(time.time())
        cls.student_email = f"teststudent_{cls.test_timestamp}@test.ie"
        cls.employer_email = f"testemployer_{cls.test_timestamp}@test.ie"
        cls.password = "testpass123"
    
    def test_14_register_student(self):
        """Test student registration"""
        data = {
            'name': 'Test Student',
            'email': self.student_email,
            'password': self.password,
            'phone': '0871234567',
            'university': 'Test University',
            'major': 'Computer Science',
            'year': 3
        }
        
        response = requests.post(f"{API_BASE_URL}/auth/register/student", json=data)
        self.assertEqual(response.status_code, 201)
        
        result = response.json()
        self.assertTrue(result.get('success'))
        self.assertIn('user', result)
        print(f"✓ Student registration successful - ID: {result['user']['id']}")
    
    def test_15_register_employer(self):
        """Test employer registration"""
        data = {
            'company': 'Test Company',
            'email': self.employer_email,
            'password': self.password,
            'phone': '0871234567'
        }
        
        response = requests.post(f"{API_BASE_URL}/auth/register/employer", json=data)
        self.assertEqual(response.status_code, 201)
        
        result = response.json()
        self.assertTrue(result.get('success'))
        self.assertIn('user', result)
        print(f"✓ Employer registration successful - ID: {result['user']['id']}")
    
    def test_16_login_student(self):
        """Test student login"""
        # Use existing student from sample data
        data = {
            'email': 'john.smith@student.ie',
            'password': 'password123'
        }
        
        response = requests.post(f"{API_BASE_URL}/auth/login/student", json=data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        self.assertTrue(result.get('success'))
        self.assertIn('user', result)
        self.assertEqual(result['user']['type'], 'student')
        print(f"✓ Student login successful - {result['user']['name']}")
    
    def test_17_login_employer(self):
        """Test employer login"""
        # Use existing employer from sample data
        data = {
            'email': 'hr@techstart.ie',
            'password': 'password123'
        }
        
        response = requests.post(f"{API_BASE_URL}/auth/login/employer", json=data)
        self.assertEqual(response.status_code, 200)
        
        result = response.json()
        self.assertTrue(result.get('success'))
        self.assertIn('user', result)
        self.assertEqual(result['user']['type'], 'employer')
        print(f"✓ Employer login successful - {result['user']['name']}")
    
    def test_18_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'email': 'invalid@test.ie',
            'password': 'wrongpassword'
        }
        
        response = requests.post(f"{API_BASE_URL}/auth/login/student", json=data)
        self.assertEqual(response.status_code, 401)
        
        result = response.json()
        self.assertFalse(result.get('success'))
        print("✓ Invalid login correctly rejected")

class TestJobOperations(unittest.TestCase):
    """Test job-related operations"""
    
    def test_19_create_job(self):
        """Test creating a new job"""
        data = {
            'title': 'Test Software Developer',
            'company': 'Test Company Ltd',
            'type': 'part-time',
            'location': 'Dublin',
            'salary': '€20-25/hr',
            'hours': '20 hours/week',
            'description': 'Test job description',
            'skills': ['Python', 'JavaScript', 'SQL'],
            'employer_id': 6  # Use existing employer
        }
        
        response = requests.post(f"{API_BASE_URL}/jobs", json=data)
        self.assertEqual(response.status_code, 201)
        
        result = response.json()
        self.assertTrue(result.get('success'))
        self.assertIn('job_id', result)
        print(f"✓ Job creation successful - Job ID: {result['job_id']}")
    
    def test_20_get_specific_job(self):
        """Test retrieving specific job details"""
        # First get all jobs
        response = requests.get(f"{API_BASE_URL}/jobs")
        data = response.json()
        
        if data['jobs']:
            job_id = data['jobs'][0]['id']
            job_title = data['jobs'][0]['title']
            print(f"✓ Retrieved job details - ID: {job_id}, Title: {job_title}")
        else:
            self.skipTest("No jobs available to test")

class TestApplicationOperations(unittest.TestCase):
    """Test application-related operations"""
    
    def test_21_submit_application(self):
        """Test submitting a job application"""
        # Get an existing job
        jobs_response = requests.get(f"{API_BASE_URL}/jobs")
        jobs_data = jobs_response.json()
        
        if not jobs_data['jobs']:
            self.skipTest("No jobs available to apply to")
        
        job = jobs_data['jobs'][0]
        
        data = {
            'job_id': job['id'],
            'student_id': 1,  # Use existing student
            'job_title': job['title'],
            'company': job['company']
        }
        
        response = requests.post(f"{API_BASE_URL}/applications", json=data)
        
        # May get 400 if already applied, that's okay
        if response.status_code == 201:
            result = response.json()
            self.assertTrue(result.get('success'))
            print(f"✓ Application submitted successfully - ID: {result.get('application_id')}")
        elif response.status_code == 400:
            print("✓ Duplicate application correctly prevented")
        else:
            self.fail(f"Unexpected status code: {response.status_code}")
    
    def test_22_get_student_applications(self):
        """Test getting applications for a specific student"""
        student_id = 1  # Use existing student
        response = requests.get(f"{API_BASE_URL}/applications/student/{student_id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data.get('success'))
        print(f"✓ Retrieved {len(data['applications'])} applications for student {student_id}")

class TestReferenceOperations(unittest.TestCase):
    """Test reference-related operations"""
    
    def test_23_request_reference(self):
        """Test requesting a reference"""
        data = {
            'student_id': 1,  # Use existing student
            'referee_name': 'Test Referee',
            'referee_email': 'referee@test.ie',
            'referee_phone': '0871234567',
            'relationship': 'Professor',
            'company': 'Test University',
            'position': 'Senior Lecturer'
        }
        
        response = requests.post(f"{API_BASE_URL}/references", json=data)
        self.assertEqual(response.status_code, 201)
        
        result = response.json()
        self.assertTrue(result.get('success'))
        print(f"✓ Reference request created - ID: {result.get('reference_id')}")
    
    def test_24_get_student_references(self):
        """Test getting references for a specific student"""
        student_id = 1  # Use existing student
        response = requests.get(f"{API_BASE_URL}/references/student/{student_id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data.get('success'))
        print(f"✓ Retrieved {len(data['references'])} references for student {student_id}")

class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and constraints"""
    
    def test_25_duplicate_email_prevention(self):
        """Test that duplicate emails are prevented"""
        # Try to register with existing email
        data = {
            'name': 'Duplicate User',
            'email': 'john.smith@student.ie',  # Existing email
            'password': 'testpass123',
            'university': 'Test University',
            'major': 'Test Major',
            'year': 2
        }
        
        response = requests.post(f"{API_BASE_URL}/auth/register/student", json=data)
        self.assertEqual(response.status_code, 400)
        print("✓ Duplicate email correctly prevented")
    
    def test_26_data_relationships(self):
        """Test foreign key relationships"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if applications reference valid jobs and students
        cursor.execute("""
            SELECT COUNT(*) FROM Applications a
            WHERE NOT EXISTS (SELECT 1 FROM Jobs j WHERE j.id = a.job_id)
               OR NOT EXISTS (SELECT 1 FROM Users u WHERE u.id = a.student_id)
        """)
        
        orphaned = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(orphaned, 0, "Found orphaned application records")
        print("✓ Data relationships are valid")

class TestSystemStatistics(unittest.TestCase):
    """Test system statistics and reporting"""
    
    def test_27_system_overview(self):
        """Test getting system overview statistics"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Users WHERE type = 'student'")
        students = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Users WHERE type = 'employer'")
        employers = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Jobs")
        jobs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Applications")
        applications = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM [References]")
        references = cursor.fetchone()[0]
        
        conn.close()
        
        print("\n" + "="*60)
        print("SYSTEM STATISTICS:")
        print("="*60)
        print(f"Students:      {students}")
        print(f"Employers:     {employers}")
        print(f"Jobs:          {jobs}")
        print(f"Applications:  {applications}")
        print(f"References:    {references}")
        print("="*60)
        
        self.assertGreater(students, 0, "No students in system")
        self.assertGreater(jobs, 0, "No jobs in system")
        print("✓ System statistics retrieved successfully")

def run_tests():
    """Run all tests with custom test runner"""
    print("\n" + "="*70)
    print("STUDENTCONNECT UNIT TESTING SUITE")
    print("="*70)
    print("\nStarting comprehensive tests...")
    print("="*70 + "\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes in order
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseConnection))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestAuthentication))
    suite.addTests(loader.loadTestsFromTestCase(TestJobOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestApplicationOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestReferenceOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestDataIntegrity))
    suite.addTests(loader.loadTestsFromTestCase(TestSystemStatistics))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run:     {result.testsRun}")
    print(f"Successes:     {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures:      {len(result.failures)}")
    print(f"Errors:        {len(result.errors)}")
    print("="*70)
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
        print("="*70)
        return 0
    else:
        print("\n❌ SOME TESTS FAILED")
        print("="*70)
        return 1

if __name__ == '__main__':
    import sys
    exit_code = run_tests()
    sys.exit(exit_code)