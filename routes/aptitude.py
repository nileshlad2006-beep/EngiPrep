from flask import Blueprint, render_template, request, session, redirect, url_for
from db import get_connection

aptitude = Blueprint("aptitude", __name__)


@aptitude.route("/Aptitude")
def aptitude_page():

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT section_id, section_name
        FROM aptitude_sections
        ORDER BY section_id
    """)

    sections = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "Preparation/Aptitude.html",
        sections=sections
    )


@aptitude.route("/Aptitude/<int:section_id>")
def topics(section_id):

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT topic_id, topic_name
        FROM aptitude_topics
        WHERE section_id = %s
        ORDER BY topic_id
    """, (section_id,))

    topics = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "Preparation/AptitudeTopics.html",
        topics=topics,
        section_id=section_id
    )


@aptitude.route("/Aptitude/Test/<int:topic_id>", methods=["GET", "POST"])
def test(topic_id):

    if "user_id" not in session:
        return redirect(url_for("login_page"))

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        cursor.execute("""
            SELECT question_id, correct_answer
            FROM aptitude_questions
            WHERE topic_id = %s
            ORDER BY question_id
        """, (topic_id,))

        questions = cursor.fetchall()

        total_questions = len(questions)
        correct_answers = 0

        for question in questions:
            question_id = question[0]
            correct_answer = question[1]

            selected_answer = request.form.get(
                f"question_{question_id}"
            )

            if selected_answer == correct_answer:
                correct_answers += 1

        if total_questions > 0:
            percentage = (correct_answers / total_questions) * 100
        else:
            percentage = 0

        score = correct_answers

        cursor.execute("""
            INSERT INTO aptitude_attempts
            (user_id, topic_id, total_questions,
             correct_answers, score, percentage)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            session["user_id"],
            topic_id,
            total_questions,
            correct_answers,
            score,
            percentage
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return render_template(
            "Preparation/AptitudeResult.html",
            total_questions=total_questions,
            correct_answers=correct_answers,
            score=score,
            percentage=round(float(percentage), 2),
            topic_id=topic_id
        )

    cursor.execute("""
        SELECT
            question_id,
            question_text,
            option_a,
            option_b,
            option_c,
            option_d
        FROM aptitude_questions
        WHERE topic_id = %s
        ORDER BY question_id
    """, (topic_id,))

    questions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "Preparation/AptitudeTest.html",
        questions=questions,
        topic_id=topic_id
    )