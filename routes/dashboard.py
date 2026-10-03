from flask import Blueprint, render_template, redirect, session, url_for
from db import get_connection

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/Dashboard")
def dashboard_page():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    user_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.full_name,
            u.username,
            u.email,
            sp.college_name,
            sp.branch,
            sp.semester,
            sp.cgpa,
            sp.phone,
            sp.city,
            sp.linkedin,
            sp.github,
            sp.resume_link
        FROM users u
        LEFT JOIN student_profile sp
            ON u.user_id = sp.user_id
        WHERE u.user_id = %s
    """, (user_id,))

    profile = cursor.fetchone()

    cursor.execute("""
        SELECT COUNT(*)
        FROM student_skills
        WHERE user_id = %s
    """, (user_id,))

    skill_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM projects
        WHERE user_id = %s
    """, (user_id,))

    project_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM aptitude_attempts
        WHERE user_id = %s
    """, (user_id,))

    test_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COALESCE(AVG(percentage), 0)
        FROM aptitude_attempts
        WHERE user_id = %s
    """, (user_id,))

    average_score = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            at.attempt_id,
            ap.topic_name,
            at.total_questions,
            at.correct_answers,
            at.score,
            at.percentage,
            at.attempt_date
        FROM aptitude_attempts at
        JOIN aptitude_topics ap
            ON at.topic_id = ap.topic_id
        WHERE at.user_id = %s
        ORDER BY at.attempt_date DESC
    """, (user_id,))

    aptitude_history = cursor.fetchall()

    cursor.execute("""
        SELECT
            s.section_name,
            t.topic_name,
            COUNT(a.attempt_id) AS tests_taken,
            COALESCE(AVG(a.percentage), 0) AS average_percentage
        FROM aptitude_topics t
        JOIN aptitude_sections s
            ON t.section_id = s.section_id
        LEFT JOIN aptitude_attempts a
            ON t.topic_id = a.topic_id
            AND a.user_id = %s
        GROUP BY
            s.section_id,
            s.section_name,
            t.topic_id,
            t.topic_name
        ORDER BY
            s.section_id,
            t.topic_id
    """, (user_id,))

    topic_progress = cursor.fetchall()

    cursor.execute("""
        SELECT
            s.section_name,
            COUNT(a.attempt_id) AS tests_taken,
            COALESCE(AVG(a.percentage), 0) AS average_percentage
        FROM aptitude_sections s
        LEFT JOIN aptitude_topics t
            ON s.section_id = t.section_id
        LEFT JOIN aptitude_attempts a
            ON t.topic_id = a.topic_id
            AND a.user_id = %s
        GROUP BY
            s.section_id,
            s.section_name
        ORDER BY
            s.section_id
    """, (user_id,))

    section_progress = cursor.fetchall()

    section_progress = [
        (
            section[0],
            section[1],
            float(section[2])
        )
        for section in section_progress
    ]

    strong_topics = []
    improving_topics = []
    weak_topics = []
    not_attempted_topics = []

    for topic in topic_progress:

        section_name = topic[0]
        topic_name = topic[1]
        tests_taken = topic[2]
        average_percentage = float(topic[3])

        topic_data = (
            section_name,
            topic_name,
            tests_taken,
            average_percentage
        )

        if tests_taken == 0:
            not_attempted_topics.append(topic_data)

        elif average_percentage >= 80:
            strong_topics.append(topic_data)

        elif average_percentage >= 50:
            improving_topics.append(topic_data)

        else:
            weak_topics.append(topic_data)

    cursor.close()
    conn.close()

    return render_template(
        "Dashboard.html",
        profile=profile,
        skill_count=skill_count,
        project_count=project_count,
        test_count=test_count,
        average_score=round(float(average_score), 2),
        aptitude_history=aptitude_history,
        topic_progress=topic_progress,
        section_progress=section_progress,
        strong_topics=strong_topics,
        improving_topics=improving_topics,
        weak_topics=weak_topics,
        not_attempted_topics=not_attempted_topics
    )