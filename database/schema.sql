-- ============================================================
-- STUDENT PREPARATION PLATFORM
-- PostgreSQL Database Schema
-- Author: Vedant Magdum Mini Project
-- ============================================================

DROP TABLE IF EXISTS job_applications CASCADE;
DROP TABLE IF EXISTS companies CASCADE;
DROP TABLE IF EXISTS internships CASCADE;
DROP TABLE IF EXISTS certificates CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS aptitude_tests CASCADE;
DROP TABLE IF EXISTS academics CASCADE;
DROP TABLE IF EXISTS skill_gap_analysis CASCADE;
DROP TABLE IF EXISTS student_skills CASCADE;
DROP TABLE IF EXISTS skills CASCADE;
DROP TABLE IF EXISTS student_profile CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================================
-- USERS TABLE
-- ============================================================

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- STUDENT PROFILE
-- ============================================================

CREATE TABLE student_profile (
    profile_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(user_id) ON DELETE CASCADE,

    college_name VARCHAR(150),
    branch VARCHAR(80),
    semester INTEGER CHECK(semester BETWEEN 1 AND 8),

    cgpa NUMERIC(3,2) CHECK(cgpa BETWEEN 0 AND 10),

    phone VARCHAR(15),
    city VARCHAR(80),
    linkedin TEXT,
    github TEXT,

    resume_link TEXT,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SKILLS MASTER TABLE
-- ============================================================

CREATE TABLE skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name VARCHAR(80) UNIQUE NOT NULL,
    category VARCHAR(50)
);

-- ============================================================
-- STUDENT SKILLS
-- ============================================================

CREATE TABLE student_skills (
    student_skill_id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,

    skill_id INTEGER REFERENCES skills(skill_id) ON DELETE CASCADE,

    skill_level INTEGER CHECK(skill_level BETWEEN 1 AND 100),

    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(user_id, skill_id)
);

-- ============================================================
-- SKILL GAP ANALYZER
-- ============================================================

CREATE TABLE skill_gap_analysis (

    gap_id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,

    target_role VARCHAR(80),

    missing_skill VARCHAR(80),

    required_level INTEGER CHECK(required_level BETWEEN 1 AND 100),

    current_level INTEGER CHECK(current_level BETWEEN 1 AND 100),

    gap_percentage INTEGER,

    recommendation TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- ACADEMICS
-- ============================================================

CREATE TABLE academics (

    academic_id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,

    semester INTEGER CHECK(semester BETWEEN 1 AND 8),

    subject_name VARCHAR(100),

    marks INTEGER CHECK(marks BETWEEN 0 AND 100),

    grade VARCHAR(5),

    sgpa NUMERIC(3,2),

    cgpa NUMERIC(3,2)
);

-- ============================================================
-- APTITUDE TESTS
-- ============================================================

CREATE TABLE aptitude_tests (

    test_id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,

    test_name VARCHAR(100),

    category VARCHAR(50),

    total_questions INTEGER,

    score INTEGER,

    percentage NUMERIC(5,2),

    test_date DATE DEFAULT CURRENT_DATE
);

-- ============================================================
-- PROJECTS
-- ============================================================

CREATE TABLE projects (

    project_id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,

    project_title VARCHAR(120),

    description TEXT,

    technologies TEXT,

    github_link TEXT,

    project_status VARCHAR(30),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- CERTIFICATES
-- ============================================================

CREATE TABLE certificates (

    certificate_id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,

    certificate_name VARCHAR(150),

    provider VARCHAR(120),

    issue_date DATE,

    certificate_link TEXT
);

-- ============================================================
-- INTERNSHIPS
-- ============================================================

CREATE TABLE internships (

    internship_id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,

    company_name VARCHAR(120),

    role VARCHAR(80),

    start_date DATE,

    end_date DATE,

    skills_used TEXT,

    certificate_link TEXT
);

-- ============================================================
-- COMPANIES TABLE
-- ============================================================

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
-- JOB APPLICATIONS
-- ============================================================

CREATE TABLE job_applications (

    application_id SERIAL PRIMARY KEY,

    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,

    company_id INTEGER REFERENCES companies(company_id) ON DELETE CASCADE,

    application_status VARCHAR(30),

    applied_on DATE DEFAULT CURRENT_DATE
);