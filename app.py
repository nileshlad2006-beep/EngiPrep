#/signup and /login. & auth.py file is used for authentication and authorization of the user. It contains the routes for signup and login. It also contains the logic for hashing the password and checking if the user already exists in the database.
from flask import Flask, render_template
from config import Config
from routes.auth import auth
from routes.profile import profile
from routes.dashboard import dashboard
from routes.aptitude import aptitude

app = Flask(__name__)
app.config.from_object(Config)

# Register Blueprint
app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(dashboard)
app.register_blueprint(aptitude)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/Preparation")
def preparation_page():
    return render_template("Preparation.html")

@app.route("/admin")
def admin_page():
    return render_template("admin/dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)

#-------------------------------------------------------------------------------------------


    









































# this is code of the check the my database are connect or not

# from flask import Flask
# from db import get_connection

# app = Flask(__name__)

# @app.route("/")
# def home():
#     try:
#         conn = get_connection()

#         cursor = conn.cursor()

#         cursor.execute("SELECT version();")

#         version = cursor.fetchone()

#         cursor.close()
#         conn.close()

#         return f"""
#         <h2>PostgreSQL Connected Successfully</h2>
#         <p>{version[0]}</p>
#         """

#     except Exception as e:
#         return f"<h3>Database Connection Failed</h3><p>{e}</p>"

# if __name__ == "__main__":
#     app.run(debug=True)