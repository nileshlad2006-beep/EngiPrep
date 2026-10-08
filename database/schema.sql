-- ============================================================
-- ENGIPREP – PLACEMENT PREPARATION PLATFORM
-- PostgreSQL Master Database Schema
-- ============================================================
-- Purpose:
-- This file contains the complete database structure required
-- by the EngiPrep Flask application.
--
-- IMPORTANT:
-- This is a master schema for creating a fresh database.
-- Do not run this file on the current working database unless
-- you intentionally want to rebuild the database from scratch.
-- ============================================================


-- ============================================================
-- REMOVE OLD TABLES
-- ============================================================
-- These commands are used only when creating a fresh database.
-- CASCADE automatically removes dependent foreign-key objects.

DROP TABLE IF EXISTS job_applications CASCADE;
DROP TABLE IF EXISTS companies CASCADE;
DROP TABLE IF EXISTS internships CASCADE;
DROP TABLE IF EXISTS certificates CASCADE;
DROP TABLE IF EXISTS projects CASCADE;

DROP TABLE IF EXISTS aptitude_attempts CASCADE;
DROP TABLE IF EXISTS aptitude_tests CASCADE;
DROP TABLE IF EXISTS aptitude_questions CASCADE;
DROP TABLE IF EXISTS aptitude_topics CASCADE;
DROP TABLE IF EXISTS aptitude_sections CASCADE;

DROP TABLE IF EXISTS academics CASCADE;
DROP TABLE IF EXISTS competitions CASCADE;

DROP TABLE IF EXISTS skill_gap_analysis CASCADE;
DROP TABLE IF EXISTS student_skills CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS student_profile CASCADE;
DROP TABLE IF EXISTS users CASCADE;


-- ============================================================
-- 1. USERS TABLE
-- ============================================================
-- Stores login, account and role information for students.

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 2. STUDENT PROFILE
-- ============================================================
-- Stores educational, personal and professional profile details.

CREATE TABLE student_profile (
    profile_id SERIAL PRIMARY KEY,

    user_id INTEGER UNIQUE
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    college_name VARCHAR(150),
    branch VARCHAR(80),

    semester INTEGER
        CHECK (semester BETWEEN 1 AND 8),

    cgpa NUMERIC(3,2)
        CHECK (cgpa BETWEEN 0 AND 10),

    phone VARCHAR(15),
    city VARCHAR(80),

    linkedin TEXT,
    github TEXT,
    resume_link TEXT,

    strengths TEXT,
    weaknesses TEXT,
    academic_achievements TEXT,

    graduation_year INTEGER,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 3. SKILLS MASTER TABLE
-- ============================================================
-- Stores the master list of skills available in the platform.

CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,

    skill_name VARCHAR(80) UNIQUE NOT NULL,

    category VARCHAR(50)
);


-- ============================================================
-- 4. STUDENT SKILLS
-- ============================================================
-- Connects students with their skills and skill levels.

CREATE TABLE student_skills (
    student_skill_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    skill_id INTEGER
        REFERENCES skills(skill_id)
        ON DELETE CASCADE,

    skill_level INTEGER
        CHECK (skill_level BETWEEN 1 AND 100),

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id, skill_id)
);


-- ============================================================
-- 5. SKILL GAP ANALYSIS
-- ============================================================
-- Stores missing skills and recommendations for a target role.

CREATE TABLE skill_gap_analysis (
    gap_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    target_role VARCHAR(80),

    missing_skill VARCHAR(80),

    required_level INTEGER
        CHECK (required_level BETWEEN 1 AND 100),

    current_level INTEGER
        CHECK (current_level BETWEEN 1 AND 100),

    gap_percentage INTEGER,

    recommendation TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 6. ACADEMICS
-- ============================================================
-- Stores semester, subject, marks, grades and academic performance.

CREATE TABLE academics (
    academic_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    semester INTEGER
        CHECK (semester BETWEEN 1 AND 8),

    subject_name VARCHAR(100),

    marks INTEGER
        CHECK (marks BETWEEN 0 AND 100),

    grade VARCHAR(5),

    sgpa NUMERIC(3,2),

    cgpa NUMERIC(3,2)
);


-- ============================================================
-- 7. APTITUDE SECTIONS
-- ============================================================
-- Stores the main aptitude preparation sections.

CREATE TABLE aptitude_sections (
    section_id SERIAL PRIMARY KEY,

    section_name VARCHAR(100) NOT NULL
);


-- ============================================================
-- 8. APTITUDE TOPICS
-- ============================================================
-- Stores topics belonging to each aptitude section.

CREATE TABLE aptitude_topics (
    topic_id SERIAL PRIMARY KEY,

    section_id INTEGER
        REFERENCES aptitude_sections(section_id)
        ON DELETE CASCADE,

    topic_name VARCHAR(100) NOT NULL
);


-- ============================================================
-- 9. APTITUDE QUESTIONS
-- ============================================================
-- Stores aptitude questions.
-- Questions can be automatically generated by Gemini
-- and saved here for future use.

CREATE TABLE aptitude_questions (
    question_id SERIAL PRIMARY KEY,

    topic_id INTEGER
        REFERENCES aptitude_topics(topic_id)
        ON DELETE CASCADE,

    question_text TEXT NOT NULL,

    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,

    correct_answer VARCHAR(20) NOT NULL,

    difficulty VARCHAR(30),

    explanation TEXT
);


-- ============================================================
-- 10. APTITUDE ATTEMPTS
-- ============================================================
-- Stores individual attempts made by students on aptitude topics.

CREATE TABLE aptitude_attempts (
    attempt_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    topic_id INTEGER
        REFERENCES aptitude_topics(topic_id)
        ON DELETE CASCADE,

    total_questions INTEGER,

    correct_answers INTEGER,

    score INTEGER,

    percentage NUMERIC(5,2),

    attempt_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 11. APTITUDE TESTS
-- ============================================================
-- Stores overall aptitude test results used by the dashboard.

CREATE TABLE aptitude_tests (
    test_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    test_name VARCHAR(100),

    category VARCHAR(50),

    total_questions INTEGER,

    score INTEGER,

    percentage NUMERIC(5,2),

    test_date DATE DEFAULT CURRENT_DATE
);


-- ============================================================
-- 12. PROJECTS
-- ============================================================
-- Stores student projects and their technologies.

CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    project_title VARCHAR(120),

    description TEXT,

    technologies TEXT,

    github_link TEXT,

    project_status VARCHAR(30),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- ============================================================
-- 13. CERTIFICATES
-- ============================================================
-- Stores certificates earned by students.

CREATE TABLE certificates (
    certificate_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    certificate_name VARCHAR(150),

    provider VARCHAR(120),

    issue_date DATE,

    certificate_link TEXT
);


-- ============================================================
-- 14. INTERNSHIPS
-- ============================================================
-- Stores internship information of students.

CREATE TABLE internships (
    internship_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    company_name VARCHAR(120),

    role VARCHAR(80),

    start_date DATE,

    end_date DATE,

    skills_used TEXT,

    certificate_link TEXT
);


-- ============================================================
-- 15. COMPANIES
-- ============================================================
-- Stores companies, job roles, packages and eligibility details.

CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,

    company_name VARCHAR(120) UNIQUE,

    role VARCHAR(80),

    package_lpa NUMERIC(4,2),

    location VARCHAR(100),

    eligibility_cgpa NUMERIC(3,2),

    skills_required TEXT,

    application_link TEXT
);


-- ============================================================
-- 16. JOB APPLICATIONS
-- ============================================================
-- Stores applications submitted by students to companies.

CREATE TABLE job_applications (
    application_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    company_id INTEGER
        REFERENCES companies(company_id)
        ON DELETE CASCADE,

    application_status VARCHAR(30),

    applied_on DATE DEFAULT CURRENT_DATE
);


-- ============================================================
-- 17. COMPETITIONS
-- ============================================================
-- Stores competitions and participation details of students.

CREATE TABLE competitions (
    competition_id SERIAL PRIMARY KEY,

    user_id INTEGER
        REFERENCES users(user_id)
        ON DELETE CASCADE,

    competition_name VARCHAR(150),

    description TEXT,

    participation_date DATE
);


-- ============================================================
-- END OF ENGIPREP DATABASE SCHEMA
-- ============================================================