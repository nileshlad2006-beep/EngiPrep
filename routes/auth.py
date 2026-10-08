from flask import Blueprint, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():

    data = request.get_json(silent=True) or {}

    full_name = data.get("full_name", "").strip()
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not full_name or not username or not email or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400

    hashed_password = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE email = %s OR username = %s
            """,
            (email, username)
        )

        existing = cursor.fetchone()

        if existing:
            return jsonify({
                "message": "User already exists"
            }), 400

        cursor.execute(
            """
            INSERT INTO users
            (full_name, username, email, password_hash, role)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                full_name,
                username,
                email,
                hashed_password,
                "student"
            )
        )

        conn.commit()

        return jsonify({
            "message": "Signup Successful"
        }), 201

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()


@auth.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    username = data.get("username", "").strip()
    password = data.get("password", "")

    if not username or not password:
        return jsonify({
            "message": "Username and password are required"
        }), 400

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT
                user_id,
                full_name,
                username,
                email,
                password_hash,
                role
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        if not user or not check_password_hash(user[4], password):
            return jsonify({
                "message": "Invalid Username or Password"
            }), 401

        session["user_id"] = user[0]
        session["full_name"] = user[1]
        session["username"] = user[2]
        session["email"] = user[3]
        session["role"] = user[5]

        cursor.execute(
            """
            SELECT profile_id
            FROM student_profile
            WHERE user_id = %s
            """,
            (user[0],)
        )

        profile = cursor.fetchone()

        if profile:
            next_page = "/Dashboard"
        else:
            next_page = "/profile"

        return jsonify({
            "message": "Login Successful",
            "user_id": user[0],
            "full_name": user[1],
            "username": user[2],
            "email": user[3],
            "role": user[5],
            "next_page": next_page
        })

    finally:
        cursor.close()
        conn.close()


@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login_page"))