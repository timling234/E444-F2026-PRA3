from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class NameForm(FlaskForm):
    name = StringField(
        "What is your name?",
        validators=[DataRequired()]
    )

    email = StringField(
        "What is your UofT Email address?",
        validators=[DataRequired(), Email()]
    )

    submit = SubmitField("Submit")