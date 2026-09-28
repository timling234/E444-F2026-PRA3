from flask import Flask, render_template, session, redirect, url_for
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
            return redirect(url_for("index"))
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