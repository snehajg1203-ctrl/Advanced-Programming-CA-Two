USE StudentConnectDB;
GO

-- ============================================
-- CLEAN EXISTING SAMPLE DATA (IF ANY)
-- ============================================
PRINT 'Cleaning existing data...';
PRINT '';

-- Delete in correct order to respect foreign key constraints
DELETE FROM StudentReferences;
DELETE FROM Applications;
DELETE FROM Jobs;
DELETE FROM Employers;
DELETE FROM Students;

-- Reset identity seeds
DBCC CHECKIDENT ('Students', RESEED, 0);
DBCC CHECKIDENT ('Employers', RESEED, 0);
DBCC CHECKIDENT ('Jobs', RESEED, 0);
DBCC CHECKIDENT ('Applications', RESEED, 0);
DBCC CHECKIDENT ('StudentReferences', RESEED, 0);

PRINT '✓ Existing data cleaned';
PRINT '';

-- ============================================
-- SAMPLE DATA FOR STUDENTCONNECT DATABASE
-- ============================================

PRINT 'Inserting sample data...';
PRINT '';

-- ============================================
-- 1. STUDENTS TABLE
-- ============================================
PRINT 'Inserting Students...';

-- Password hash for 'password123' = ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
INSERT INTO Students (full_name, email, password_hash, phone, university, major, gpa, skills, created_at)
VALUES 
('John Smith', 'john.smith@student.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 87 123 4567', 'Trinity College Dublin', 'Computer Science', 3.5, 
 'Python,Java,React,SQL,Git', '2024-01-15'),

('Emma O''Brien', 'emma.obrien@student.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 86 234 5678', 'University College Dublin', 'Business Analytics', 3.7, 
 'Excel,PowerBI,SQL,Python,Tableau', '2024-02-20'),

('Michael Murphy', 'michael.murphy@student.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 85 345 6789', 'University College Cork', 'Mechanical Engineering', 3.8, 
 'CAD,MATLAB,SolidWorks,3D Printing,Arduino', '2024-01-10'),

('Sarah Kelly', 'sarah.kelly@student.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 89 456 7890', 'National University of Ireland Galway', 'Marketing', 3.4, 
 'Social Media,Content Creation,Adobe Creative Suite,SEO,Google Analytics', '2024-03-05'),

('David Walsh', 'david.walsh@student.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 87 567 8901', 'Dublin City University', 'Data Science', 3.9, 
 'R,Python,Machine Learning,Statistics,Data Visualization', '2024-02-12');

PRINT '✓ 5 Students inserted';

-- ============================================
-- 2. EMPLOYERS TABLE
-- ============================================
PRINT 'Inserting Employers...';

-- Password hash for 'password123' = ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f
INSERT INTO Employers (company_name, contact_person, email, password_hash, phone, industry, company_size, website, created_at)
VALUES 
('TechStart Ireland', 'Sarah Johnson', 'hr@techstart.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 1 234 5678', 'Technology', 'Small (10-50)', 'www.techstart.ie', '2024-01-05'),

('Dublin Retail Solutions', 'Michael Brown', 'jobs@dublinretail.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 1 345 6789', 'Retail', 'Medium (50-200)', 'www.dublinretail.ie', '2024-01-08'),

('Green Energy Co.', 'Patricia Green', 'careers@greenenergy.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 21 456 7890', 'Energy', 'Medium (50-200)', 'www.greenenergy.ie', '2024-02-01'),

('Creative Digital Agency', 'Tom Wilson', 'hello@creativedigital.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 1 567 8901', 'Marketing', 'Small (10-50)', 'www.creativedigital.ie', '2024-01-20'),

('DataViz Analytics', 'Lisa Murphy', 'recruit@dataviz.ie', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 
 '+353 1 678 9012', 'Technology', 'Small (10-50)', 'www.dataviz.ie', '2024-02-15');

PRINT '✓ 5 Employers inserted';

-- ============================================
-- 3. JOBS TABLE
-- ============================================
PRINT 'Inserting Jobs...';

-- employer_id values 1-5 correspond to the employers we just created in Employers table
INSERT INTO Jobs (title, company, job_type, location, salary, hours, description, required_skills, posted, employer_id, created_at)
VALUES 
('Junior Software Developer', 'TechStart Ireland', 'Part-time', 'Dublin 2', '€18-22/hr', '20 hours/week',
 'Join our dynamic startup as a junior developer. Work on exciting projects using modern technologies. Perfect for students looking to gain real-world experience in software development.',
 'Python,JavaScript,Git,Problem Solving', '2 days ago', 1, '2024-12-15'),

('Retail Sales Assistant', 'Dublin Retail Solutions', 'Part-time', 'Dublin City Centre', '€13-15/hr', '15-25 hours/week',
 'Customer-focused retail position in busy city centre location. Flexible hours to suit college schedule. Great opportunity to develop customer service and sales skills.',
 'Customer Service,Communication,Cash Handling,Teamwork', '5 days ago', 2, '2024-12-12'),

('Engineering Intern', 'Green Energy Co.', 'Internship', 'Cork', '€16-18/hr', '30 hours/week',
 'Summer internship opportunity in renewable energy sector. Work alongside experienced engineers on sustainable energy projects. Gain hands-on experience with cutting-edge technology.',
 'CAD,Technical Drawing,MATLAB,Analytical Skills', '1 week ago', 3, '2024-12-10'),

('Social Media Content Creator', 'Creative Digital Agency', 'Part-time', 'Remote/Hybrid Dublin', '€15-20/hr', '10-15 hours/week',
 'Creative role managing social media accounts for various clients. Create engaging content, schedule posts, and analyze performance. Perfect for marketing students with creative flair.',
 'Social Media,Content Creation,Adobe Photoshop,Copywriting', '3 days ago', 4, '2024-12-14'),

('Data Analysis Assistant', 'DataViz Analytics', 'Part-time', 'Dublin 4', '€17-21/hr', '20 hours/week',
 'Support our analytics team in processing and visualizing data. Work with real business data and modern analytics tools. Ideal for data science or business analytics students.',
 'Excel,Python,SQL,Data Visualization,PowerBI', '1 day ago', 5, '2024-12-16');

PRINT '✓ 5 Jobs inserted';

-- ============================================
-- 4. APPLICATIONS TABLE
-- ============================================
PRINT 'Inserting Applications...';

-- Student IDs are 1-5, Job IDs are 1-5
-- Status values must match CHECK constraint: 'Pending', 'Reviewed', 'Shortlisted', 'Accepted', 'Rejected'
INSERT INTO Applications (job_id, student_id, job_title, company, applied_date, status, cover_letter)
VALUES 
(1, 1, 'Junior Software Developer', 'TechStart Ireland', '2024-12-15 10:30:00', 'Pending',
 'I am excited to apply for the Junior Software Developer position. As a third-year Computer Science student with strong Python and JavaScript skills, I believe I would be a great fit for your team.'),

(5, 2, 'Data Analysis Assistant', 'DataViz Analytics', '2024-12-16 14:20:00', 'Reviewed',
 'My background in Business Analytics and proficiency in Excel, Python, and PowerBI make me an ideal candidate for this role. I am eager to apply my analytical skills in a real-world setting.'),

(3, 3, 'Engineering Intern', 'Green Energy Co.', '2024-12-11 09:15:00', 'Shortlisted',
 'As a final-year Mechanical Engineering student with experience in CAD and MATLAB, I am passionate about sustainable energy solutions and would love to contribute to your innovative projects.'),

(4, 4, 'Social Media Content Creator', 'Creative Digital Agency', '2024-12-14 16:45:00', 'Pending',
 'I have been managing social media accounts for student organizations and have strong skills in content creation and Adobe Creative Suite. I would bring creativity and enthusiasm to your team.'),

(2, 5, 'Retail Sales Assistant', 'Dublin Retail Solutions', '2024-12-13 11:30:00', 'Accepted',
 'I have previous retail experience and excellent customer service skills. My flexible schedule allows me to work evenings and weekends, making me available for your busiest periods.');

PRINT '✓ 5 Applications inserted';

-- ============================================
-- 5. STUDENTREFERENCES TABLE
-- ============================================
PRINT 'Inserting References...';

-- Student IDs are 1-5
INSERT INTO StudentReferences (student_id, referee_name, referee_email, referee_phone, relationship, company, position, 
                          request_date, status, response_date, reference_text, rating, token, expiry_date)
VALUES 
(1, 'Dr. Patricia Collins', 'p.collins@tcd.ie', '+353 1 896 1234', 'Lecturer', 
 'Trinity College Dublin', 'Senior Lecturer in Computer Science', 
 '2024-11-20 10:00:00', 'completed', '2024-11-22 15:30:00',
 'John has been an outstanding student in my advanced programming courses. He demonstrates excellent problem-solving abilities and works well in team projects. I highly recommend him for any technical role.',
 5, 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', '2025-01-20'),

(2, 'Mark O''Sullivan', 'mark.osullivan@analytics.ie', '+353 86 123 9876', 'Supervisor', 
 'Analytics Solutions Ltd', 'Data Analytics Manager', 
 '2024-12-01 09:30:00', 'completed', '2024-12-03 11:20:00',
 'Emma completed a summer placement with our team and impressed us with her analytical skills and attention to detail. She quickly mastered PowerBI and delivered excellent insights.',
 4, 'b2c3d4e5-f6a7-8901-bcde-f12345678901', '2025-02-01'),

(3, 'Prof. James McCarthy', 'j.mccarthy@ucc.ie', '+353 21 490 3000', 'Project Supervisor', 
 'University College Cork', 'Professor of Mechanical Engineering', 
 '2024-11-15 14:00:00', 'completed', '2024-11-18 16:45:00',
 'Michael has exceptional technical skills and shows great initiative in his project work. His proficiency with CAD software and practical engineering approach make him a valuable asset to any engineering team.',
 5, 'c3d4e5f6-a7b8-9012-cdef-123456789012', '2025-01-15'),

(4, 'Lisa Murphy', 'lisa.murphy@socialmedia.ie', '+353 87 234 5678', 'Marketing Manager', 
 'Social Buzz Marketing', 'Head of Digital Marketing', 
 '2024-12-05 10:15:00', 'pending', NULL, NULL, NULL,
 'd4e5f6a7-b8c9-0123-def1-234567890123', '2025-02-05'),

(5, 'Dr. Richard Burke', 'r.burke@dcu.ie', '+353 1 700 5000', 'Thesis Supervisor', 
 'Dublin City University', 'Assistant Professor in Data Science', 
 '2024-12-08 13:20:00', 'completed', '2024-12-10 09:30:00',
 'David is one of the top students in our Data Science program. His understanding of statistical methods and machine learning is impressive. He has contributed to research projects and would excel in any data-focused role.',
 5, 'e5f6a7b8-c9d0-1234-ef12-345678901234', '2025-02-08');

PRINT '✓ 5 References inserted';

-- ============================================
-- VERIFICATION
-- ============================================
PRINT '';
PRINT '============================================';
PRINT 'SAMPLE DATA INSERTED SUCCESSFULLY!';
PRINT '============================================';
PRINT '';

-- Display counts
DECLARE @StudentCount INT, @EmployerCount INT, @JobCount INT, @AppCount INT, @RefCount INT;

SELECT @StudentCount = COUNT(*) FROM Students;
SELECT @EmployerCount = COUNT(*) FROM Employers;
SELECT @JobCount = COUNT(*) FROM Jobs;
SELECT @AppCount = COUNT(*) FROM Applications;
SELECT @RefCount = COUNT(*) FROM StudentReferences;

PRINT 'Data Summary:';
PRINT '  ✓ Students:      ' + CAST(@StudentCount AS VARCHAR(10));
PRINT '  ✓ Employers:     ' + CAST(@EmployerCount AS VARCHAR(10));
PRINT '  ✓ Jobs:          ' + CAST(@JobCount AS VARCHAR(10));
PRINT '  ✓ Applications:  ' + CAST(@AppCount AS VARCHAR(10));
PRINT '  ✓ References:    ' + CAST(@RefCount AS VARCHAR(10));
PRINT '';
PRINT '============================================';
PRINT 'TEST CREDENTIALS:';
PRINT '============================================';
PRINT '';
PRINT 'Student Login:';
PRINT '  Email:    john.smith@student.ie';
PRINT '  Password: password123';
PRINT '';
PRINT 'Employer Login:';
PRINT '  Email:    hr@techstart.ie';
PRINT '  Password: password123';
PRINT '';
PRINT 'All user accounts use password: password123';
PRINT '============================================';
PRINT '';
PRINT 'Next Steps:';
PRINT '  1. Run test_connection.py to verify data';
PRINT '  2. Start backend: python app_backend.py';
PRINT '  3. Access student portal: http://localhost:5000/student';
PRINT '  4. Access admin portal: http://localhost:5000/admin';
PRINT '============================================';
GO