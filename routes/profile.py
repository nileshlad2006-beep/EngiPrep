from flask import Blueprint, render_template, request, redirect, session, url_for
from db import get_connection

profile = Blueprint("profile", __name__)


@profile.route("/profile", methods=["GET", "POST"])
def profile_page():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    user_id = session["user_id"]

    if request.method == "POST":

        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        city = request.form.get("city")

        college_name = request.form.get("college_name")
        branch = request.form.get("branch")
        semester = request.form.get("semester")
        cgpa = request.form.get("cgpa")
        graduation_year = request.form.get("graduation_year")

        competitions = request.form.get("competitions")
        academic_achievements = request.form.get("academic_achievements")

        skills = request.form.get("skills")
        strengths = request.form.get("strengths")
        weaknesses = request.form.get("weaknesses")

        project_title = request.form.get("project_title")
        project_technologies = request.form.get("project_technologies")
        project_description = request.form.get("project_description")
        project_github = request.form.get("project_github")

        linkedin = request.form.get("linkedin")
        github = request.form.get("github")
        resume_link = request.form.get("resume_link")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET full_name = %s,
                email = %s
            WHERE user_id = %s
        """, (
            full_name,
            email,
            user_id
        ))

        cursor.execute("""
            SELECT profile_id
            FROM student_profile
            WHERE user_id = %s
        """, (user_id,))

        existing_profile = cursor.fetchone()

        if existing_profile:

            cursor.execute("""
                UPDATE student_profile
                SET college_name = %s,
                    branch = %s,
                    semester = %s,
                    cgpa = %s,
                    phone = %s,
                    city = %s,
                    linkedin = %s,
                    github = %s,
                    resume_link = %s,
                    strengths = %s,
                    weaknesses = %s,
                    academic_achievements = %s,
                    graduation_year = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = %s
            """, (
                college_name,
                branch,
                semester,
                cgpa,
                phone,
                city,
                linkedin,
                github,
                resume_link,
                strengths,
                weaknesses,
                academic_achievements,
                graduation_year,
                user_id
            ))

        else:

            cursor.execute("""
                INSERT INTO student_profile
                (
                    user_id,
                    college_name,
                    branch,
                    semester,
                    cgpa,
                    phone,
                    city,
                    linkedin,
                    github,
                    resume_link,
                    strengths,
                    weaknesses,
                    academic_achievements,
                    graduation_year
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                user_id,
                college_name,
                branch,
                semester,
                cgpa,
                phone,
                city,
                linkedin,
                github,
                resume_link,
                strengths,
                weaknesses,
                academic_achievements,
                graduation_year
            ))

        cursor.execute("""
            DELETE FROM competitions
            WHERE user_id = %s
        """, (user_id,))

        if competitions:

            competition_list = competitions.split(",")

            for competition in competition_list:

                competition = competition.strip()

                if competition:

                    cursor.execute("""
                        INSERT INTO competitions
                        (user_id, competition_name)
                        VALUES (%s, %s)
                    """, (
                        user_id,
                        competition
                    ))

        if skills:

            skill_list = skills.split(",")

            for skill in skill_list:

                skill = skill.strip()

                if skill:

                    cursor.execute("""
                        INSERT INTO skills
                        (skill_name)
                        VALUES (%s)
                        ON CONFLICT (skill_name)
                        DO NOTHING
                    """, (skill,))

                    cursor.execute("""
                        SELECT skill_id
                        FROM skills
                        WHERE skill_name = %s
                    """, (skill,))

                    skill_record = cursor.fetchone()

                    if skill_record:

                        skill_id = skill_record[0]

                        cursor.execute("""
                            INSERT INTO student_skills
                            (user_id, skill_id, skill_level)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (user_id, skill_id)
                            DO UPDATE SET
                            last_updated = CURRENT_TIMESTAMP
                        """, (
                            user_id,
                            skill_id,
                            50
                        ))

        if project_title:

            cursor.execute("""
                SELECT project_id
                FROM projects
                WHERE user_id = %s
                LIMIT 1
            """, (user_id,))

            existing_project = cursor.fetchone()

            if existing_project:

                cursor.execute("""
                    UPDATE projects
                    SET project_title = %s,
                        description = %s,
                        technologies = %s,
                        github_link = %s
                    WHERE project_id = %s
                """, (
                    project_title,
                    project_description,
                    project_technologies,
                    project_github,
                    existing_project[0]
                ))

            else:

                cursor.execute("""
                    INSERT INTO projects
                    (
                        user_id,
                        project_title,
                        description,
                        technologies,
                        github_link,
                        project_status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    user_id,
                    project_title,
                    project_description,
                    project_technologies,
                    project_github,
                    "Completed"
                ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("home"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT profile_id
        FROM student_profile
        WHERE user_id = %s
    """, (user_id,))

    existing_profile = cursor.fetchone()

    cursor.close()
    conn.close()

    if existing_profile:
        return redirect(url_for("dashboard.dashboard_page"))

    return render_template("profile.html")
