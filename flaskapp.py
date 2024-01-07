# flaskapp.py

from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Sample storage for users and analytics
users = {"demo": "demo"}  # For demonstration purposes only, you should use a more secure authentication method

@app.route("/")
def home():
    if "user" in session:
        return render_template("index.html", user=session["user"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            session.setdefault("short_links", {})
            session.setdefault("analytics", [])
            return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("short_links", None)
    session.pop("analytics", None)
    return redirect(url_for("login"))

@app.route("/generate", methods=["POST"])
def generate_short_link():
    if "user" in session:
        url = request.form.get("url")
        if url:
            short_key = secrets.token_urlsafe(6)
            expiration_time = datetime.now() + timedelta(hours=48)

            session["short_links"][short_key] = {"url": url, "expires": expiration_time}
            session["analytics"].append({"short_key": short_key, "url": url, "clicks": 0})

            return redirect(url_for("home"))

    return redirect(url_for("login"))

@app.route("/analytics")
def user_analytics():
    if "user" in session:
        return render_template("analytics.html", user=session["user"], analytics=session["analytics"])

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
