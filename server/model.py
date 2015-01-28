from flask_wtf import Form
from wtforms import TextField, RadioField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(Form):
    type_ = RadioField('Type', choices=[('bug', 'Bug'),
                                        ('suggestion', 'Suggestion'), ('question', 'Question')],
                       validators=[DataRequired()])
    subject = TextField('Subject', validators=[Length(min=5), DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    name = TextField('Name', validators=[DataRequired()])
    email = EmailField('E-mail', validators=[Email(), DataRequired()])
