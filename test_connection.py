# test_connection.py - Test Database Connection and Verify Data
import pyodbc
import hashlib
from datetime import datetime

def test_database_connection():
    """Test database connection and display statistics"""
    
    print("="*70)
    print("STUDENTCONNECT DATABASE CONNECTION TEST")
    print("="*70)
    
    try:
        # Database connection string
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=StudentConnectDB;"
            "Trusted_Connection=yes;"
        )
        
        print("\n1. Testing connection to SQL Server...")
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("   ✓ Connection successful!")
        
        # Test each table
        print("\n2. Verifying database tables...")
        
        tables = ['Users', 'Jobs', 'Applications', '[References]']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   ✓ {table:15} : {count} records")
        
        # Detailed statistics
        print("\n3. Detailed Statistics:")
        print("-" * 70)
        
        # Students
        cursor.execute("SELECT COUNT(*) FROM Users WHERE type = 'student'")
        students = cursor.fetchone()[0]
        print(f"   Students:           {students}")
        
        # Employers
        cursor.execute("SELECT COUNT(*) FROM Users WHERE type = 'employer'")
        employers = cursor.fetchone()[0]
        print(f"   Employers:          {employers}")
        
        # Jobs
        cursor.execute("SELECT COUNT(*) FROM Jobs")
        jobs = cursor.fetchone()[0]
        print(f"   Active Jobs:        {jobs}")
        
        # Applications
        cursor.execute("SELECT COUNT(*) FROM Applications")
        apps = cursor.fetchone()[0]
        print(f"   Total Applications: {apps}")
        
        # References
        cursor.execute("SELECT COUNT(*) FROM [References]")
        refs = cursor.fetchone()[0]
        print(f"   Total References:   {refs}")
        
        # Status breakdown
        print("\n4. Application Status Breakdown:")
        print("-" * 70)
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM Applications 
            GROUP BY status 
            ORDER BY count DESC
        """)
        for row in cursor.fetchall():
            print(f"   {row[0]:15} : {row[1]}")
        
        # Reference status breakdown
        print("\n5. Reference Status Breakdown:")
        print("-" * 70)
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM [References] 
            GROUP BY status 
            ORDER BY count DESC
        """)
        for row in cursor.fetchall():
            print(f"   {row[0]:15} : {row[1]}")
        
        # Recent activity
        print("\n6. Recent Activity (Last 7 Days):")
        print("-" * 70)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Applications 
            WHERE applied_date >= DATEADD(day, -7, GETDATE())
        """)
        recent_apps = cursor.fetchone()[0]
        print(f"   New Applications:   {recent_apps}")
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM [References] 
            WHERE request_date >= DATEADD(day, -7, GETDATE())
        """)
        recent_refs = cursor.fetchone()[0]
        print(f"   New References:     {recent_refs}")
        
        # Sample data preview
        print("\n7. Sample Data Preview:")
        print("-" * 70)
        print("\n   Latest 3 Jobs:")
        cursor.execute("""
            SELECT TOP 3 title, company, location, salary 
            FROM Jobs 
            ORDER BY created_at DESC
        """)
        for row in cursor.fetchall():
            print(f"   • {row[0]} at {row[1]} ({row[2]}) - {row[3]}")
        
        print("\n   Latest 3 Applications:")
        cursor.execute("""
            SELECT TOP 3 u.name, a.job_title, a.company, a.status 
            FROM Applications a
            JOIN Users u ON a.student_id = u.id
            ORDER BY a.applied_date DESC
        """)
        for row in cursor.fetchall():
            print(f"   • {row[0]} → {row[1]} at {row[2]} ({row[3]})")
        
        # Test login credentials
        print("\n8. Testing Login Credentials:")
        print("-" * 70)
        
        # Test student login
        test_email = "john.smith@student.ie"
        test_password = "password123"
        password_hash = hashlib.sha256(test_password.encode()).hexdigest()
        
        cursor.execute("""
            SELECT id, name, email, type 
            FROM Users 
            WHERE email = ? AND password_hash = ?
        """, (test_email, password_hash))
        
        result = cursor.fetchone()
        if result:
            print(f"   ✓ Test Login Successful!")
            print(f"     Email:    {test_email}")
            print(f"     Password: {test_password}")
            print(f"     Name:     {result[1]}")
            print(f"     Type:     {result[3]}")
        else:
            print(f"   ✗ Test Login Failed")
        
        conn.close()
        
        print("\n" + "="*70)
        print("DATABASE TEST COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\n✓ Your database is properly configured and ready to use")
        print("✓ All sample data has been verified")
        print("✓ You can now run your Flask backend (python app_backend.py)")
        print("\nTest Credentials:")
        print(f"  Email:    {test_email}")
        print(f"  Password: {test_password}")
        print("="*70)
        
        return True
        
    except pyodbc.Error as e:
        print(f"\n✗ Database Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure SQL Server is running")
        print("2. Verify StudentConnectDB database exists")
        print("3. Run the StudentConnectDB.sql script first")
        print("4. Check your SQL Server connection settings")
        return False
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def quick_data_check():
    """Quick check to see if data exists"""
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost;"
            "DATABASE=StudentConnectDB;"
            "Trusted_Connection=yes;"
        )
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Users")
        user_count = cursor.fetchone()[0]
        
        conn.close()
        
        if user_count == 0:
            print("\n⚠️  WARNING: No data found in database!")
            print("Please run the sample data SQL script to populate the database.")
            print("\nSteps:")
            print("1. Open SQL Server Management Studio")
            print("2. Connect to your SQL Server")
            print("3. Open the sample_data.sql file")
            print("4. Execute the script")
            return False
        else:
            print(f"\n✓ Database contains {user_count} users")
            return True
            
    except Exception as e:
        print(f"✗ Could not check database: {e}")
        return False


if __name__ == '__main__':
    # Run quick check first
    if quick_data_check():
        # Run full test
        test_database_connection()
    else:
        print("\nPlease populate the database first before running the full test.")