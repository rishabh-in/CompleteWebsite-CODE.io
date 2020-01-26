## CodeCompany/CodePost/forms.py

from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,TextAreaField
from wtforms.validators import DataRequired

class CodePostForm(FlaskForm):

    title=StringField("Title",validators=[DataRequired()])
    code=TextAreaField("Code",validators=[DataRequired()])
    submit=SubmitField("Post")