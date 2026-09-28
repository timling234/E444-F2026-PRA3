from flask import (
    Flask, render_template, session,
    redirect, url_for, request, jsonify
)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timezone

from forms import NameForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key"

bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    name = session.get("name")
    email = session.get("email")
    error = None

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data

        if "utoronto" in email.lower():
            session["name"] = name
            session["email"] = email
            return redirect(url_for("chat_page"))
        else:
            session.pop("name", None)
            session.pop("email", None)
            error = "Please enter a valid UofT email address."
            name = None
            email = None

    return render_template(
        "index.html",
        form=form,
        name=name,
        email=email,
        error=error,
        current_time=datetime.now(timezone.utc)
    )


@app.route("/user/<name>")
def user(name):
    return render_template(
        "index.html",
        name=name,
        email=None,
        form=NameForm(),
        error=None,
        current_time=datetime.now(timezone.utc)
    )

@app.route("/chat", methods=["GET"])
def chat_page():
    if "email" not in session:
        return redirect(url_for("index"))

    return render_template(
        "chat.html",
        name=session.get("name")
    )


@app.route("/chat", methods=["POST"])
def chat():
    if "email" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    lower_message = message.lower()

    if "my name is " in lower_message:
        start = lower_message.index("my name is ") + len("my name is ")
        remembered_name = message[start:].strip().rstrip(".!?")

        if remembered_name:
            session["remembered_name"] = remembered_name
            reply = f"Nice to meet you, {remembered_name}!"
        else:
            reply = "Please tell me your name."

    elif "what is my name" in lower_message:
        remembered_name = session.get("remembered_name")

        if remembered_name:
            reply = f"Your name is {remembered_name}."
        else:
            reply = "I don't remember your name."

    elif "hello" in lower_message:
        reply = "Hello!"

    else:
        reply = "I don't understand."

    return jsonify({"reply": reply})


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))