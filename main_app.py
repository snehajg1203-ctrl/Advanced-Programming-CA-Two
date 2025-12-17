# main_app.py - StudentConnect Management System - CLI VERSION
"""
StudentConnect - Part-Time Job & Reference Management System
Command Line Interface for Admin Operations
"""

import sys
import os
import pyodbc
from datetime import datetime

class StudentConnectApp:
    """Main application class for CLI interface"""
    
    def __init__(self):
        """Initialize the application with database connection"""
        self.db_config = {
            'driver': '{ODBC Driver 17 for SQL Server}',
            'server': 'localhost',
            'database': 'StudentConnectDB',
            'trusted_connection': 'yes'
        }
        self.conn = None
        self.initialize_database()
    
    def get_connection(self):
        """Get database connection"""
        if not self.conn:
            conn_str = (
                f"DRIVER={self.db_config['driver']};"
                f"SERVER={self.db_config['server']};"
                f"DATABASE={self.db_config['database']};"
                f"Trusted_Connection={self.db_config['trusted_connection']};"
            )
            self.conn = pyodbc.connect(conn_str)
        return self.conn
    
    def initialize_database(self):
        """Check database connection"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Users")
            print("✓ Database connected successfully!")
        except Exception as e:
            print(f"✗ Database connection error: {e}")
            print("\nPlease ensure:")
            print("  1. SQL Server is running")
            print("  2. StudentConnectDB database exists")
            print("  3. Tables are created (run StudentConnectDB.sql)")
            sys.exit(1)
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_menu(self):
        """Display main menu options"""
        print("\n" + "="*60)
        print("       STUDENTCONNECT MANAGEMENT SYSTEM")
        print("    Part-Time Jobs & Reference Management")
        print("="*60)
        print("\n1. Student Management")
        print("2. Employer Management")
        print("3. Job Management")
        print("4. Application Management")
        print("5. Reference Management")
        print("6. Reports & Statistics")
        print("7. Exit")
        print("-"*60)
    
    # ==================== STUDENT MANAGEMENT ====================
    
    def student_management_menu(self):
        """Handle student-related operations"""
        while True:
            print("\n--- STUDENT MANAGEMENT ---")
            print("1. View All Students")
            print("2. View Student Details")
            print("3. Search Students by University")
            print("4. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.view_all_students()
            elif choice == '2':
                self.view_student_details()
            elif choice == '3':
                self.search_students_by_university()
            elif choice == '4':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def view_all_students(self):
        """Display all registered students"""
        print("\n--- ALL STUDENTS ---")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, email, university, major, year, created_at
            FROM Users WHERE type = 'student'
            ORDER BY created_at DESC
        """)
        
        students = cursor.fetchall()
        
        if not students:
            print("No students registered yet.")
            return
        
        print(f"\n{'ID':<5} {'Name':<20} {'Email':<25} {'University':<25} {'Major':<20} {'Year':<5}")
        print("-"*105)
        for s in students:
            print(f"{s[0]:<5} {s[1]:<20} {s[2]:<25} {s[3] or 'N/A':<25} {s[4] or 'N/A':<20} {s[5] or 'N/A':<5}")
        
        print(f"\nTotal Students: {len(students)}")
    
    def view_student_details(self):
        """View detailed information about a specific student"""
        student_id = input("\nEnter Student ID: ")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, email, phone, university, major, year, skills, created_at
            FROM Users WHERE id = ? AND type = 'student'
        """, (student_id,))
        
        student = cursor.fetchone()
        
        if student:
            print("\n--- STUDENT DETAILS ---")
            print(f"ID: {student[0]}")
            print(f"Name: {student[1]}")
            print(f"Email: {student[2]}")
            print(f"Phone: {student[3] or 'N/A'}")
            print(f"University: {student[4] or 'N/A'}")
            print(f"Major: {student[5] or 'N/A'}")
            print(f"Year: {student[6] or 'N/A'}")
            print(f"Skills: {student[7] or 'N/A'}")
            print(f"Registered: {student[8]}")
            
            # Get student's applications
            cursor.execute("SELECT COUNT(*) FROM Applications WHERE student_id = ?", (student_id,))
            app_count = cursor.fetchone()[0]
            print(f"Total Applications: {app_count}")
            
            # Get student's references
            cursor.execute("SELECT COUNT(*) FROM [References] WHERE student_id = ?", (student_id,))
            ref_count = cursor.fetchone()[0]
            print(f"Total References: {ref_count}")
        else:
            print(f"✗ Student with ID {student_id} not found!")
    
    def search_students_by_university(self):
        """Search students by university"""
        university = input("\nEnter University name: ")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, email, major, year
            FROM Users WHERE type = 'student' AND university LIKE ?
        """, (f'%{university}%',))
        
        students = cursor.fetchall()
        
        if students:
            print(f"\n--- STUDENTS FROM {university.upper()} ---")
            print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Major':<20} {'Year':<5}")
            print("-"*90)
            for s in students:
                print(f"{s[0]:<5} {s[1]:<25} {s[2]:<30} {s[3] or 'N/A':<20} {s[4] or 'N/A':<5}")
            print(f"\nFound {len(students)} students")
        else:
            print("No students found from that university.")
    
    # ==================== EMPLOYER MANAGEMENT ====================
    
    def employer_management_menu(self):
        """Handle employer-related operations"""
        while True:
            print("\n--- EMPLOYER MANAGEMENT ---")
            print("1. View All Employers")
            print("2. View Employer Details")
            print("3. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.view_all_employers()
            elif choice == '2':
                self.view_employer_details()
            elif choice == '3':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def view_all_employers(self):
        """Display all registered employers"""
        print("\n--- ALL EMPLOYERS ---")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, email, phone, created_at
            FROM Users WHERE type = 'employer'
            ORDER BY created_at DESC
        """)
        
        employers = cursor.fetchall()
        
        if not employers:
            print("No employers registered yet.")
            return
        
        print(f"\n{'ID':<5} {'Company':<30} {'Email':<30} {'Phone':<15}")
        print("-"*85)
        for e in employers:
            print(f"{e[0]:<5} {e[1]:<30} {e[2]:<30} {e[3] or 'N/A':<15}")
        
        print(f"\nTotal Employers: {len(employers)}")
    
    def view_employer_details(self):
        """View detailed information about a specific employer"""
        employer_id = input("\nEnter Employer ID: ")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, email, phone, created_at
            FROM Users WHERE id = ? AND type = 'employer'
        """, (employer_id,))
        
        employer = cursor.fetchone()
        
        if employer:
            print("\n--- EMPLOYER DETAILS ---")
            print(f"ID: {employer[0]}")
            print(f"Company: {employer[1]}")
            print(f"Email: {employer[2]}")
            print(f"Phone: {employer[3] or 'N/A'}")
            print(f"Registered: {employer[4]}")
            
            # Get employer's jobs
            cursor.execute("SELECT COUNT(*) FROM Jobs WHERE employer_id = ?", (employer_id,))
            job_count = cursor.fetchone()[0]
            print(f"Total Jobs Posted: {job_count}")
        else:
            print(f"✗ Employer with ID {employer_id} not found!")
    
    # ==================== JOB MANAGEMENT ====================
    
    def job_management_menu(self):
        """Handle job-related operations"""
        while True:
            print("\n--- JOB MANAGEMENT ---")
            print("1. View All Jobs")
            print("2. View Job Details")
            print("3. View Jobs by Company")
            print("4. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.view_all_jobs()
            elif choice == '2':
                self.view_job_details()
            elif choice == '3':
                self.view_jobs_by_company()
            elif choice == '4':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def view_all_jobs(self):
        """Display all jobs"""
        print("\n--- ALL JOBS ---")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, company, type, location, salary, created_at
            FROM Jobs ORDER BY created_at DESC
        """)
        
        jobs = cursor.fetchall()
        
        if not jobs:
            print("No jobs posted yet.")
            return
        
        print(f"\n{'ID':<5} {'Title':<30} {'Company':<25} {'Type':<15} {'Location':<20}")
        print("-"*100)
        for j in jobs:
            print(f"{j[0]:<5} {j[1]:<30} {j[2]:<25} {j[3] or 'N/A':<15} {j[4] or 'N/A':<20}")
        
        print(f"\nTotal Jobs: {len(jobs)}")
    
    def view_job_details(self):
        """View detailed information about a specific job"""
        job_id = input("\nEnter Job ID: ")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, company, type, location, salary, hours, description, required_skills, created_at
            FROM Jobs WHERE id = ?
        """, (job_id,))
        
        job = cursor.fetchone()
        
        if job:
            print("\n--- JOB DETAILS ---")
            print(f"ID: {job[0]}")
            print(f"Title: {job[1]}")
            print(f"Company: {job[2]}")
            print(f"Type: {job[3] or 'N/A'}")
            print(f"Location: {job[4] or 'N/A'}")
            print(f"Salary: {job[5] or 'N/A'}")
            print(f"Hours: {job[6] or 'N/A'}")
            print(f"Description: {job[7] or 'N/A'}")
            print(f"Required Skills: {job[8] or 'N/A'}")
            print(f"Posted: {job[9]}")
            
            # Get application count
            cursor.execute("SELECT COUNT(*) FROM Applications WHERE job_id = ?", (job_id,))
            app_count = cursor.fetchone()[0]
            print(f"Total Applications: {app_count}")
        else:
            print(f"✗ Job with ID {job_id} not found!")
    
    def view_jobs_by_company(self):
        """View all jobs from a specific company"""
        company = input("\nEnter Company name: ")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, type, location, salary
            FROM Jobs WHERE company LIKE ?
        """, (f'%{company}%',))
        
        jobs = cursor.fetchall()
        
        if jobs:
            print(f"\n--- JOBS FROM {company.upper()} ---")
            print(f"{'ID':<5} {'Title':<35} {'Type':<15} {'Location':<20} {'Salary':<15}")
            print("-"*95)
            for j in jobs:
                print(f"{j[0]:<5} {j[1]:<35} {j[2] or 'N/A':<15} {j[3] or 'N/A':<20} {j[4] or 'N/A':<15}")
            print(f"\nFound {len(jobs)} jobs")
        else:
            print("No jobs found from that company.")
    
    # ==================== APPLICATION MANAGEMENT ====================
    
    def application_management_menu(self):
        """Handle application-related operations"""
        while True:
            print("\n--- APPLICATION MANAGEMENT ---")
            print("1. View All Applications")
            print("2. View Applications by Status")
            print("3. View Student's Applications")
            print("4. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.view_all_applications()
            elif choice == '2':
                self.view_applications_by_status()
            elif choice == '3':
                self.view_student_applications()
            elif choice == '4':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def view_all_applications(self):
        """Display all applications"""
        print("\n--- ALL APPLICATIONS ---")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT a.id, u.name, a.job_title, a.company, a.status, a.applied_date
            FROM Applications a
            JOIN Users u ON a.student_id = u.id
            ORDER BY a.applied_date DESC
        """)
        
        apps = cursor.fetchall()
        
        if not apps:
            print("No applications yet.")
            return
        
        print(f"\n{'ID':<5} {'Student':<25} {'Job Title':<30} {'Company':<20} {'Status':<15} {'Date':<12}")
        print("-"*115)
        for a in apps:
            date_str = a[5].strftime('%Y-%m-%d') if a[5] else 'N/A'
            print(f"{a[0]:<5} {a[1]:<25} {a[2]:<30} {a[3]:<20} {a[4]:<15} {date_str:<12}")
        
        print(f"\nTotal Applications: {len(apps)}")
    
    def view_applications_by_status(self):
        """View applications filtered by status"""
        print("\nSelect Status:")
        print("1. Pending")
        print("2. Under Review")
        print("3. Shortlisted")
        print("4. Rejected")
        print("5. Accepted")
        
        choice = input("\nEnter choice: ")
        status_map = {
            '1': 'pending',
            '2': 'under review',
            '3': 'shortlisted',
            '4': 'rejected',
            '5': 'accepted'
        }
        
        if choice not in status_map:
            print("Invalid choice!")
            return
        
        status = status_map[choice]
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT a.id, u.name, a.job_title, a.company, a.applied_date
            FROM Applications a
            JOIN Users u ON a.student_id = u.id
            WHERE a.status = ?
            ORDER BY a.applied_date DESC
        """, (status,))
        
        apps = cursor.fetchall()
        
        if apps:
            print(f"\n--- {status.upper()} APPLICATIONS ---")
            print(f"{'ID':<5} {'Student':<25} {'Job Title':<30} {'Company':<20} {'Date':<12}")
            print("-"*95)
            for a in apps:
                date_str = a[4].strftime('%Y-%m-%d') if a[4] else 'N/A'
                print(f"{a[0]:<5} {a[1]:<25} {a[2]:<30} {a[3]:<20} {date_str:<12}")
            print(f"\nFound {len(apps)} applications")
        else:
            print(f"No {status} applications found.")
    
    def view_student_applications(self):
        """View all applications from a specific student"""
        student_id = input("\nEnter Student ID: ")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT a.id, a.job_title, a.company, a.status, a.applied_date
            FROM Applications a
            WHERE a.student_id = ?
            ORDER BY a.applied_date DESC
        """, (student_id,))
        
        apps = cursor.fetchall()
        
        if apps:
            print(f"\n--- APPLICATIONS FOR STUDENT {student_id} ---")
            print(f"{'ID':<5} {'Job Title':<35} {'Company':<25} {'Status':<15} {'Date':<12}")
            print("-"*95)
            for a in apps:
                date_str = a[4].strftime('%Y-%m-%d') if a[4] else 'N/A'
                print(f"{a[0]:<5} {a[1]:<35} {a[2]:<25} {a[3]:<15} {date_str:<12}")
            print(f"\nTotal: {len(apps)} applications")
        else:
            print("No applications found for this student.")
    
    # ==================== REFERENCE MANAGEMENT ====================
    
    def reference_management_menu(self):
        """Handle reference-related operations"""
        while True:
            print("\n--- REFERENCE MANAGEMENT ---")
            print("1. View All References")
            print("2. View References by Status")
            print("3. View Student's References")
            print("4. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.view_all_references()
            elif choice == '2':
                self.view_references_by_status()
            elif choice == '3':
                self.view_student_references()
            elif choice == '4':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def view_all_references(self):
        """Display all references"""
        print("\n--- ALL REFERENCES ---")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.id, u.name, r.referee_name, r.company, r.status, r.request_date
            FROM [References] r
            JOIN Users u ON r.student_id = u.id
            ORDER BY r.request_date DESC
        """)
        
        refs = cursor.fetchall()
        
        if not refs:
            print("No references yet.")
            return
        
        print(f"\n{'ID':<5} {'Student':<25} {'Referee':<25} {'Company':<25} {'Status':<12} {'Date':<12}")
        print("-"*110)
        for r in refs:
            date_str = r[5].strftime('%Y-%m-%d') if r[5] else 'N/A'
            print(f"{r[0]:<5} {r[1]:<25} {r[2]:<25} {r[3] or 'N/A':<25} {r[4]:<12} {date_str:<12}")
        
        print(f"\nTotal References: {len(refs)}")
    
    def view_references_by_status(self):
        """View references filtered by status"""
        print("\nSelect Status:")
        print("1. Pending")
        print("2. Completed")
        print("3. Declined")
        
        choice = input("\nEnter choice: ")
        status_map = {'1': 'pending', '2': 'completed', '3': 'declined'}
        
        if choice not in status_map:
            print("Invalid choice!")
            return
        
        status = status_map[choice]
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.id, u.name, r.referee_name, r.company, r.request_date, r.rating
            FROM [References] r
            JOIN Users u ON r.student_id = u.id
            WHERE r.status = ?
            ORDER BY r.request_date DESC
        """, (status,))
        
        refs = cursor.fetchall()
        
        if refs:
            print(f"\n--- {status.upper()} REFERENCES ---")
            print(f"{'ID':<5} {'Student':<25} {'Referee':<25} {'Company':<25} {'Date':<12} {'Rating':<8}")
            print("-"*105)
            for r in refs:
                date_str = r[4].strftime('%Y-%m-%d') if r[4] else 'N/A'
                rating = r[5] if r[5] else 'N/A'
                print(f"{r[0]:<5} {r[1]:<25} {r[2]:<25} {r[3] or 'N/A':<25} {date_str:<12} {rating:<8}")
            print(f"\nFound {len(refs)} references")
        else:
            print(f"No {status} references found.")
    
    def view_student_references(self):
        """View all references for a specific student"""
        student_id = input("\nEnter Student ID: ")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, referee_name, company, relationship, status, rating, request_date
            FROM [References]
            WHERE student_id = ?
            ORDER BY request_date DESC
        """, (student_id,))
        
        refs = cursor.fetchall()
        
        if refs:
            print(f"\n--- REFERENCES FOR STUDENT {student_id} ---")
            print(f"{'ID':<5} {'Referee':<25} {'Company':<25} {'Relationship':<15} {'Status':<12} {'Rating':<8}")
            print("-"*95)
            for r in refs:
                rating = r[5] if r[5] else 'N/A'
                print(f"{r[0]:<5} {r[1]:<25} {r[2] or 'N/A':<25} {r[3] or 'N/A':<15} {r[4]:<12} {rating:<8}")
            print(f"\nTotal: {len(refs)} references")
        else:
            print("No references found for this student.")
    
    # ==================== REPORTS ====================
    
    def reports_menu(self):
        """Generate reports and statistics"""
        while True:
            print("\n--- REPORTS & STATISTICS ---")
            print("1. System Overview")
            print("2. Application Statistics")
            print("3. Reference Statistics")
            print("4. Back to Main Menu")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.system_overview()
            elif choice == '2':
                self.application_statistics()
            elif choice == '3':
                self.reference_statistics()
            elif choice == '4':
                break
            else:
                print("Invalid choice! Please try again.")
    
    def system_overview(self):
        """Display system overview statistics"""
        print("\n--- SYSTEM OVERVIEW ---")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Students count
        cursor.execute("SELECT COUNT(*) FROM Users WHERE type = 'student'")
        students = cursor.fetchone()[0]
        
        # Employers count
        cursor.execute("SELECT COUNT(*) FROM Users WHERE type = 'employer'")
        employers = cursor.fetchone()[0]
        
        # Jobs count
        cursor.execute("SELECT COUNT(*) FROM Jobs")
        jobs = cursor.fetchone()[0]
        
        # Applications count
        cursor.execute("SELECT COUNT(*) FROM Applications")
        apps = cursor.fetchone()[0]
        
        # References count
        cursor.execute("SELECT COUNT(*) FROM [References]")
        refs = cursor.fetchone()[0]
        
        print(f"\nTotal Students:      {students}")
        print(f"Total Employers:     {employers}")
        print(f"Total Jobs:          {jobs}")
        print(f"Total Applications:  {apps}")
        print(f"Total References:    {refs}")
    
    def application_statistics(self):
        """Display application statistics"""
        print("\n--- APPLICATION STATISTICS ---")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM Applications
            GROUP BY status
            ORDER BY count DESC
        """)
        
        stats = cursor.fetchall()
        
        if stats:
            print(f"\n{'Status':<20} {'Count':<10}")
            print("-"*30)
            for stat in stats:
                print(f"{stat[0]:<20} {stat[1]:<10}")
        else:
            print("No application data available.")
    
    def reference_statistics(self):
        """Display reference statistics"""
        print("\n--- REFERENCE STATISTICS ---")
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM [References]
            GROUP BY status
            ORDER BY count DESC
        """)
        
        stats = cursor.fetchall()
        
        if stats:
            print(f"\n{'Status':<20} {'Count':<10}")
            print("-"*30)
            for stat in stats:
                print(f"{stat[0]:<20} {stat[1]:<10}")
            
            # Average rating
            cursor.execute("SELECT AVG(CAST(rating AS FLOAT)) FROM [References] WHERE rating IS NOT NULL")
            avg_rating = cursor.fetchone()[0]
            if avg_rating:
                print(f"\nAverage Rating: {avg_rating:.2f}/5")
        else:
            print("No reference data available.")
    
    # ==================== MAIN LOOP ====================
    
    def run(self):
        """Main application loop"""
        print("""
    ╔════════════════════════════════════════════════════════════╗
    ║         STUDENTCONNECT MANAGEMENT SYSTEM (CLI)             ║
    ║      Part-Time Jobs & Reference Management System          ║
    ╚════════════════════════════════════════════════════════════╝
        """)
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.student_management_menu()
            elif choice == '2':
                self.employer_management_menu()
            elif choice == '3':
                self.job_management_menu()
            elif choice == '4':
                self.application_management_menu()
            elif choice == '5':
                self.reference_management_menu()
            elif choice == '6':
                self.reports_menu()
            elif choice == '7':
                if self.conn:
                    self.conn.close()
                print("\nThank you for using StudentConnect Management System!")
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")
            
            input("\nPress Enter to continue...")

# Run the application
if __name__ == "__main__":
    try:
        app = StudentConnectApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)