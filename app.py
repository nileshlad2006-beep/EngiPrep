from flask import Flask, render_template
from config import Config
from routes.auth import auth
from routes.profile import profile
from routes.dashboard import dashboard
from routes.aptitude import aptitude
from routes.chatbot import chatbot

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth)
app.register_blueprint(profile)
app.register_blueprint(dashboard)
app.register_blueprint(aptitude)
app.register_blueprint(chatbot)


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


if __name__ == "__main__":
    app.run(debug=True)