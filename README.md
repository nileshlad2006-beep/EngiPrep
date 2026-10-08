# EngiPrep – Placement Preparation Platform

EngiPrep is a web-based placement preparation platform developed using Flask, PostgreSQL, HTML, CSS, JavaScript, and Google Gemini AI.

The platform helps students manage their placement preparation, practice aptitude questions, maintain their student profile, track test performance, and interact with an AI-powered preparation assistant.

## Features

### Student Authentication
- Student signup
- Student login
- Password hashing
- Session-based authentication
- Logout functionality

### Student Profile
Students can maintain their:
- Personal information
- College information
- Branch
- Semester
- CGPA
- Graduation year
- City
- Phone number
- LinkedIn profile
- GitHub profile
- Resume link
- Strengths
- Weaknesses
- Academic achievements

### Aptitude Preparation
The aptitude module provides:
- Multiple aptitude sections
- Multiple topics
- Automatically generated questions
- Multiple-choice questions
- Question explanations
- Automatic score calculation
- Percentage calculation
- Attempt history

### AI Question Generation
Google Gemini AI is used to generate aptitude questions dynamically.

Generated questions are stored in PostgreSQL so that they can be reused instead of generating the same questions repeatedly.

### AI Chatbot
EngiPrep includes an AI-powered chatbot that:
- Answers placement preparation questions
- Uses the student's profile information
- Uses previous aptitude performance
- Provides personalized preparation guidance
- Maintains recent conversation context

### Dashboard
The dashboard provides an overview of the student's preparation activity, including aptitude performance and student information.

## Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Poppins Font

### Backend
- Python
- Flask

### Database
- PostgreSQL
- psycopg2

### AI
- Google Gemini API

### Deployment
- Render

## Project Structure

```text
EngiPrep/
│
├── app.py
├── config.py
├── db.py
├── api_service.py
├── requirements.txt
├── render.yaml
├── .env
├── .gitignore
├── README.md
│
├── database/
│   └── schema.sql
│
├── routes/
│   ├── auth.py
│   ├── profile.py
│   ├── dashboard.py
│   ├── aptitude.py
│   └── chatbot.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   ├── Dashboard.html
│   └── Preparation.html
│
└── static/
    ├── css/
    ├── js/
    └── images/
```

## Database

EngiPrep uses PostgreSQL to store student and preparation data.

Important database tables include:

- `users`
- `student_profile`
- `skills`
- `student_skills`
- `skill_gap_analysis`
- `academics`
- `aptitude_sections`
- `aptitude_topics`
- `aptitude_questions`
- `aptitude_attempts`
- `aptitude_tests`
- `projects`
- `certificates`
- `internships`
- `companies`
- `job_applications`
- `competitions`

The master database structure is available in:

```text
database/schema.sql
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your_secret_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=project_database
DB_USER=postgres
DB_PASSWORD=your_postgresql_password

GEMINI_API_KEY=your_gemini_api_key
```

Do not upload the `.env` file to GitHub.

## Installation

Clone the project and open the project directory:

```bash
cd EngiPrep
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Configure the `.env` file with the PostgreSQL and Gemini API credentials.

Create the required PostgreSQL database:

```text
project_database
```

Run the Flask application:

```bash
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

## Application Flow

```text
Home
  ↓
Signup / Login
  ↓
Student Profile
  ↓
Dashboard
  ↓
Preparation
  ↓
Aptitude Test
  ↓
AI Generated Questions
  ↓
Score & Results
  ↓
Dashboard
  ↓
Personalized AI Chatbot
```

## Security

The application uses:
- Password hashing
- Flask sessions
- Environment variables for sensitive configuration
- Parameterized PostgreSQL queries
- Input validation

API keys, database passwords, and secret keys should never be committed to GitHub.

## Future Improvements

Planned improvements include:
- Advanced skill-gap analysis
- Resume analysis
- Placement company recommendations
- Internship recommendations
- More aptitude categories
- Advanced student performance analytics
- Improved AI-based career guidance

## Author

**Nilesh Lad**

**EngiPrep – Placement Preparation Platform**

Developed as a student mini-project for placement preparation and career development.