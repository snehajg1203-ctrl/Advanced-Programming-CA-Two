# client_candidate.py - CLI Client for StudentConnect (Student/Employer Interface)
"""
StudentConnect - Command Line Client
This allows students and employers to interact with the system via CLI
Requires app_backend.py to be running
"""

import requests
import json
from datetime import datetime

class StudentConnectClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
        self.current_user = None
    
    def _make_request(self, method, endpoint, data=None, params=None):
        """Make HTTP request to the API"""
        url = f"{self.base_url}{endpoint}"
        try:
            if method == 'GET':
                response = self.session.get(url, params=params)
            elif method == 'POST':
                response = self.session.post(url, json=data)
            elif method == 'DELETE':
                response = self.session.delete(url)
            else:
                return {'success': False, 'message': 'Invalid HTTP method'}
            
            if response.status_code >= 400:
                try:
                    return response.json()
                except:
                    return {'success': False, 'message': f'HTTP {response.status_code}'}
            
            return response.json()
        except requests.exceptions.ConnectionError:
            return {'success': False, 'message': 'Cannot connect to server. Is app_backend.py running?'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    # ==================== AUTHENTICATION ====================
    
    def register_student(self, name, email, password, **kwargs):
        """Register a new student"""
        data = {
            'name': name,
            'email': email,
            'password': password,
            'phone': kwargs.get('phone'),
            'university': kwargs.get('university'),
            'major': kwargs.get('major'),
            'year': kwargs.get('year')
        }
        return self._make_request('POST', '/api/auth/register/student', data)
    
    def register_employer(self, company, email, password, **kwargs):
        """Register a new employer"""
        data = {
            'company': company,
            'email': email,
            'password': password,
            'phone': kwargs.get('phone')
        }
        return self._make_request('POST', '/api/auth/register/employer', data)
    
    def login_student(self, email, password):
        """Login as student"""
        data = {'email': email, 'password': password}
        response = self._make_request('POST', '/api/auth/login/student', data)
        if response.get('success'):
            self.current_user = response.get('user')
        return response
    
    def login_employer(self, email, password):
        """Login as employer"""
        data = {'email': email, 'password': password}
        response = self._make_request('POST', '/api/auth/login/employer', data)
        if response.get('success'):
            self.current_user = response.get('user')
        return response
    
    # ==================== JOBS ====================
    
    def get_jobs(self):
        """Get all jobs"""
        return self._make_request('GET', '/api/jobs')
    
    def create_job(self, title, company, **kwargs):
        """Create a new job"""
        data = {
            'title': title,
            'company': company,
            'type': kwargs.get('type', 'part-time'),
            'location': kwargs.get('location'),
            'salary': kwargs.get('salary'),
            'hours': kwargs.get('hours'),
            'description': kwargs.get('description'),
            'skills': kwargs.get('skills', []),
            'employer_id': kwargs.get('employer_id') or (self.current_user['id'] if self.current_user else None)
        }
        return self._make_request('POST', '/api/jobs', data)
    
    # ==================== APPLICATIONS ====================
    
    def apply_for_job(self, job_id, job_title, company):
        """Apply for a job"""
        if not self.current_user:
            return {'success': False, 'message': 'Not logged in'}
        
        data = {
            'job_id': job_id,
            'student_id': self.current_user['id'],
            'job_title': job_title,
            'company': company
        }
        return self._make_request('POST', '/api/applications', data)
    
    def get_my_applications(self):
        """Get applications for current user"""
        if not self.current_user:
            return {'success': False, 'message': 'Not logged in'}
        return self._make_request('GET', f'/api/applications/student/{self.current_user["id"]}')
    
    # ==================== REFERENCES ====================
    
    def request_reference(self, referee_name, referee_email, **kwargs):
        """Request a reference"""
        if not self.current_user:
            return {'success': False, 'message': 'Not logged in'}
        
        data = {
            'student_id': self.current_user['id'],
            'referee_name': referee_name,
            'referee_email': referee_email,
            'referee_phone': kwargs.get('referee_phone'),
            'relationship': kwargs.get('relationship'),
            'company': kwargs.get('company'),
            'position': kwargs.get('position')
        }
        return self._make_request('POST', '/api/references', data)
    
    def get_my_references(self):
        """Get references for current user"""
        if not self.current_user:
            return {'success': False, 'message': 'Not logged in'}
        return self._make_request('GET', f'/api/references/student/{self.current_user["id"]}')
    
    # ==================== CLI INTERFACE ====================
    
    def run_cli(self):
        """Run command-line interface"""
        print("\n" + "="*70)
        print("STUDENTCONNECT - CLIENT INTERFACE")
        print("="*70)
        
        # Test connection first
        test = self._make_request('GET', '/api/jobs')
        if not test.get('success'):
            print("\n❌ Error: Cannot connect to backend server!")
            print("Please start the backend first: python app_backend.py")
            return
        
        print("✅ Connected to backend server")
        
        while True:
            print("\n" + "="*70)
            
            if not self.current_user:
                print("MAIN MENU")
                print("="*70)
                print("1. Register as Student")
                print("2. Register as Employer")
                print("3. Login as Student")
                print("4. Login as Employer")
                print("5. View All Jobs (Guest)")
                print("6. Exit")
                choice = input("\nSelect option: ")
                
                if choice == '1':
                    self._cli_register_student()
                elif choice == '2':
                    self._cli_register_employer()
                elif choice == '3':
                    self._cli_login_student()
                elif choice == '4':
                    self._cli_login_employer()
                elif choice == '5':
                    self._cli_view_jobs()
                elif choice == '6':
                    print("\nGoodbye!")
                    break
                else:
                    print("Invalid choice!")
            else:
                print(f"Logged in as: {self.current_user['name']} ({self.current_user['type']})")
                print("="*70)
                
                if self.current_user['type'] == 'student':
                    self._cli_student_menu()
                else:
                    self._cli_employer_menu()
            
            input("\nPress Enter to continue...")
    
    def _cli_register_student(self):
        """CLI: Register student"""
        print("\n=== STUDENT REGISTRATION ===")
        name = input("Full Name: ")
        email = input("Email: ")
        password = input("Password: ")
        phone = input("Phone (optional): ")
        university = input("University: ")
        major = input("Major: ")
        year = input("Year of Study (1-4): ")
        
        result = self.register_student(
            name=name,
            email=email,
            password=password,
            phone=phone or None,
            university=university,
            major=major,
            year=int(year) if year.isdigit() else None
        )
        
        if result.get('success'):
            print(f"\n✓ {result.get('message', 'Registration successful')}")
            print("You can now login with your credentials")
        else:
            print(f"\n✗ Error: {result.get('message', 'Registration failed')}")
    
    def _cli_register_employer(self):
        """CLI: Register employer"""
        print("\n=== EMPLOYER REGISTRATION ===")
        company = input("Company Name: ")
        email = input("Email: ")
        password = input("Password: ")
        phone = input("Phone (optional): ")
        
        result = self.register_employer(
            company=company,
            email=email,
            password=password,
            phone=phone or None
        )
        
        if result.get('success'):
            print(f"\n✓ {result.get('message', 'Registration successful')}")
            print("You can now login with your credentials")
        else:
            print(f"\n✗ Error: {result.get('message', 'Registration failed')}")
    
    def _cli_login_student(self):
        """CLI: Student login"""
        print("\n=== STUDENT LOGIN ===")
        email = input("Email: ")
        password = input("Password: ")
        
        result = self.login_student(email, password)
        
        if result.get('success'):
            print(f"\n✓ Welcome, {self.current_user['name']}!")
        else:
            print(f"\n✗ Error: {result.get('message', 'Invalid credentials')}")
    
    def _cli_login_employer(self):
        """CLI: Employer login"""
        print("\n=== EMPLOYER LOGIN ===")
        email = input("Email: ")
        password = input("Password: ")
        
        result = self.login_employer(email, password)
        
        if result.get('success'):
            print(f"\n✓ Welcome, {self.current_user['name']}!")
        else:
            print(f"\n✗ Error: {result.get('message', 'Invalid credentials')}")
    
    def _cli_view_jobs(self):
        """CLI: View all jobs"""
        result = self.get_jobs()
        
        if result.get('success'):
            jobs = result.get('jobs', [])
            if not jobs:
                print("\n📭 No jobs available")
                return
            
            print("\n=== AVAILABLE JOBS ===")
            print(f"\n{'ID':<5} {'Title':<30} {'Company':<25} {'Type':<15} {'Location':<20}")
            print("-" * 100)
            for job in jobs:
                print(f"{job['id']:<5} {job['title']:<30} {job['company']:<25} "
                      f"{job['type'] or 'N/A':<15} {job['location'] or 'N/A':<20}")
            print(f"\nTotal Jobs: {len(jobs)}")
        else:
            print(f"\n✗ Error: {result.get('message', 'Failed to load jobs')}")
    
    def _cli_student_menu(self):
        """CLI: Student menu"""
        print("\n1. View All Jobs")
        print("2. Apply to Job")
        print("3. View My Applications")
        print("4. Request Reference")
        print("5. View My References")
        print("6. Logout")
        
        choice = input("\nSelect option: ")
        
        if choice == '1':
            self._cli_view_jobs()
        elif choice == '2':
            self._cli_apply_job()
        elif choice == '3':
            self._cli_view_applications()
        elif choice == '4':
            self._cli_request_reference()
        elif choice == '5':
            self._cli_view_references()
        elif choice == '6':
            self.current_user = None
            print("\n✓ Logged out successfully")
        else:
            print("Invalid choice!")
    
    def _cli_employer_menu(self):
        """CLI: Employer menu"""
        print("\n1. View All Jobs")
        print("2. Post New Job")
        print("3. Logout")
        
        choice = input("\nSelect option: ")
        
        if choice == '1':
            self._cli_view_jobs()
        elif choice == '2':
            self._cli_post_job()
        elif choice == '3':
            self.current_user = None
            print("\n✓ Logged out successfully")
        else:
            print("Invalid choice!")
    
    def _cli_apply_job(self):
        """CLI: Apply for job"""
        job_id = input("\nEnter Job ID: ")
        
        if not job_id.isdigit():
            print("✗ Invalid Job ID")
            return
        
        jobs_result = self.get_jobs()
        if not jobs_result.get('success'):
            print(f"\n✗ Error: {jobs_result.get('message')}")
            return
        
        job = next((j for j in jobs_result.get('jobs', []) if j['id'] == int(job_id)), None)
        if not job:
            print("\n✗ Job not found")
            return
        
        print(f"\nApplying for: {job['title']} at {job['company']}")
        confirm = input("Confirm application? (yes/no): ")
        
        if confirm.lower() == 'yes':
            result = self.apply_for_job(job['id'], job['title'], job['company'])
            
            if result.get('success'):
                print(f"\n✓ {result.get('message')}")
            else:
                print(f"\n✗ Error: {result.get('message')}")
    
    def _cli_view_applications(self):
        """CLI: View applications"""
        result = self.get_my_applications()
        
        if result.get('success'):
            apps = result.get('applications', [])
            if not apps:
                print("\n📭 No applications yet")
                return
            
            print("\n=== MY APPLICATIONS ===")
            print(f"\n{'ID':<5} {'Job Title':<30} {'Company':<25} {'Status':<15} {'Date':<12}")
            print("-" * 90)
            for app in apps:
                date_str = app['applied_date'][:10] if app.get('applied_date') else 'N/A'
                print(f"{app['id']:<5} {app['job_title']:<30} {app['company']:<25} "
                      f"{app['status']:<15} {date_str:<12}")
            print(f"\nTotal Applications: {len(apps)}")
        else:
            print(f"\n✗ Error: {result.get('message')}")
    
    def _cli_request_reference(self):
        """CLI: Request reference"""
        print("\n=== REQUEST REFERENCE ===")
        name = input("Referee Name: ")
        email = input("Referee Email: ")
        phone = input("Phone (optional): ")
        relationship = input("Relationship (e.g., Professor, Manager): ")
        company = input("Company/Organization: ")
        position = input("Position/Title: ")
        
        result = self.request_reference(
            referee_name=name,
            referee_email=email,
            referee_phone=phone or None,
            relationship=relationship,
            company=company,
            position=position
        )
        
        if result.get('success'):
            print(f"\n✓ {result.get('message')}")
        else:
            print(f"\n✗ Error: {result.get('message')}")
    
    def _cli_view_references(self):
        """CLI: View references"""
        result = self.get_my_references()
        
        if result.get('success'):
            refs = result.get('references', [])
            if not refs:
                print("\n📭 No references yet")
                return
            
            print("\n=== MY REFERENCES ===")
            print(f"\n{'ID':<5} {'Referee':<25} {'Relationship':<20} {'Company':<25} {'Status':<12}")
            print("-" * 90)
            for ref in refs:
                print(f"{ref['id']:<5} {ref['referee_name']:<25} {ref['relationship'] or 'N/A':<20} "
                      f"{ref['company'] or 'N/A':<25} {ref['status']:<12}")
            print(f"\nTotal References: {len(refs)}")
        else:
            print(f"\n✗ Error: {result.get('message')}")
    
    def _cli_post_job(self):
        """CLI: Post job"""
        print("\n=== POST NEW JOB ===")
        title = input("Job Title: ")
        job_type = input("Type (part-time/internship/contract): ")
        location = input("Location: ")
        salary = input("Salary (e.g., €15-20/hr): ")
        hours = input("Hours per week: ")
        description = input("Description: ")
        skills = input("Required Skills (comma-separated): ")
        
        result = self.create_job(
            title=title,
            company=self.current_user['name'],
            type=job_type,
            location=location,
            salary=salary,
            hours=hours,
            description=description,
            skills=skills.split(',') if skills else []
        )
        
        if result.get('success'):
            print(f"\n✓ {result.get('message')}")
        else:
            print(f"\n✗ Error: {result.get('message')}")

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║        STUDENTCONNECT CLIENT (STUDENT/EMPLOYER)            ║
    ║         Part-Time Jobs & Reference Management              ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    client = StudentConnectClient()
    try:
        client.run_cli()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting... Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")