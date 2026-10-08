import psycopg2
from config import Config


def get_connection():
    return psycopg2.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD
    )


def get_topic_id(topic_name):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT topic_id
            FROM aptitude_topics
            WHERE LOWER(topic_name) = LOWER(%s)
            """,
            (topic_name,)
        )

        result = cursor.fetchone()
        return result[0] if result else None

    finally:
        cursor.close()
        conn.close()


def question_exists(topic_id, question_text):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT question_id
            FROM aptitude_questions
            WHERE topic_id = %s
            AND LOWER(TRIM(question_text)) = LOWER(TRIM(%s))
            LIMIT 1
            """,
            (topic_id, question_text)
        )

        result = cursor.fetchone()
        return True if result else False

    finally:
        cursor.close()
        conn.close()


def insert_generated_question(topic_id, question):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO aptitude_questions
            (
                topic_id,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_answer,
                difficulty,
                explanation
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING question_id
            """,
            (
                topic_id,
                question.question,
                question.option_a,
                question.option_b,
                question.option_c,
                question.option_d,
                question.correct_answer,
                "Medium",
                question.explanation
            )
        )

        question_id = cursor.fetchone()[0]

        conn.commit()

        return question_id

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


def get_student_profile(user_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
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
            FROM student_profile
            WHERE user_id = %s
            """,
            (user_id,)
        )

        result = cursor.fetchone()

        if not result:
            return None

        return {
            "college_name": result[0],
            "branch": result[1],
            "semester": result[2],
            "cgpa": result[3],
            "phone": result[4],
            "city": result[5],
            "linkedin": result[6],
            "github": result[7],
            "resume_link": result[8],
            "strengths": result[9],
            "weaknesses": result[10],
            "academic_achievements": result[11],
            "graduation_year": result[12]
        }

    finally:
        cursor.close()
        conn.close()


def get_student_aptitude_results(user_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                test_name,
                category,
                total_questions,
                score,
                percentage,
                test_date
            FROM aptitude_tests
            WHERE user_id = %s
            ORDER BY test_date DESC
            LIMIT 20
            """,
            (user_id,)
        )

        results = cursor.fetchall()

        return [
            {
                "test_name": row[0],
                "category": row[1],
                "total_questions": row[2],
                "score": row[3],
                "percentage": float(row[4]) if row[4] is not None else None,
                "test_date": str(row[5]) if row[5] is not None else None
            }
            for row in results
        ]

    finally:
        cursor.close()
        conn.close()